# AI Company Hub

> 한국어 기반 AI 에이전트 회사 시뮬레이션. 뉴스페이퍼+스탠드업+사무실 모델, FIFO 큐 기반 에이전트 통신, 칸반보드, 정기 작업, 비용 추적을 지원합니다.

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

## 아키텍처

### 에이전트 통신 (Queue + Nudge)
서버가 에이전트를 직접 제어하지 않습니다. 가벼운 nudge만 보내고, 에이전트가 자율적으로 응답합니다.

```
사용자 채팅 → 서버가 큐 저장 + nudge (fire-and-forget)
           → 에이전트가 브리프/인박스/스탠드업 컨텍스트로 판단
           → 에이전트 응답 (stdout) → 서버가 파싱해서 채팅에 저장
           → 멘션이 있으면 대상 에이전트도 같은 방식으로 nudge
```

### FIFO 큐 + 중복 방지
- 같은 에이전트에 연속 요청 시 큐에 대기 (최대 3개)
- 처리 순서 보장 (FIFO)
- 바쁜 에이전트는 조용히 대기 (락 없음, 데드락 불가)

### 3단계 폴백
1. **1차**: 일반 호출 (120초 타임아웃)
2. **2차**: 2초 대기 후 재시도
3. **3차**: 세션 초기화 + 새 시도
4. **실패**: 사용자에게 채팅으로 알림

### 🗞️ 뉴스페이퍼 모델
에이전트 턴마다 자동 생성되는 브리프로 컨텍스트 최소화:
- 팀원 상태 (working/active)
- 작업 현황 (대기/진행중/오늘 완료)
- 승인 대기 항목
- 마스터의 최근 지시
- 최근 결과물
- 화이트보드 요약

### 📋 스탠드업 모델
에이전트가 자기 상황을 자발적으로 파일에 기록:
- 어제 한 것 / 지금 하는 것 / 필요한 것

### 🏢 사무실 모델
파일 기반 에이전트 간 소통:
- **inbox/**: @멘션 시 서버가 자동 생성, 응답 완료 후 자동 보관
- **outbox/**: 보낸 지시 기록
- **_shared/whiteboard.md**: 공용 아이디어 공간
- **_shared/deliverables/**: 팀 공유 결과물
- **_shared/newspaper.md**: 자동 생성 브리프

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
| 🗞️ **뉴스페이퍼** | 자동 브리프로 컨텍스트 관리 |
| 📋 **스탠드업** | 에이전트 자율 상태 보고 |
| 🏢 **사무실** | inbox/outbox/화이트보드 파일 기반 소통 |
| 🔔 **승인 관리** | 에이전트가 사용자 개입 요청 시 자동 감지 |
| 🛡️ **안전** | 원자적 JSON 쓰기, UTF-8 복구, 사용자 개입 감지 |

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

## 소통 방식

- **CEO**: 마스터가 일반 채팅을 보내면 자동 응답 (멘션 불필요)
- **팀원**: `@CMO 내용` 또는 `@CTO 내용` 형식으로 멘션 필요
- **에이전트 간**: CEO가 `@CMO`, `@CTO`로 지시, 팀원은 자유롭게 상호 멘션
- **인박스**: @멘션 시 서버가 자동으로 수신자 inbox에 기록

## 폴더 구조
```
ai-company-hub/
├── dashboard/
│   ├── server.py      # 메인 서버 (Python http.server)
│   └── index.html      # UI (싱글 HTML)
├── data/               # 회사별 데이터 (.gitignore)
│   └── {company-id}/
│       ├── _shared/
│       │   ├── newspaper.md      # 자동 생성 브리프
│       │   ├── whiteboard.md     # 공용 화이트보드
│       │   └── deliverables/     # 팀 공유 결과물
│       ├── workspaces/
│       │   └── {agent}/
│       │       ├── inbox/        # 받은 지시 (서버 자동 생성)
│       │       ├── inbox-done/   # 처리된 inbox (자동 보관)
│       │       ├── standup.md    # 스탠드업 (에이전트 작성)
│       │       ├── SOUL.md       # 에이전트 성격
│       │       ├── TOOLS.md      # 사용 가능한 명령어
│       │       └── memory/       # 에이전트 메모리
│       └── {company-id}.json
└── README.md
```

## API 엔드포인트

| 엔드포인트 | 설명 |
|---|---|
| `GET /api/companies` | 회사 목록 |
| `GET /api/company/{cid}` | 회사 상세 |
| `POST /api/chat/{cid}` | 사용자 채팅 전송 |
| `POST /api/agent-msg/{cid}` | 에이전트 메시지 전송 |
| `GET /api/newspaper/{cid}` | 브리프 조회 |
| `GET /api/inbox/{cid}/{agent_id}` | 인박스 조회 |
| `GET /api/board-tasks/{cid}` | 칸반 작업 목록 |
| `POST /api/board-task-add/{cid}` | 작업 추가 |
| `GET /api/approvals/{cid}?status=pending` | 승인 대기 목록 |
| `GET /api/deliverables/{cid}` | 결과물 목록 |
| `GET /api/costs/{cid}` | 비용 통계 |
| `GET /api/sse` | SSE 실시간 업데이트 |
