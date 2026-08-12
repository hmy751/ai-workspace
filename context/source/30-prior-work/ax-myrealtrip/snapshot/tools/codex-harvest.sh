#!/bin/sh
# 훅 승인 전이나 훅 실패로 누락된 Codex 세션 로그를 복구한다.
#
# 정상 경로:
# - Codex 데스크톱 앱은 대화 원본을 ~/.codex/sessions/에 rollout jsonl로 남긴다
#   (메타의 originator = "Codex Desktop"). 신뢰 승인된 .codex/hooks.json의 Stop 훅이
#   매 turn 종료 시 tools/save_log.py를 실행해 logs/codex/에 자동 저장한다.
# - 이 스크립트는 자동 저장이 누락된 세션만 복구하는 비상용이다.
# - cwd가 이 레포인 세션만 가져온다 — 무관한 데스크톱 대화가 제출 로그에 섞이지 않게.
# - 원본 rollout은 절대 편집·삭제하지 않는다. 공식 스크립트로 대화 라인만 추려 저장한다.
# - 이미 존재하는 제출 로그는 절대 덮어쓰지 않는다.
#
# 사용법: 누락이 확인된 경우에만 레포 루트에서 ./tools/codex-harvest.sh
cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"
SESS="$HOME/.codex/sessions"
[ -d "$SESS" ] || { echo "세션 폴더 없음: $SESS"; exit 1; }

# cwd가 이 레포인 rollout만 선별
grep -rls --include='rollout-*.jsonl' "\"cwd\":\"$ROOT\"" "$SESS" 2>/dev/null | while read -r f; do
  sid=$(basename "$f" .jsonl | sed -E 's/^rollout-[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}-//')
  dest="$ROOT/logs/codex/$sid.jsonl"
  if [ -e "$dest" ]; then
    echo "  건너뜀(이미 저장됨): $sid"
    continue
  fi
  printf '{"transcript_path":"%s","cwd":"%s","session_id":"%s"}' "$f" "$ROOT" "$sid" \
    | python3 tools/save_log.py --tool codex
  echo "  복구: $sid"
done

echo "----"
if ls "$ROOT"/logs/codex/*.jsonl >/dev/null 2>&1; then
  echo "logs/codex 현재 상태:"
  ls -la "$ROOT/logs/codex"
else
  echo "cwd=$ROOT 인 Codex 세션을 못 찾았다."
  echo "앱에서 이 레포 폴더를 작업 폴더로 열었는지 확인해라."
  echo "(cwd가 다른 폴더면 원본은 $SESS 에 남아 있으니, 그 폴더를 레포로 열어 다시 하거나 수동 저장 가능)"
fi
