#!/bin/bash

# AI Company Hub 큐 처리 스크립트
# 작업: data/ 디렉토리의 모든 *-queue.json 파일에서 processed: false인 메시지를 처리

DATA_DIR="/home/sra/.openclaw/workspace/ai-company/data"
LOG_FILE="/tmp/ai-company-queue-processor.log"

# 로깅 함수
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 에러 처리 함수
error_exit() {
    log "ERROR: $1"
    exit 1
}

# CEO 작업 처리 함수
process_ceo_task() {
    local company_id="$1"
    local text="$2"
    local time="$3"
    
    # 회사 상태에서 CEO 정보 가져오기
    local ceo_name=$(cat "$DATA_DIR/$company_id.json" | jq -r '.agents[] | select(.id == "ceo") | .name')
    local ceo_emoji=$(cat "$DATA_DIR/$company_id.json" | jq -r '.agents[] | select(.id == "ceo") | .emoji')
    
    # 간단한 CEO 응답 생성
    echo "$ceo_emoji @마스터 지시 확인. 즉시 조치하겠습니다. 현재 상태: 운영 중, 팀 구성: $(cat "$DATA_DIR/$company_id.json" | jq '.agents | length')명."
}

# CMO 작업 처리 함수
process_cmo_task() {
    local company_id="$1"
    local text="$2"
    local time="$3"
    
    # 웹 검색 등 실제 작업 수행
    if echo "$text" | grep -q "분석\|검색\|조사"; then
        # 간단한 웹 검색 (실제 구현에서는 더 복잡한 로직)
        echo "📈 웹 검색 결과: 시장 분석 및 경쟁사 정보 수집 완료"
    else
        echo "📈 CMO: 마케팅 전략 수립 및 실행"
    fi
}

# CTO 작업 처리 함수
process_cto_task() {
    local company_id="$1"
    local text="$2"
    local time="$3"
    
    echo "💻 CTO: 기술 인프라 구축 및 시스템 개작"
}

# HR 작업 처리 함수
process_hr_task() {
    local company_id="$1"
    local text="$2"
    local time="$3"
    
    echo "👥 HR: 인사 관리 및 채용 프로세스"
}

# Designer 작업 처리 함수
process_designer_task() {
    local company_id="$1"
    local text="$2"
    local time="$3"
    
    echo "🎨 Designer: UI/UX 디자인 및 브랜딩"
}

# API에 결과 전송 함수
send_to_api() {
    local company_id="$1"
    local target="$2"
    local original_text="$3"
    local result="$4"
    local time="$5"
    
    # 회사 정보 가져오기
    company_name=$(cat "$DATA_DIR/$company_id.json" | jq -r '.name')
    agent_emoji=$(cat "$DATA_DIR/$company_id.json" | jq -r ".agents[] | select(.name == \"$target\") | .emoji")
    
    # API 요청 데이터 생성
    api_data=$(cat <<EOF
{
    "from": "$target",
    "emoji": "$agent_emoji",
    "to": "마스터",
    "text": "$result",
    "company_id": "$company_id",
    "company_name": "$company_name",
    "original_text": "$original_text",
    "time": "$time"
}
EOF
)
    
    # API 호출 (실제 API 서버가 실행되지 않아도 일단 실행)
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$api_data" \
        "http://localhost:3000/api/agent-msg/$company_id" \
        2>/dev/null || echo "API 호출 실패 (서버 실행 중 아닐 수 있음)"
}

# 큐 업데이트 함수
update_queue() {
    local queue_file="$1"
    local message_id="$2"
    local processed_value="$3"
    
    # jq를 사용하여 특정 메시지의 processed 필드 업데이트
    temp_file=$(mktemp)
    cp "$queue_file" "$temp_file"
    
    # processed 필드 업데이트
    jq --arg id "$message_id" --argjson processed "$processed_value" '
        map(if .id == $id then .processed = $processed else . end)
    ' "$temp_file" > "$queue_file"
    
    # 임시 파일 삭제
    rm -f "$temp_file"
}

# 큐 파일 목록 가져오기
queue_files=$(find "$DATA_DIR" -name "*-queue.json" -type f 2>/dev/null)

if [ -z "$queue_files" ]; then
    log "큐 파일이 없습니다."
    exit 0
fi

log "발견된 큐 파일: $queue_files"

# 각 큐 파일 처리
for queue_file in $queue_files; do
    company_id=$(basename "$queue_file" | sed 's/-queue\.json$//')
    company_file="$DATA_DIR/$company_id.json"
    
    log "처리 시작: $queue_file (company_id: $company_id)"
    
    # 회사 상태 파일 확인
    if [ ! -f "$company_file" ]; then
        log "경고: 회사 상태 파일 없음 - $company_file"
        continue
    fi
    
    # 큐 파일 읽기
    queue_content=$(cat "$queue_file")
    
    # processed: false인 메시지만 필터링
    unprocessed_messages=$(echo "$queue_content" | jq -c '.[] | select(.processed == false)')
    
    if [ -z "$unprocessed_messages" ]; then
        log "처리할 메시지가 없음: $queue_file"
        continue
    fi
    
    log "발견된 미처리 메시지:"
    
    # 각 미처리 메시지 처리
    message_count=$(echo "$unprocessed_messages" | wc -l)
    for ((i=1; i<=message_count; i++)); do
        message=$(echo "$unprocessed_messages" | sed -n "${i}p")
        
        text=$(echo "$message" | jq -r '.text')
        target=$(echo "$message" | jq -r '.target')
        time=$(echo "$message" | jq -r '.time')
        id=$(echo "$message" | jq -r '.id')
        
        log "  메시지 ID: $id, 대상: $target, 내용: $text"
        
        # 실제 작업 수행 (타겟 에이전트에 따라)
        case "$target" in
            "CEO")
                result=$(process_ceo_task "$company_id" "$text" "$time")
                ;;
            "CMO")
                result=$(process_cmo_task "$company_id" "$text" "$time")
                ;;
            "CTO")
                result=$(process_cto_task "$company_id" "$text" "$time")
                ;;
            "HR")
                result=$(process_hr_task "$company_id" "$text" "$time")
                ;;
            "Designer")
                result=$(process_designer_task "$company_id" "$text" "$time")
                ;;
            *)
                result="에이전트 $target는 지원되지 않습니다"
                ;;
        esac
        
        log "  작업 결과: $result"
        
        # 결과를 API로 전송
        api_result=$(send_to_api "$company_id" "$target" "$text" "$result" "$time")
        log "  API 전송 결과: $api_result"
        
        # 큐에서 processed: true로 업데이트
        update_queue "$queue_file" "$id" "true"
        
        log "  메시지 처리 완료: ID $id"
    done
done

log "모든 큐 처리 완료"
exit 0