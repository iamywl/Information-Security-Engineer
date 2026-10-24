#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[에이전트 3-보완] 정보보안기사 실기 누락 회차(1회, 2회, 18회, 19회) 복원 데이터 생성 에이전트
수험생 커뮤니티 및 합격자 블로그 복원 기출문제를 바탕으로 정규 스키마 구축
"""

import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "실기", "기출문제", "markdown")

SUPPLEMENTAL_DATA = {
    1: {
        "round": 1,
        "name": "정보보안기사 실기 제1회 기출복원",
        "questions": [
            {
                "number": 1,
                "type": "단답형",
                "question": "네트워크 공격에서 공격자가 특정 네트워크의 모든 시스템에 다량의 브로드캐스트 패킷을 전송하고, 이를 받은 시스템들이 대상 시스템에 많은 양의 ICMP 패킷을 보내게 하여 서비스 장애를 일으키는 공격 방법은 무엇인가?",
                "extra": "",
                "answer": "Smurf 공격 (스머프 공격)",
                "explanation": "공격자가 출발지 IP를 희생자 IP로 위조(IP Spoofing)하여 브로드캐스트 대역으로 ICMP Echo Request를 전송하면, 대역 내 모든 호스트가 희생자에게 ICMP Echo Reply를 쏟아붓는 반사 DoS 공격입니다."
            },
            {
                "number": 2,
                "type": "단답형",
                "question": "서버가 클라이언트 요청을 통해 내부 네트워크 자원에 접근하게 되는 취약점 및 공격 기법으로, 외부에서 접근할 수 없는 내부망 시스템(메타데이터 서버 등)에 임의 요청을 전달하는 공격은 무엇인가?",
                "extra": "",
                "answer": "SSRF (Server-Side Request Forgery)",
                "explanation": "서버 사이드 요청 위조 취약점으로 웹 서버가 원격 리소스를 가져오는 기능을 악용하여 내부망 인트라넷, 루프백 인터페이스(127.0.0.1) 등을 탐색하거나 공격합니다."
            },
            {
                "number": 3,
                "type": "단답형",
                "question": "VLAN 구성과 관련하여 (A) 관리자가 스위치의 각 포트에 수동으로 VLAN을 할당하는 방식과 (B) 호스트의 MAC 주소나 인증 정보를 기반으로 자동 할당하는 방식의 명칭을 쓰고, (C) Cisco 스위치에서 VLAN 구성을 확인하는 명령어를 기술하시오.",
                "extra": "",
                "answer": "(A) 정적 VLAN (Static VLAN), (B) 동적 VLAN (Dynamic VLAN), (C) show vlan",
                "explanation": "포트 기반 할당은 정적 VLAN이며, MAC/프로토콜 기반은 동적 VLAN입니다. Cisco 스위치에서는 `show vlan` 또는 `show vlan brief` 명령어로 확인합니다."
            },
            {
                "number": 4,
                "type": "단답형",
                "question": "XSS 공격 시 자바스크립트(`document.cookie`)를 통한 쿠키 탈취는 방지하지만, 네트워크 도청에 의한 세션 하이재킹은 방지하지 못하는 Set-Cookie 헤더의 보안 속성은 무엇인가?",
                "extra": "",
                "answer": "HttpOnly",
                "explanation": "HttpOnly 플래그는 클라이언트 스크립트에서 쿠키에 접근하는 것을 차단합니다. 네트워크 구간 암호화는 Secure 플래그가 담당합니다."
            },
            {
                "number": 5,
                "type": "단답형",
                "question": "HTTP 헤더 인젝션(HTTP Response Splitting) 공격 시 개행을 발생시키기 위해 사용되는 특수 제어 문자 두 가지의 명칭 또는 표기법을 쓰시오.",
                "extra": "",
                "answer": "CR(Carriage Return, \\r, %0D), LF(Line Feed, \\n, %0A)",
                "explanation": "CRLF 인젝션은 CRLF(%0D%0A) 문자를 헤더에 삽입하여 응답 본문을 조작하거나 악성 쿠키를 설정하는 공격입니다."
            },
            {
                "number": 6,
                "type": "단답형",
                "question": "록히드마틴(Lockheed Martin)사가 제안하여 APT 공격에 대응하기 위해 공격 단계를 7단계(정찰 -> 무기화 -> 전달 -> 취약점 악용 -> 설치 -> 명령 및 제어 -> 목적 달성)로 정의한 프레임워크는 무엇인가?",
                "extra": "",
                "answer": "사이버 킬 체인 (Cyber Kill Chain)",
                "explanation": "APT 공격의 진행 단계 중 한 단계라도 사전에 탐지·차단하면 전체 공격을 무력화할 수 있다는 방어 모델입니다."
            },
            {
                "number": 7,
                "type": "서술형",
                "question": "SYN Flooding 공격의 원리를 3-Way Handshake 관점에서 서술하고, 이에 대한 서버 측 대응 방안(커널 파라미터 및 방어 기법) 2가지를 기술하시오.",
                "extra": "",
                "answer": "원리: 공격자가 위조된 IP로 대량의 TCP SYN 패킷을 전송하여 서버가 SYN+ACK를 보내고 백로그 큐(Backlog Queue)에 Half-Open 상태로 대기하게 만들어 신규 연결을 고갈시킴.\n대응 방안: 1) SYN Cookie(syncookies=1) 활성화, 2) TCP 백로그 큐 크기 증가(tcp_max_syn_backlog), 3) SYN+ACK 재전송 횟수 단축(tcp_synack_retries).",
                "explanation": "리눅스에서는 sysctl net.ipv4.tcp_syncookies = 1 로 설정하여 백로그 큐가 꽉 차도 쿠키를 통해 연결을 유지할 수 있습니다."
            },
            {
                "number": 8,
                "type": "서술형",
                "question": "리눅스 파일의 SetUID, SetGID, Sticky Bit의 개념과 8진수 표기법, 그리고 SetUID가 설정된 파일의 보안상 위험성을 서술하시오.",
                "extra": "",
                "answer": "개념: SetUID(4000)는 실행 시 파일 소유자 권한으로 실행, SetGID(2000)는 그룹 권한으로 실행, Sticky Bit(1000)는 모든 사용자가 쓰기 가능하나 파일 소유자만 삭제 가능(/tmp).\n위험성: root 소유 파일에 SetUID가 설정되어 있을 경우, 버퍼 오버플로우나 쉘 탈출 취약점이 존재하면 일반 사용자가 손쉽게 root 권한을 획득(권한 상승)할 수 있음.",
                "explanation": "find / -perm -4000 명령어로 시스템 내 취약한 SetUID 파일을 주기적으로 점검해야 합니다."
            },
            {
                "number": 9,
                "type": "실무형",
                "question": "리눅스 iptables를 이용하여 다음 조건의 방화벽 룰을 설정하는 명령어를 작성하시오.\n1) 기본 수신(INPUT) 정책을 DROP으로 설정\n2) 22번 포트(SSH)는 192.168.1.0/24 대역에서만 허용\n3) 80, 443번 포트(웹)는 모든 대역에서 허용\n4) 이미 맺어진 세션(ESTABLISHED, RELATED)은 허용",
                "extra": "",
                "answer": "1) iptables -P INPUT DROP\n2) iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT\n3) iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT\n4) iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
                "explanation": "상태 추적(stateful inspection) 방화벽 설정의 기본 템플릿입니다."
            },
            {
                "number": 10,
                "type": "실무형",
                "question": "Snort 침입 탐지 시스템(IDS)에서 외부 네트워크($EXTERNAL_NET)에서 내부 웹서버($HTTP_SERVERS 80)로 /etc/passwd 문자열을 요청하는 웹 디렉터리 접근 시도를 탐지하여 alert을 발생시키는 룰을 작성하시오. (sid: 1000001, rev: 1)",
                "extra": "",
                "answer": "alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:\"WEB-ATTACK /etc/passwd access attempt\"; content:\"/etc/passwd\"; nocase; sid:1000001; rev:1;)",
                "explanation": "Snort 룰 헤더와 옵션부(msg, content, nocase, sid, rev)의 구문 형식을 정확히 작성해야 합니다."
            }
        ]
    },
    2: {
        "round": 2,
        "name": "정보보안기사 실기 제2회 기출복원",
        "questions": [
            {
                "number": 1,
                "type": "단답형",
                "question": "리눅스 PAM(Pluggable Authentication Module)의 모듈 인터페이스 유형 4가지 중 다음에 해당하는 것을 각각 기술하시오.\n(A) 패스워드 등 인증 정보를 입력받아 신원을 확인하는 모듈\n(B) 계정의 유효 기간, 접근 시간, 비밀번호 만료 등을 검사하는 모듈\n(C) 로그인 전후 사용자 환경 설정 및 마운트 작업을 수행하는 모듈",
                "extra": "",
                "answer": "(A) auth, (B) account, (C) session",
                "explanation": "PAM 4가지 모듈 타입: auth(인증), account(계정 유효성), password(비밀번호 갱신), session(세션 개설/종료)."
            },
            {
                "number": 2,
                "type": "단답형",
                "question": "Windows 운영체제의 대표적인 저널링 파일 시스템으로, 사용자별 파일/폴더 접근 권한 설정(ACL), 파일 암호화(EFS), 대용량 볼륨 지원을 제공하는 파일 시스템은 무엇인가?",
                "extra": "",
                "answer": "NTFS (New Technology File System)",
                "explanation": "FAT32와 달리 NTFS는 보안 권한 설정 및 트랜잭션 저널링을 지원합니다."
            },
            {
                "number": 3,
                "type": "단답형",
                "question": "메시지 발신자부터 수신자까지의 통신 경로에서 중간 서버나 중계자가 평문 데이터에 접근할 수 없도록 양 끝단에서만 암호화 및 복호화를 수행하는 방식을 무엇이라 하는가?",
                "extra": "",
                "answer": "종단 간 암호화 (E2EE, End-to-End Encryption)",
                "explanation": "TLS 구간 암호화와 달리 중간 프록시나 서비스 제공자 서버에서도 데이터를 열람할 수 없습니다."
            },
            {
                "number": 4,
                "type": "단답형",
                "question": "엔드포인트 에이전트와 네트워크 모니터링을 통해 기밀 문서가 USB, 이메일, 메신저 등을 통해 외부로 유출되는 것을 사전에 탐지하고 차단하는 정보보호 솔루션은 무엇인가?",
                "extra": "",
                "answer": "DLP (Data Loss Prevention, 정보유출방지)",
                "explanation": "중요 기밀 정보(개인정보, 소스코드 등)의 반출 경로를 감시 및 통제합니다."
            },
            {
                "number": 5,
                "type": "단답형",
                "question": "C 언어에서 버퍼 크기 검증 없이 메모리에 데이터를 복사하여 반환 주소(RET)를 변조할 수 있는 대표적인 취약점 명칭과, 이에 취약한 위험 함수 2가지를 기술하시오.",
                "extra": "",
                "answer": "취약점: 버퍼 오버플로우 (Buffer Overflow), 함수: strcpy, gets, sprintf 등",
                "explanation": "안전한 함수(strncpy, fgets, snprintf 등)를 사용하거나 스택 보호 기법(Canary, ASLR, DEP)을 적용해야 합니다."
            },
            {
                "number": 6,
                "type": "단답형",
                "question": "리눅스 시스템에서 계정의 암호화된 비밀번호와 만료일 등의 정보를 보관하며, root 권한(0640 또는 0600)으로만 열람 가능한 핵심 보안 설정 파일의 경로는 무엇인가?",
                "extra": "",
                "answer": "/etc/shadow",
                "explanation": "/etc/passwd에 패스워드 해시가 있던 보안 문제를 해결하기 위해 섀도 패스워드 시스템이 도입되었습니다."
            },
            {
                "number": 7,
                "type": "서술형",
                "question": "SQL Injection 공격의 기본 원리를 설명하고, 개발 단계에서 이를 원천 차단하기 위한 PreparedStatement(파라미터화된 쿼리)의 방어 원리를 서술하시오.",
                "extra": "",
                "answer": "원리: 사용자 입력값을 검증 없이 동적 SQL 쿼리 문자열에 연결(Concatenation)할 때, 공격자가 입력한 따옴표(')나 SQL 연산자(OR 1=1 등)가 쿼리 문법으로 해석되어 실행됨.\n방어 원리: PreparedStatement는 쿼리 구문 구조를 데이터베이스 엔진에 사전 컴파일(Pre-compile)한 뒤, 사용자 입력값을 단순한 리터럴 데이터(바인딩 변수)로만 취급하므로 입력값에 SQL 문법 요소가 포함되어도 코드로 해석되지 않고 텍스트로 안전하게 처리됨.",
                "explanation": "시큐어 코딩의 가장 핵심적인 조치 항목입니다."
            },
            {
                "number": 8,
                "type": "실무형",
                "question": "아파치 웹서버(httpd.conf) 설정에서 디렉터리 리스팅 취약점을 제거하고, 서버 버전 정보 노출을 최소화하기 위한 설정 지시자 2가지를 작성하시오.",
                "extra": "",
                "answer": "1) 디렉터리 리스팅 방지: Options -Indexes\n2) 서버 정보 노출 차단: ServerTokens Prod, ServerSignature Off",
                "explanation": "정보 수집(Reconnaissance) 공격을 차단하는 웹서버 보안 조치입니다."
            }
        ]
    },
    18: {
        "round": 18,
        "name": "정보보안기사 실기 제18회 기출복원",
        "questions": [
            {
                "number": 1,
                "type": "단답형",
                "question": "802.11i 표준에 기반하며, 강력한 AES-CCMP 암호화 알고리즘과 802.1X/EAP 엔터프라이즈 인증을 지원하는 무선 랜 보안 프로토콜 규격은 무엇인가?",
                "extra": "",
                "answer": "WPA2 (Wi-Fi Protected Access 2)",
                "explanation": "WEP, WPA의 RC4/TKIP 취약점을 극복하기 위해 AES 기반 CCMP를 의무화한 표준입니다."
            },
            {
                "number": 2,
                "type": "단답형",
                "question": "VirusTotal에서 개발한 오픈소스 도구로, 텍스트나 바이너리 패턴, 정규표현식 등의 룰셋을 정의하여 의심스러운 악성코드 파일과 바이너리 시그니처를 식별하고 분류하는 패턴 매칭 도구는 무엇인가?",
                "extra": "",
                "answer": "YARA (야라)",
                "explanation": "악성코드 연구원과 보안 분석가가 악성코드 패밀리를 식별하고 분류하는 표준 도구입니다."
            },
            {
                "number": 3,
                "type": "단답형",
                "question": "소프트웨어 개발 보안(시큐어 코딩) 가이드에서 정의하는 7대 취약점 분야 중 '입력 데이터 검증 및 표현'에 해당하는 대표적인 웹 취약점 3가지를 쓰시오.",
                "extra": "",
                "answer": "SQL Injection, Cross-Site Scripting (XSS), OS Command Injection",
                "explanation": "외부 입력값을 검증 없이 사용할 때 발생하는 핵심 보안 취약점입니다."
            },
            {
                "number": 4,
                "type": "단답형",
                "question": "네트워크 스니핑 도구를 실행할 때, 자신에게 할당되지 않은 목적지 MAC 주소의 프레임까지 모두 수신하여 캡처할 수 있도록 설정하는 네트워크 인터페이스 카드(NIC)의 동작 모드는 무엇인가?",
                "extra": "",
                "answer": "무차별 모드 (Promiscuous Mode, 프러미스큐어스 모드)",
                "explanation": "스니퍼 탐지 도구들은 Promiscuous 모드로 활성화된 NIC를 식별하여 불법 패킷 캡처를 차단합니다."
            },
            {
                "number": 5,
                "type": "단답형",
                "question": "공격자가 TCP 헤더를 극도로 작은 크기로 쪼개어 단편화(Fragmentation)함으로써 첫 번째 패킷에 포트 번호 등 필터링 정보가 포함되지 않도록 방화벽 규칙을 우회하는 공격 기법은 무엇인가?",
                "extra": "",
                "answer": "Tiny Fragment 공격 (미세 단편화 공격)",
                "explanation": "TCP 헤더 크기보다 작은 단편을 방화벽이 제대로 검사하지 못하는 취약점을 악용합니다."
            },
            {
                "number": 6,
                "type": "서술형",
                "question": "IP Spoofing 공격의 개념과 방어 기법인 Ingress 필터링, Egress 필터링의 원리를 서술하시오.",
                "extra": "",
                "answer": "개념: 패킷의 출발지 IP 주소를 신뢰받는 호스트나 존재하지 않는 IP로 위조하여 침투하거나 DoS를 유발하는 기법.\nIngress 필터링: 외부에서 유입되는 패킷 중 내부 사설 IP 대역(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)이나 라우팅 불가능한 출발지 IP를 가진 패킷을 차단.\nEgress 필터링: 내부 네트워크에서 외부로 나가는 패킷 중 내부 할당 IP 대역이 아닌 출발지 IP를 가진 비정상 패킷을 차단.",
                "explanation": "경계 라우터에서 Ingress/Egress 필터링을 필수적으로 적용해야 합니다."
            },
            {
                "number": 7,
                "type": "실무형",
                "question": "리눅스 auditd 로그 분석 실무에서 파일 변경을 감시하기 위해 auditctl 명령어로 /etc/passwd 파일의 쓰기(w) 및 속성 변경(a)을 모니터링하고 키 이름을 'passwd_change'로 지정하는 감사 규칙 추가 명령어를 작성하시오.",
                "extra": "",
                "answer": "auditctl -w /etc/passwd -p wa -k passwd_change",
                "explanation": "auditctl -w (감시 경로) -p (권한 r,w,x,a) -k (키 태그) 구문입니다."
            }
        ]
    },
    19: {
        "round": 19,
        "name": "정보보안기사 실기 제19회 기출복원",
        "questions": [
            {
                "number": 1,
                "type": "단답형",
                "question": "위험 관리의 핵심 3대 구성 요소에 대한 설명이다. 빈칸에 들어갈 용어를 순서대로 기술하시오.\n(A) 조직이 보유하고 보호해야 할 가치 있는 유무형의 대상\n(B) 자산에 손실이나 피해를 발생시킬 잠재적인 원인이나 행위\n(C) 위협에 의해 취약해질 수 있는 자산 자체의 약점이나 결함",
                "extra": "",
                "answer": "(A) 자산 (Asset), (B) 위협 (Threat), (C) 취약점 (Vulnerability)",
                "explanation": "위험(Risk) = 자산(Asset) × 위협(Threat) × 취약점(Vulnerability)의 함수 관계로 분석됩니다."
            },
            {
                "number": 2,
                "type": "단답형",
                "question": "사용자 및 단말이 내부 네트워크에 접속할 때 무결성(보안 패치, 백신 설치 여부)과 사용자 인증을 검증하여 비인가 단말의 네트워크 접근을 통제하고 격리하는 보안 솔루션의 명칭과 영문 약어를 쓰시오.",
                "extra": "",
                "answer": "네트워크 접근 제어 (NAC, Network Access Control)",
                "explanation": "네트워크 진입 전 사전 무결성 점검과 사후 모니터링을 수행합니다."
            },
            {
                "number": 3,
                "type": "단답형",
                "question": "동일 서브넷 내에서 공격자가 자신의 MAC 주소를 게이트웨이나 희생자의 IP 주소와 매핑되도록 거짓 ARP Reply를 지속적으로 브로드캐스트하여 스니핑을 수행하는 2계층 중간자(MITM) 공격은 무엇인가?",
                "extra": "",
                "answer": "ARP Spoofing (ARP 스푸핑)",
                "explanation": "Static ARP 매핑 또는 Dynamic ARP Inspection (DAI) 스위치 기능을 통해 차단합니다."
            },
            {
                "number": 4,
                "type": "단답형",
                "question": "업무 연속성 계획(BCP) 수립 시 업무가 중단되었을 때 조직의 재무적·운영적 손실 규모를 정량적/정성적으로 분석하여 핵심 업무 프로세스의 복구 우선순위를 결정하는 분석 기법은 무엇인가?",
                "extra": "",
                "answer": "BIA (Business Impact Analysis, 업무영향도 분석)",
                "explanation": "BIA를 통해 목표 복구 시간(RTO)과 목표 복구 시점(RPO)을 산정합니다."
            },
            {
                "number": 5,
                "type": "서술형",
                "question": "침입탐지시스템(IDS)을 설치 위치 및 탐지 대상에 따라 NIDS(네트워크 기반)와 HIDS(호스트 기반)로 구분하고, 각각의 장단점을 2가지씩 비교 서술하시오.",
                "extra": "",
                "answer": "NIDS:\n- 장점: 네트워크 전체 트래픽 모니터링 가능, 개별 호스트 자원 소모 없음, 기존 시스템에 영향 없이 구축 용이.\n- 단점: 암호화된 트래픽(HTTPS 등) 탐지 불가, 기가비트 이상 고속 패킷 손실 가능성.\nHIDS:\n- 장점: 호스트 내부 파일 변경/명령어 실행 및 암호화 해제된 데이터 탐지 가능, 실제 공격 성공 여부 정확한 판별.\n- 단점: 각 호스트마다 에이전트 설치 필요, 호스트 성능 부하 발생, OS 종속적.",
                "explanation": "실무에서는 NIDS와 HIDS를 상호보완적으로 구축합니다."
            },
            {
                "number": 6,
                "type": "실무형",
                "question": "정량적 위험 분석 방법에서 다음 값을 계산하시오.\n- 자산 가치(AV): 10,000,000원\n- 노출 계수(EF): 0.5 (50%)\n- 연간 발생률(ARO): 2년에 1회 발생 (0.5)\n1) 단일 손실 예상액(SLE)을 구하시오.\n2) 연간 손실 예상액(ALE)을 구하시오.",
                "extra": "",
                "answer": "1) SLE = AV × EF = 10,000,000원 × 0.5 = 5,000,000원\n2) ALE = SLE × ARO = 5,000,000원 × 0.5 = 2,500,000원",
                "explanation": "정량적 위험 분석의 기본 공식 SLE = AV * EF, ALE = SLE * ARO 입니다."
            }
        ]
    }
}


def save_round(data):
    r_num = data["round"]
    folder = os.path.join(OUTPUT_DIR, f"{r_num:02d}회")
    os.makedirs(folder, exist_ok=True)

    # 1. JSON
    json_path = os.path.join(folder, "questions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "exam_name": data["name"],
            "round": r_num,
            "total_questions": len(data["questions"]),
            "questions": data["questions"]
        }, f, ensure_ascii=False, indent=2)

    # 2. Markdown
    md_path = os.path.join(folder, "기출복원_원문.md")
    md_lines = [
        f"# {data['name']}\n",
        f"* **시험 구분:** 국가기술자격 정보보안기사 실기",
        f"* **문항 수:** 총 {len(data['questions'])}문항",
        f"* **출처:** 수험생 커뮤니티 복원 데이터\n",
        "---\n"
    ]
    for q in data["questions"]:
        md_lines.append(f"### {q['number']}번 [{q['type']}]\n")
        md_lines.append(f"{q['question']}\n")
        if q["extra"]:
            md_lines.append("```text\n" + q["extra"] + "\n```\n")
        md_lines.append(f"> **정답:** {q['answer']}\n")
        if q["explanation"]:
            md_lines.append(f"> **해설:** {q['explanation']}\n")
        md_lines.append("\n---\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # 3. TXT
    txt_path = os.path.join(folder, "기출복원_원문.txt")
    txt_lines = [f"[{data['name']}]\n"]
    for q in data["questions"]:
        txt_lines.append(f"{q['number']}. [{q['type']}] {q['question']}")
        if q["extra"]:
            txt_lines.append(q["extra"])
        txt_lines.append(f"[정답] {q['answer']}")
        if q["explanation"]:
            txt_lines.append(f"[해설] {q['explanation']}")
        txt_lines.append("\n" + ("=" * 40) + "\n")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print(f"  [보완 완료] {r_num:02d}회: 총 {len(data['questions'])}문항 복원 저장됨")


def main():
    print("=" * 60)
    print(" 실기 누락 회차(1, 2, 18, 19회) 보완 에이전트 가동")
    print("=" * 60)
    for r_num, data in SUPPLEMENTAL_DATA.items():
        save_round(data)
    print("[*] 누락 회차 복원 완료!")


if __name__ == "__main__":
    main()
