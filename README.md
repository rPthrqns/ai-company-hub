# AI Company Hub

> 한국어 기반 AI 에이전트 회사 시뮬레이션. 파일 기반 컨텍스트, COMPLEX 의사결정 프로토콜, 칸반보드, 정기 작업, 비용 추적을 지원합니다.

## 빠른 시작

```bash
git clone https://github.com/rPthrqns/ai-company-hub.git
cd ai-company-hub

# 서버 시작
python3 dashboard/server.py
# → http://localhost:3000
```

## 서버 관리

```bash
# 서버 시작 (백그라운드)
nohup python3 dashboard/server.py > /tmp/ai-company-server.log 2>&1 &

# 서버 재시작
fuser -k 3000/tcp; sleep 1; nohup python3 dashboard/server.py > /tmp/ai-company-server.log 2>&1 &

# 서버 상태 확인
curl -s http://localhost:3000/api/companies | python3 -m json.tool

# 로그 확인
tail -20 /tmp/ai-company-server.log
```

## 필요 사항
- Python 3.12+
- OpenClaw (에이전트 실행용)
- LLM API 키 (z.ai 등)

## 주요 기능

| 기능 | 설명 |
|---|---|
| 🏢 **다회사 관리** | 여러 회사 동시 운영 |
| 👥 **에이전트 조직** | CEO/CMO/CTO 등 자유 조직 구성 |
| 💬 **@멘션 소통** | `@CEO 내용` 형식의 에이전트 간 통신 |
| 📋 **칸반보드** | 자동 작업 추적 (대기→진행→완료) |
| 🔄 **정기 작업** | 에이전트가 `[CRON_ADD:...]`로 자동 스케줄링 |
| 📂 **결과물** | 에이전트가 파일로 작업 결과 저장, 클릭으로 열기 |
| 🧠 **메모리** | 에이전트별 일일 로그 + 장기 기억 |
| 💰 **비용 추적** | 에이전트별 토큰/비용 실시간 모니터링 |
| 🎯 **목표 관리** | 목표 설정 + 칸반 작업 연동 |

## 에이전트 명령

에이전트는 응답에 다음 명령을 포함하여 시스템을 제어할 수 있습니다:

### 칸반 작업
```
[TASK_ADD:작업명:우선순위(높음/보통/낮음)]
[TASK_START:작업명]
[TASK_DONE:작업명]
[TASK_BLOCK:작업명:사유]
```

### 정기 작업
```
[CRON_ADD:작업명:주기(분):프롬프트]
[CRON_DEL:작업명]
```

### 자동 감지
에이전트가 "~작성하겠습니다" → 칸반에 자동 추가 (진행)
에이전트가 "~완료했습니다" → 칸반에서 자동 완료 처리
멘션 수신 시 → 타겟 에이전트 칸반에 자동 대기 추가

## 소통 방식

- **CEO**: 마스터가 일반 채팅을 보내면 자동 응답 (멘션 불필요)
- **팀원**: `@CMO 내용` 또는 `@CTO 내용` 형식으로 멘션 필요
- **에이전트 간**: CEO가 `@CMO`, `@CTO`로 지시, 팀원은 자유롭게 상호 멘션
- **FROM → TO**: 멘션은 발신자→수신자 방향으로 시각화

## 폴더 구조
```
ai-company-hub/
├── dashboard/
│   ├── server.py      # 메인 서버 (Python http.server)
│   └── index.html      # UI (싱글 HTML)
├── data/               # 회사별 데이터 (.gitignore)
│   └── {company-id}/
│       ├── workspaces/
│       │   ├── {agent}/
│       │   │   ├── deliverables/   # 작업 결과물
│       │   │   └── memory/         # 에이전트 메모리
│       │   └── _shared/memory/     # 대화 요약
│       └── {company-id}.json
└── README.md
```


