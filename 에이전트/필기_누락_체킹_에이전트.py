#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 2] 정보보안기사 필기 기출문제 누락 검증 및 복구 체킹 에이전트
HWP 파일(필기/기출문제/hwp/) 및 Markdown 문서(필기/기출문제/markdown/) 무결성 검증
"""

import os
import glob
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(PROJECT_ROOT, "필기", "기출문제")
HWP_DIR = os.path.join(BASE_DIR, "hwp")
MD_DIR = os.path.join(BASE_DIR, "markdown")
STATUS_FILE = os.path.join(BASE_DIR, "STATUS.md")
CRAWLER_SCRIPT = os.path.join(PROJECT_ROOT, "에이전트", "필기_크롤링_에이전트.py")

EXPECTED_ROUNDS = range(1, 22)


def check_written_status():
    report = []
    missing_rounds = []
    incomplete_rounds = []
    total_files = 0

    print("=" * 60)
    print(" [필기 기출문제 무결성 및 분리 검증 (HWP vs Markdown)]")
    print("=" * 60)

    for r in EXPECTED_ROUNDS:
        pattern = os.path.join(HWP_DIR, f"*_{r:02d}회")
        folders = glob.glob(pattern)
        if not folders:
            pattern2 = os.path.join(HWP_DIR, f"*_{r}회")
            folders = glob.glob(pattern2)

        if not folders:
            missing_rounds.append(r)
            report.append({
                "round": r,
                "status": "❌ 누락 (HWP 폴더 없음)",
                "folder": "-",
                "hwp_count": 0,
                "pdf_count": 0,
                "has_md": False,
                "files": []
            })
            continue

        folder = folders[0]
        folder_name = os.path.basename(folder)
        files = os.listdir(folder)
        hwp_files = [f for f in files if f.endswith(".hwp") and os.path.getsize(os.path.join(folder, f)) > 1024]
        pdf_files = [f for f in files if f.endswith(".pdf") and os.path.getsize(os.path.join(folder, f)) > 1024]

        # Markdown 검사
        md_folder = os.path.join(MD_DIR, folder_name)
        has_md = os.path.exists(os.path.join(md_folder, "기출문제.md"))

        total_files += len(hwp_files) + len(pdf_files)

        is_complete = len(hwp_files) >= 1 and len(pdf_files) >= 1 and has_md
        status_str = "✅ 확보 완료" if is_complete else "⚠️ 파일 불완전"
        if not is_complete:
            incomplete_rounds.append(r)

        report.append({
            "round": r,
            "status": status_str,
            "folder": folder_name,
            "hwp_count": len(hwp_files),
            "pdf_count": len(pdf_files),
            "has_md": has_md,
            "files": hwp_files + pdf_files
        })

    for item in report:
        md_mark = "MD: O" if item["has_md"] else "MD: X"
        print(f"[{item['round']:02d}회] {item['status']} | HWP: {item['hwp_count']}개, PDF: {item['pdf_count']}개, {md_mark} | {item['folder']}")

    print("-" * 60)
    print(f"총 검사 회차: {len(EXPECTED_ROUNDS)}개 | 누락: {len(missing_rounds)}개 | 불완전: {len(incomplete_rounds)}개 | 총 HWP/PDF: {total_files}개")

    write_status_markdown(report, missing_rounds, incomplete_rounds, total_files)

    if missing_rounds or incomplete_rounds:
        print("\n[!] 누락 발생! 재수집 에이전트를 가동합니다...")
        subprocess.run(["python3", CRAWLER_SCRIPT], check=True)
        return False
    else:
        print("\n[✨] 필기 HWP 원문 파일과 Markdown 문서가 완벽히 분리 보관되었습니다!")
        return True


def write_status_markdown(report, missing, incomplete, total_files):
    md_lines = [
        "# 정보보안기사 필기 기출문제 확보 현황 (HWP vs Markdown 분리 저장)\n",
        f"* **전체 대상 회차:** 1회 ~ 21회 (총 {len(EXPECTED_ROUNDS)}개 회차)",
        f"* **확보 완료 회차:** {len(EXPECTED_ROUNDS) - len(missing) - len(incomplete)}개 회차",
        f"* **누락 회차:** {len(missing)}개",
        f"* **총 원문 파일 수:** {total_files}개 (HWP/PDF)",
        f"* **저장 구조:** 원본 바이너리는 `hwp/`, 정리 문서는 `markdown/` 디렉토리에 분리 저장\n",
        "| 회차 | 상태 | HWP 폴더 | HWP 수 | PDF 수 | Markdown 문서 | HWP/PDF 파일 목록 |",
        "| :---: | :---: | :--- | :---: | :---: | :---: | :--- |"
    ]

    for item in report:
        md_str = "✅ 있음" if item["has_md"] else "❌ 없음"
        files_str = "<br>".join(item["files"]) if item["files"] else "-"
        md_lines.append(f"| {item['round']}회 | {item['status']} | `hwp/{item['folder']}` | {item['hwp_count']} | {item['pdf_count']} | {md_str} | {files_str} |")

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[*] 필기 상태 리포트 저장 완료: {STATUS_FILE}")


if __name__ == "__main__":
    check_written_status()
