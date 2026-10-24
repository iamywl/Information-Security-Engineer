#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[병렬 마스터] 정보보안기사 필기/실기 병렬 패턴 분석 오케스트레이터
concurrent.futures.ProcessPoolExecutor를 활용하여
필기 분석 에이전트와 실기 분석 에이전트를 완전 병렬(동시)로 실행
"""

import os
import sys
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT_DIR = os.path.join(PROJECT_ROOT, "에이전트")


def run_single_agent(agent_filename, task_name):
    """독립 프로세스에서 단일 에이전트 실행"""
    start_time = time.time()
    script_path = os.path.join(AGENT_DIR, agent_filename)
    print(f"▶ [병렬 가동 시작] {task_name} (PID: {os.getpid()})")
    
    result = subprocess.run([sys.executable, script_path], cwd=PROJECT_ROOT, capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    return {
        "name": task_name,
        "script": agent_filename,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "elapsed": elapsed
    }


def main():
    print("=" * 70)
    print(" 🚀 정보보안기사 필기 & 실기 병렬 패턴 분석 오케스트레이터 가동")
    print("=" * 70)
    total_start = time.time()

    tasks = [
        ("필기_패턴분석_에이전트.py", "필기 기출 빅데이터(2,100문항) 패턴 분석"),
        ("실기_패턴분석_에이전트.py", "실기 기출 빅데이터(417문항) 패턴 분석")
    ]

    print(f"[*] {len(tasks)}개의 에이전트를 독립 프로세스로 동시(병렬) 실행합니다...\n")

    # 병렬 프로세스 풀 가동
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(run_single_agent, script, name) for script, name in tasks]
        results = [f.result() for f in futures]

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 70)
    print(" [병렬 실행 완료 리포트]")
    print("=" * 70)

    for r in results:
        status_str = "✅ 성공" if r["returncode"] == 0 else "❌ 실패"
        print(f"* {r['name']}: {status_str} (소요 시간: {r['elapsed']:.2f}초)")
        if r["returncode"] != 0:
            print(f"  [에러 내용]:\n{r['stderr']}")

    print("-" * 70)
    print(f"[*] 총 병렬 소요 시간: {total_elapsed:.2f}초")
    print(f"[*] 필기 패턴 보고서: 필기/기출문제/패턴_분석_보고서.md")
    print(f"[*] 실기 패턴 보고서: 실기/기출문제/패턴_분석_보고서.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
