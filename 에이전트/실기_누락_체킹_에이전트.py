#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 4] 정보보안기사 실기 기출문제 누락 검증 및 체킹 에이전트
실기 1회 ~ 29회 복원 상태, 문항 수, 파일 무결성(MD, JSON, TXT) 검사
누락 회차 보고 및 STATUS.md 생성
"""

import os
import json
import glob
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(PROJECT_ROOT, "실기", "기출문제")
CRAWLER_SCRIPT = os.path.join(PROJECT_ROOT, "에이전트", "실기_크롤링_에이전트.py")
STATUS_FILE = os.path.join(TARGET_DIR, "STATUS.md")

# 정보보안기사 실기 총 회차 범위
ALL_ROUNDS = range(1, 30)


def check_practical_status():
    report = []
    missing_rounds = []
    incomplete_rounds = []
    total_questions = 0

    print("=" * 60)
    print(" [실기 기출문제 무결성 및 누락 검증]")
    print("=" * 60)

    for r in ALL_ROUNDS:
        pattern = os.path.join(TARGET_DIR, f"{r:02d}회")
        folders = glob.glob(pattern)
        if not folders:
            pattern2 = os.path.join(TARGET_DIR, f"{r}회")
            folders = glob.glob(pattern2)

        if not folders:
            missing_rounds.append(r)
            report.append({
                "round": r,
                "status": "❌ 미확보 (복원 자료 탐색 필요)",
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

        is_complete = has_md and has_json and q_count >= 10
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

    # 출력
    for item in report:
        print(f"[{item['round']:02d}회] {item['status']} | {item['folder']}")

    print("-" * 60)
    print(f"총 검사 회차: {len(ALL_ROUNDS)}개 | 누락: {len(missing_rounds)}개 | 불완전: {len(incomplete_rounds)}개 | 총 복원 문항: {total_questions}문항")

    write_status_markdown(report, missing_rounds, incomplete_rounds, total_questions)

    if missing_rounds:
        print(f"\n[안내] 누락 회차 {missing_rounds}는 오픈소스 아카이브 및 블로그 추가 크롤링으로 보완 가능합니다.")

    return len(missing_rounds) == 0 and len(incomplete_rounds) == 0


def write_status_markdown(report, missing, incomplete, total_questions):
    md_lines = [
        "# 정보보안기사 실기 기출문제 확보 현황\n",
        f"* **전체 대상 회차:** 1회 ~ 29회 (총 {len(ALL_ROUNDS)}개 회차)",
        f"* **확보 완료 회차:** {len(ALL_ROUNDS) - len(missing) - len(incomplete)}개 회차",
        f"* **부분/누락 회차:** {len(missing) + len(incomplete)}개 회차",
        f"* **총 복원 문항 수:** {total_questions}문항\n",
        "> [!NOTE]",
        "> 정보보안기사 실기 시험은 KCA에서 문제지를 회수하여 비공개로 운영되므로, 모든 기출문제는 수험생의 기억을 기반으로 복원된 데이터입니다.\n",
        "| 회차 | 상태 | 문항 수 | 마크다운(MD) | JSON | 폴더명 |",
        "| :---: | :--- | :---: | :---: | :---: | :--- |"
    ]

    for item in report:
        md_check = "O" if item["has_md"] else "X"
        json_check = "O" if item["has_json"] else "X"
        md_lines.append(f"| {item['round']}회 | {item['status']} | {item['q_count']}문항 | {md_check} | {json_check} | `{item['folder']}` |")

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[*] 실기 상태 리포트 저장 완료: {STATUS_FILE}")


if __name__ == "__main__":
    check_practical_status()
