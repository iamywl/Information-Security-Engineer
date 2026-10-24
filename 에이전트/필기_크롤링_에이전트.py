#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 1] 정보보안기사 필기 기출문제 크롤링 에이전트
출처: 전자문제집 CBT (comcbt.com/xe/ccw)
원문 HWP 및 PDF 파일 다운로드, 본문 텍스트 아카이빙
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
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "필기", "기출문제")


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
                # HTML 에러 페이지가 내려왔는지 검사
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
                        # Full URL 정규화
                        if href.startswith("/"):
                            href = "https://www.comcbt.com" + href
                        elif not href.startswith("http"):
                            href = "https://www.comcbt.com/xe/" + href

                        # 회차 정보 추출
                        # 예: 정보보안기사 필기 기출문제 및 CBT 2023년 03월 11일(21회)
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

    # 회차 기준 오름차순 정렬 (1회 -> 21회)
    posts.sort(key=lambda x: x["round"])
    return posts


def process_post(post):
    """개별 게시글에서 첨부파일(HWP, PDF)과 본문 텍스트 추출"""
    folder = os.path.join(OUTPUT_DIR, post["folder_name"])
    os.makedirs(folder, exist_ok=True)

    print(f"\n==================================================")
    print(f"[*] [{post['round']}회] {post['year']}년 {post['month']}월 ({post['folder_name']})")
    print(f"[*] URL: {post['url']}")

    try:
        html = fetch_html(post["url"])
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"[!] 게시글 열기 실패: {e}")
        return False

    # 본문 텍스트 백업 (토큰 친화적 파싱을 위한 원천 텍스트)
    content_div = soup.select_one(".xe_content, article, .document_content")
    if content_div:
        text_path = os.path.join(folder, "content.txt")
        raw_text = content_div.get_text("\n")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(raw_text)

    # 첨부파일 링크 탐색
    downloaded_files = []
    seen_links = set()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text().strip()
        if "procFileDownload" in href and href not in seen_links:
            seen_links.add(href)
            if href.startswith("/"):
                href = "https://www.comcbt.com" + href

            # 파일명 결정
            filename = text
            if not (filename.endswith(".hwp") or filename.endswith(".pdf") or filename.endswith(".zip")):
                # href 내 또는 text 파싱
                m = re.search(r'([^\s/]+\.(?:hwp|pdf|zip))', text, re.I)
                if m:
                    filename = m.group(1)
                else:
                    filename = f"{post['folder_name']}_attached_{len(downloaded_files)+1}.bin"

            # 안전한 파일명 정리
            filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
            save_path = os.path.join(folder, filename)

            # 다운로드 실행
            success = download_file(href, save_path, referer=post["url"])
            if success:
                downloaded_files.append(filename)
            time.sleep(0.5)  # 서버 부하 방지 매너 딜레이

    print(f"[*] 다운로드 완료 파일: {downloaded_files}")
    return len(downloaded_files) > 0


def main():
    print("=" * 60)
    print(" 정보보안기사 필기 기출문제 크롤링 에이전트 시작")
    print("=" * 60)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    posts = get_post_list()
    print(f"\n[+] 총 {len(posts)}개 회차 발굴 완료 (1회 ~ {posts[-1]['round'] if posts else 0}회)")

    success_count = 0
    for p in posts:
        ok = process_post(p)
        if ok:
            success_count += 1
        time.sleep(1)  # 회차별 1초 대기

    print("\n" + "=" * 60)
    print(f"[*] 필기 기출 크롤링 완료: {success_count}/{len(posts)} 회차 처리됨")
    print(f"[*] 저장 위치: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
