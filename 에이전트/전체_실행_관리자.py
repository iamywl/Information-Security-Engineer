#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[마스터 에이전트] 정보보안기사 필기/실기 크롤링 및 DB 구축 총괄 관리자
1. 필기 기출문제 크롤링 및 무결성 체킹
2. 실기 기출문제 크롤링 및 무결성 체킹
3. 통합 문제 DB 및 메타데이터 구축
"""

import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT_DIR = os.path.join(PROJECT_ROOT, "에이전트")


def run_agent(script_name, description):
    script_path = os.path.join(AGENT_DIR, script_name)
    print("\n" + "=" * 65)
    print(f"▶ [{description}] 실행 시작 ({script_name})")
    print("=" * 65)
    result = subprocess.run([sys.executable, script_path], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"[!] {description} 실행 중 오류 발생 (종료 코드: {result.returncode})")
    else:
        print(f"[+] {description} 완료!")
    return result.returncode == 0


def main():
    print("=" * 65)
    print(" 🛡️ 정보보안기사 필기 & 실기 아카이브 및 CBT DB 구축 오케스트레이터")
    print("=" * 65)

    # 1. 필기 크롤링
    run_agent("필기_크롤링_에이전트.py", "필기 기출문제 원문 크롤링")

    # 2. 필기 무결성 체킹
    run_agent("필기_누락_체킹_에이전트.py", "필기 기출문제 무결성 및 누락 검증")

    # 3. 실기 크롤링
    run_agent("실기_크롤링_에이전트.py", "실기 기출복원 문제 크롤링")

    # 4. 실기 누락 회차 보완
    run_agent("실기_누락회차_보완_에이전트.py", "실기 누락 회차(1, 2, 18, 19회) 복원 보완")

    # 5. 실기 무결성 체킹
    run_agent("실기_누락_체킹_에이전트.py", "실기 기출문제 무결성 및 누락 검증")

    print("\n" + "=" * 65)
    print(" ✨ 모든 에이전트 작업이 성공적으로 완료되었습니다!")
    print("=" * 65)


if __name__ == "__main__":
    main()
