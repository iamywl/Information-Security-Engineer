#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 3] 정보보안기사 실기 기출문제 크롤링 에이전트
출처: 뉴비티(NewBT) 기출문제 은행 및 복원 아카이브
역대 실기 복원 문제(단답형, 서술형, 실무형) 수집, 정제 마크다운/JSON 아카이빙
"""

import os
import re
import json
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

BASE_URL = "https://newbt.kr"
LIST_URL = "https://newbt.kr/" + urllib.parse.quote("시험/정보보안기사 실기")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "실기", "기출문제")


def fetch_html(url):
    parsed = urllib.parse.urlsplit(url)
    encoded_path = urllib.parse.quote(urllib.parse.unquote(parsed.path))
    safe_url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, encoded_path, parsed.query, parsed.fragment))
    req = urllib.request.Request(safe_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def get_practical_exam_links():
    """실기 기출 회차 목록 수집 (여러 등록자가 있는 경우 모두 수집)"""
    print(f"[*] 실기 기출 목록 조회 중: {LIST_URL}")
    html = fetch_html(LIST_URL)
    soup = BeautifulSoup(html, "html.parser")

    round_map = {}  # { round_num: [url1, url2, ...] }

    for a in soup.find_all("a"):
        h = a.get("href", "")
        t = a.get_text().strip()
        if "/시험/정보보안기사 실기/" in h:
            m = re.search(r"(\d+)회", t)
            if not m:
                # URL에서 파싱 시도
                decoded_h = urllib.parse.unquote(h)
                m = re.search(r"(\d+)회", decoded_h)
            
            if m:
                r_num = int(m.group(1))
                full_url = BASE_URL + h if h.startswith("/") else h
                if r_num not in round_map:
                    round_map[r_num] = []
                if full_url not in round_map[r_num]:
                    round_map[r_num].append(full_url)

    return round_map


def parse_exam_page(url):
    """실기 시험 상세 페이지 파싱 (문제, 보기, 정답, 해설 추출)"""
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    questions = []
    current_section = "단답형"

    # 페이지 텍스트 내 섹션 마커 추적
    # blog-post 컨테이너들을 순회
    posts = soup.select(".blog-post")
    for p in posts:
        # 섹션 헤더(단답형, 서술형, 실무형)가 이전 형제 요소나 내부에 있는지 확인
        prev_node = p.find_previous(["h3", "h4", "h5", "div", "b", "strong"])
        if prev_node:
            prev_t = prev_node.get_text().strip()
            if "단답형" in prev_t:
                current_section = "단답형"
            elif "서술형" in prev_t:
                current_section = "서술형"
            elif "실무형" in prev_t:
                current_section = "실무형"

        # 문항 번호
        num_span = p.select_one("span.number")
        q_num = None
        if num_span:
            try:
                q_num = int(num_span.get_text().strip())
            except ValueError:
                pass

        # 문항 지문
        subject_el = p.select_one("h5.subject")
        q_text = ""
        if subject_el:
            # span.number 텍스트 제거
            for s in subject_el.find_all("span", class_="number"):
                s.decompose()
            q_text = subject_el.get_text(" ").strip()
            # 맨 앞 번호 점 제거 (예: "1 . " or ". ")
            q_text = re.sub(r'^\s*[\.\)]\s*', '', q_text)

        # 추가 내용 (코드, 지문 박스 pre.contents)
        pre_content = p.select_one("pre.contents, div.contents")
        extra_content = pre_content.get_text("\n").strip() if pre_content else ""

        # 정답 (shortAnswer)
        ans_el = p.select_one(".shortAnswer, .answer, div[class*=shortAnswer]")
        answer = ans_el.get_text(" ").strip() if ans_el else ""

        # 해설 (wiki 등)
        wiki_el = p.select_one(".wiki, div[id^=wiki], div[class*=explanation]")
        explanation = wiki_el.get_text("\n").strip() if wiki_el else ""
        # 불필요한 위키 힌트 문구 제거
        explanation = re.sub(r'위키해설\s*클릭하면\s*보입니다\.?', '', explanation).strip()

        if q_text or extra_content:
            questions.append({
                "number": q_num,
                "type": current_section,
                "question": q_text,
                "extra": extra_content,
                "answer": answer,
                "explanation": explanation
            })

    return questions


def save_practical_round(round_num, questions):
    """실기 회차별 마크다운, 텍스트, JSON 저장"""
    folder = os.path.join(OUTPUT_DIR, f"{round_num:02d}회")
    os.makedirs(folder, exist_ok=True)

    # 1. JSON 저장
    json_path = os.path.join(folder, "questions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "exam_name": f"정보보안기사 실기 제{round_num}회 기출복원",
            "round": round_num,
            "total_questions": len(questions),
            "questions": questions
        }, f, ensure_ascii=False, indent=2)

    # 2. Markdown 문서 생성
    md_path = os.path.join(folder, "기출복원_원문.md")
    md_lines = [
        f"# 정보보안기사 실기 제{round_num}회 기출문제 (복원)\n",
        f"* **시험 구분:** 국가기술자격 정보보안기사 실기",
        f"* **문항 수:** 총 {len(questions)}문항",
        f"* **출처:** 수험생 기출 복원 아카이브\n",
        "---\n"
    ]

    for q in questions:
        num_str = f"{q['number']}번" if q['number'] else "문제"
        type_str = f"[{q['type']}]" if q.get('type') else ""
        md_lines.append(f"### {num_str} {type_str}\n")
        md_lines.append(f"{q['question']}\n")
        if q["extra"]:
            md_lines.append("```text\n" + q["extra"] + "\n```\n")
        
        md_lines.append(f"> **정답:** {q['answer'] if q['answer'] else '(미입력)'}\n")
        if q["explanation"]:
            md_lines.append(f"> **해설:** {q['explanation']}\n")
        md_lines.append("\n---\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # 3. 텍스트 문서 생성
    txt_path = os.path.join(folder, "기출복원_원문.txt")
    txt_lines = [f"[정보보안기사 실기 제{round_num}회]\n"]
    for q in questions:
        num_str = f"{q['number']}." if q['number'] else "-"
        txt_lines.append(f"{num_str} [{q['type']}] {q['question']}")
        if q["extra"]:
            txt_lines.append(q["extra"])
        txt_lines.append(f"[정답] {q['answer']}")
        if q["explanation"]:
            txt_lines.append(f"[해설] {q['explanation']}")
        txt_lines.append("\n" + ("=" * 40) + "\n")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"  [저장 완료] {round_num:02d}회: 총 {len(questions)}문항 저장됨 (JSON, MD, TXT)")


def main():
    print("=" * 60)
    print(" 정보보안기사 실기 기출문제 크롤링 에이전트 시작")
    print("=" * 60)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    round_map = get_practical_exam_links()
    rounds = sorted(round_map.keys())
    print(f"[+] 총 {len(rounds)}개 실기 회차 발견: {rounds}")

    for r in rounds:
        print(f"\n[*] [{r:02d}회] 기출 복원 수집 중...")
        all_q = []
        seen_questions = set()

        for url in round_map[r]:
            try:
                q_list = parse_exam_page(url)
                for q in q_list:
                    # 중복 판정 (지문 앞 30자)
                    key = q["question"][:30]
                    if key and key not in seen_questions:
                        seen_questions.add(key)
                        all_q.append(q)
                time.sleep(0.5)
            except Exception as e:
                print(f"  [!] 페이지 파싱 실패 ({url}): {e}")

        # 번호순 정렬
        all_q.sort(key=lambda x: x["number"] if x["number"] is not None else 999)

        if all_q:
            save_practical_round(r, all_q)
        else:
            print(f"  [!] {r}회 문항 수집 실패")

        time.sleep(0.8)

    print("\n" + "=" * 60)
    print("[*] 실기 기출문제 크롤링 완료")
    print(f"[*] 저장 위치: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
