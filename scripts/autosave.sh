#!/bin/bash
# 대량 수집 중 15분마다 중간 저장(커밋·푸시). 수집이 끝나면 마지막으로 한 번 저장하고 종료.
cd "$(dirname "$0")/.."
save() {
  git add -A >/dev/null 2>&1
  git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -qm "대량 수집 중간 저장 $(date +%H:%M)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CC1BwstSU2Wmmi8NeXZ2RA" >/dev/null 2>&1 && git -c push.negotiate=true push -q >/dev/null 2>&1
}
while pgrep -f "fetch_datago.py 1" >/dev/null; do save; sleep 900; done
save
