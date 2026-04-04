#!/bin/bash

# Cron job runner for AI Company Hub queue processor
# 이 스크립트는 Gateway cron job에서 호출됩니다

cd /home/sra/.openclaw/workspace

# 큐 처리 스크립트 실행
./ai-company-queue-processor.sh

# 실행 결과 확인
if [ $? -eq 0 ]; then
    echo "AI Company Hub 큐 처리 완료 - $(date)"
    exit 0
else
    echo "AI Company Hub 큐 처리 실패 - $(date)"
    exit 1
fi