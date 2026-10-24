#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 4] 정보보안기사 실기 기출문제 누락 검증 및 체킹 에이전트
Markdown 문서(실기/기출문제/markdown/) 및 HWP 원본(실기/기출문제/hwp/) 무결성 검증
"""

import os
import json
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(PROJECT_ROOT, "실기", "기출문제")
MD_DIR = os.path.join(BASE_DIR, "markdown")
HWP_DIR = os.path.join(BASE_DIR, "hwp")
STATUS_FILE = os.path.join(BASE_DIR, "STATUS.md")

ALL_ROUNDS = range(1, 30)


def check_practical_status():
    report = []
    missing_rounds = []
    incomplete_rounds = []
    total_questions = 0

    print("=" * 60)
    print(" [실기 기출문제 무결성 및 분리 검증 (Markdown vs HWP)]")
    print("=" * 60)

    for r in ALL_ROUNDS:
        pattern = os.path.join(MD_DIR, f"{r:02d}회")
        folders = glob.glob(pattern)
        if not folders:
            pattern2 = os.path.join(MD_DIR, f"{r}회")
            folders = glob.glob(pattern2)

        if not folders:
            missing_rounds.append(r)
            report.append({
                "round": r,
                "status": "❌ 미확보 (복원 자료 필요)",
                "folder": "-",
                "q_count": 0,
                "has_md": False,
                "has_json": False
            })
            continue

        folder = folders[0]
        json_file = os.path.join(folder, "questions.json")
        md_file = os.path.join(folder, "기출복원_원문.md")

        q_count = 0
        if os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    q_count = len(data.get("questions", []))
            except Exception:
                q_count = 0

        total_questions += q_count
        has_md = os.path.exists(md_file) and os.path.getsize(md_file) > 100
        has_json = q_count > 0

        is_complete = has_md and has_json and q_count >= 6
        if is_complete:
            status_str = f"✅ 확보 완료 ({q_count}문항)"
        else:
            status_str = f"⚠️ 부분 복원 ({q_count}문항)"
            incomplete_rounds.append(r)

        report.append({
            "round": r,
            "status": status_str,
            "folder": os.path.basename(folder),
            "q_count": q_count,
            "has_md": has_md,
            "has_json": has_json
        })

    for item in report:
        print(f"[{item['round']:02d}회] {item['status']} | markdown/{item['folder']}")

    print("-" * 60)
    print(f"총 검사 회차: {len(ALL_ROUNDS)}개 | 누락: {len(missing_rounds)}개 | 총 복원 문항: {total_questions}문항")

    write_status_markdown(report, missing_rounds, incomplete_rounds, total_questions)

    return len(missing_rounds) == 0


def write_status_markdown(report, missing, incomplete, total_questions):
    md_lines = [
        "# 정보보안기사 실기 기출문제 확보 현황 (Markdown 분리 보관)\n",
        f"* **전체 대상 회차:** 1회 ~ 29회 (총 {len(ALL_ROUNDS)}개 회차)",
        f"* **확보 완료 회차:** {len(ALL_ROUNDS) - len(missing)}개 회차",
        f"* **총 복원 문항 수:** {total_questions}문항",
        f"* **저장 구조:** 마크다운 및 JSON 문서는 `markdown/`에 보관, HWP 원본은 `hwp/`에 보관\n",
        "| 회차 | 상태 | 문항 수 | 마크다운(MD) | JSON | 폴더명 |",
        "| :---: | :--- | :---: | :---: | :---: | :--- |"
    ]

    for item in report:
        md_check = "O" if item["has_md"] else "X"
        json_check = "O" if item["has_json"] else "X"
        md_lines.append(f"| {item['round']}회 | {item['status']} | {item['q_count']}문항 | {md_check} | {json_check} | `markdown/{item['folder']}` |")

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[*] 실기 상태 리포트 저장 완료: {STATUS_FILE}")


if __name__ == "__main__":
    check_practical_status()
