#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 2] 정보보안기사 필기 기출문제 누락 검증 및 복구 체킹 에이전트
1회 ~ 21회 전 회차 HWP, PDF 원문 파일 무결성 및 누락 검사
누락 발생 시 자동 재수집(크롤링) 트리거
"""

import os
import glob
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "필기", "기출문제")
CRAWLER_SCRIPT = os.path.join(PROJECT_ROOT, "에이전트", "필기_크롤링_에이전트.py")
STATUS_FILE = os.path.join(TARGET_DIR, "STATUS.md")

EXPECTED_ROUNDS = range(1, 22)  # 1회부터 21회까지


def check_written_status():
    report = []
    missing_rounds = []
    incomplete_rounds = []
    total_files = 0

    print("=" * 60)
    print(" [필기 기출문제 무결성 및 누락 검증]")
    print("=" * 60)

    for r in EXPECTED_ROUNDS:
        # 폴더 검색 (예: *_01회, *_1회)
        pattern = os.path.join(TARGET_DIR, f"*_{r:02d}회")
        folders = glob.glob(pattern)
        if not folders:
            pattern2 = os.path.join(TARGET_DIR, f"*_{r}회")
            folders = glob.glob(pattern2)

        if not folders:
            missing_rounds.append(r)
            report.append({
                "round": r,
                "status": "❌ 누락 (폴더 없음)",
                "folder": "-",
                "hwp_count": 0,
                "pdf_count": 0,
                "files": []
            })
            continue

        folder = folders[0]
        files = os.listdir(folder)
        hwp_files = [f for f in files if f.endswith(".hwp") and os.path.getsize(os.path.join(folder, f)) > 1024]
        pdf_files = [f for f in files if f.endswith(".pdf") and os.path.getsize(os.path.join(folder, f)) > 1024]

        total_files += len(hwp_files) + len(pdf_files)

        is_complete = len(hwp_files) >= 1 and len(pdf_files) >= 1
        status_str = "✅ 확보 완료" if is_complete else "⚠️ 파일 불완전"
        if not is_complete:
            incomplete_rounds.append(r)

        report.append({
            "round": r,
            "status": status_str,
            "folder": os.path.basename(folder),
            "hwp_count": len(hwp_files),
            "pdf_count": len(pdf_files),
            "files": hwp_files + pdf_files
        })

    # 콘솔 출력
    for item in report:
        print(f"[{item['round']:02d}회] {item['status']} | HWP: {item['hwp_count']}개, PDF: {item['pdf_count']}개 | {item['folder']}")

    print("-" * 60)
    print(f"총 검사 회차: {len(EXPECTED_ROUNDS)}개 | 누락 회차: {len(missing_rounds)}개 | 불완전 회차: {len(incomplete_rounds)}개 | 총 원문 파일: {total_files}개")

    # STATUS.md 저장
    write_status_markdown(report, missing_rounds, incomplete_rounds, total_files)

    # 누락 또는 불완전 시 자동 재크롤링 트리거
    if missing_rounds or incomplete_rounds:
        print("\n[!] 누락되거나 불완전한 회차가 발견되었습니다. 재수집 에이전트를 가동합니다...")
        subprocess.run(["python3", CRAWLER_SCRIPT], check=True)
        print("\n[*] 재수집 완료 후 재검증을 권장합니다.")
        return False
    else:
        print("\n[✨] 모든 회차(1회~21회) 원문 HWP/PDF 파일이 완벽하게 확보되었습니다!")
        return True


def write_status_markdown(report, missing, incomplete, total_files):
    md_lines = [
        "# 정보보안기사 필기 기출문제 확보 현황\n",
        f"* **전체 대상 회차:** 1회 ~ 21회 (총 {len(EXPECTED_ROUNDS)}개 회차)",
        f"* **확보 완료 회차:** {len(EXPECTED_ROUNDS) - len(missing) - len(incomplete)}개 회차",
        f"* **누락 회차:** {len(missing)}개 ({missing})",
        f"* **총 원문 파일 수:** {total_files}개\n",
        "| 회차 | 상태 | 폴더명 | HWP 수 | PDF 수 | 파일 목록 |",
        "| :---: | :---: | :--- | :---: | :---: | :--- |"
    ]

    for item in report:
        files_str = "<br>".join(item["files"]) if item["files"] else "-"
        md_lines.append(f"| {item['round']}회 | {item['status']} | `{item['folder']}` | {item['hwp_count']} | {item['pdf_count']} | {files_str} |")

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[*] 상태 리포트 저장 완료: {STATUS_FILE}")


if __name__ == "__main__":
    check_written_status()
