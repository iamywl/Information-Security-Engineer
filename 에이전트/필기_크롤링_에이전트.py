#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 1] 정보보안기사 필기 기출문제 크롤링 에이전트
출처: 전자문제집 CBT (comcbt.com/xe/ccw)
- HWP/PDF 원문 바이너리 -> 필기/기출문제/hwp/[회차]/
- Markdown/Text 문서    -> 필기/기출문제/markdown/[회차]/
"""

import os
import re
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

BASE_URL = "https://www.comcbt.com/xe/ccw"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "필기", "기출문제")
HWP_OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, "hwp")
MD_OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, "markdown")


def fetch_html(url, referer=None):
    headers = dict(HEADERS)
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def download_file(file_url, save_path, referer=None, max_retries=3):
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1024:
        print(f"  [스킵] 이미 존재함: {os.path.basename(save_path)} ({os.path.getsize(save_path):,} bytes)")
        return True

    headers = dict(HEADERS)
    if referer:
        headers["Referer"] = referer

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(file_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if len(data) < 500 and (b"<html" in data.lower() or b"<script" in data.lower()):
                    raise ValueError("HTML response received instead of binary file")
                
                with open(save_path, "wb") as f:
                    f.write(data)
                print(f"  [성공] 다운로드 완료: {os.path.basename(save_path)} ({len(data):,} bytes)")
                return True
        except Exception as e:
            print(f"  [재시도 {attempt}/{max_retries}] 다운로드 실패 ({e}): {os.path.basename(save_path)}")
            time.sleep(2)

    return False


def get_post_list():
    """게시판 1~2페이지에서 정보보안기사 필기 회차 게시글 링크 추출"""
    posts = []
    seen_urls = set()

    pages = [
        "https://www.comcbt.com/xe/ccw",
        "https://www.comcbt.com/xe/index.php?mid=ccw&page=2"
    ]

    for p_url in pages:
        print(f"[*] 게시글 목록 조회 중: {p_url}")
        try:
            html = fetch_html(p_url)
            soup = BeautifulSoup(html, "html.parser")
            for tr in soup.select("table tr"):
                for a in tr.find_all("a"):
                    title = a.get_text().strip()
                    href = a.get("href", "")
                    if "정보보안기사 필기 기출문제 및 CBT" in title and href not in seen_urls:
                        if href.startswith("/"):
                            href = "https://www.comcbt.com" + href
                        elif not href.startswith("http"):
                            href = "https://www.comcbt.com/xe/" + href

                        m = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일.*?(\d{1,2})회', title)
                        if m:
                            year, month, day, round_num = m.group(1), m.group(2).zfill(2), m.group(3).zfill(2), int(m.group(4))
                            posts.append({
                                "title": title,
                                "url": href,
                                "year": year,
                                "month": month,
                                "day": day,
                                "round": round_num,
                                "folder_name": f"{year}년_{month}월_{round_num:02d}회"
                            })
                            seen_urls.add(href)
        except Exception as e:
            print(f"[!] 목록 조회 오류 ({p_url}): {e}")

    posts.sort(key=lambda x: x["round"])
    return posts


def process_post(post):
    """HWP/PDF는 hwp/ 폴더에, 텍스트/마크다운은 markdown/ 폴더에 분리 저장"""
    hwp_folder = os.path.join(HWP_OUTPUT_DIR, post["folder_name"])
    md_folder = os.path.join(MD_OUTPUT_DIR, post["folder_name"])
    os.makedirs(hwp_folder, exist_ok=True)
    os.makedirs(md_folder, exist_ok=True)

    print(f"\n==================================================")
    print(f"[*] [{post['round']}회] {post['year']}년 {post['month']}월 ({post['folder_name']})")
    print(f"[*] URL: {post['url']}")

    try:
        html = fetch_html(post["url"])
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"[!] 게시글 열기 실패: {e}")
        return False

    # 1. 텍스트 및 마크다운 생성 -> markdown/ 폴더에 저장
    content_div = soup.select_one(".xe_content, article, .document_content")
    raw_text = content_div.get_text("\n") if content_div else ""
    text_path = os.path.join(md_folder, "content.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(raw_text)

    # 2. 첨부파일(HWP, PDF) -> hwp/ 폴더에 분리 저장
    downloaded_files = []
    seen_links = set()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text().strip()
        if "procFileDownload" in href and href not in seen_links:
            seen_links.add(href)
            if href.startswith("/"):
                href = "https://www.comcbt.com" + href

            filename = text
            if not (filename.endswith(".hwp") or filename.endswith(".pdf") or filename.endswith(".zip")):
                m = re.search(r'([^\s/]+\.(?:hwp|pdf|zip))', text, re.I)
                if m:
                    filename = m.group(1)
                else:
                    filename = f"{post['folder_name']}_attached_{len(downloaded_files)+1}.bin"

            filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
            save_path = os.path.join(hwp_folder, filename)

            success = download_file(href, save_path, referer=post["url"])
            if success:
                downloaded_files.append(filename)
            time.sleep(0.5)

    # 3. markdown/ 폴더에 안내 마크다운 문서 기출문제.md 생성
    md_file_path = os.path.join(md_folder, "기출문제.md")
    md_lines = [
        f"# 정보보안기사 필기 제{post['round']}회 ({post['year']}년 {post['month']}월)\n",
        f"* **시험 구분:** 국가기술자격 정보보안기사 필기",
        f"* **문항 구성:** 총 100문항 (과목당 20문항, 4지 선다형)\n",
        "## 과목별 구성",
        "1. 제1과목: 시스템 보안 (1번 ~ 20번)",
        "2. 제2과목: 네트워크 보안 (21번 ~ 40번)",
        "3. 제3과목: 애플리케이션 보안 (41번 ~ 60번)",
        "4. 제4과목: 정보보안 일반 (61번 ~ 80번)",
        "5. 제5과목: 정보보안 관리 및 법규 (81번 ~ 100번)\n",
        "## 원문 다운로드 파일 (HWP / PDF)",
        f"본 회차의 원문 파일은 `../hwp/{post['folder_name']}/` 에 보관되어 있습니다.\n"
    ]
    for df in sorted(downloaded_files):
        md_lines.append(f"* [`{df}`](../../hwp/{post['folder_name']}/{df})")
    
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"[*] HWP/PDF 파일 ({len(downloaded_files)}개) -> {hwp_folder}")
    print(f"[*] Markdown 문서 -> {md_folder}")
    return len(downloaded_files) > 0


def main():
    print("=" * 60)
    print(" 정보보안기사 필기 기출문제 크롤링 에이전트 시작 (HWP / MD 분리 저장)")
    print("=" * 60)
    os.makedirs(HWP_OUTPUT_DIR, exist_ok=True)
    os.makedirs(MD_OUTPUT_DIR, exist_ok=True)

    posts = get_post_list()
    print(f"\n[+] 총 {len(posts)}개 회차 발굴 완료 (1회 ~ {posts[-1]['round'] if posts else 0}회)")

    success_count = 0
    for p in posts:
        ok = process_post(p)
        if ok:
            success_count += 1
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print(f"[*] 필기 기출 크롤링 완료: {success_count}/{len(posts)} 회차 처리됨")
    print(f"[*] HWP 파일 위치: {HWP_OUTPUT_DIR}")
    print(f"[*] Markdown 문서 위치: {MD_OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
