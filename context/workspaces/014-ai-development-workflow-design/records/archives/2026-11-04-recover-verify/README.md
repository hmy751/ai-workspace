# Recover·Verify 전환 전 보존본

2026-11-04, 기준 commit `f3d13f23ee838069d496fb7117175bc78e4a06d0`. 현재 Reference에서 제거한 실행기·기계 계약을 원래 의존 관계와 함께 복원하기 위한 역사 자료다. 현재 지침·설치 payload·일반 재개·test discovery에 사용하지 않는다.

- [before-retirement.tar.gz](before-retirement.tar.gz): 기준 commit의 `reference-project/` 전체와 당시 root 이식 스킬·AGENTS·README. Runtime만 옮기면 테스트의 상대 경로와 Workspace 의존이 깨지므로 전체 Reference를 보존했다.
- [보존 파일·해시](../../receipts/recovery-transition/2026-11-04-archive.json): 압축 사본 SHA-256과 활성 경로에서 내린 68개 파일의 원래 경로·SHA-256. Runtime 61개, 기계 계약 5개, runtime 전용 상위 package 표식 2개다.
- Archive SHA-256: `d6153f0cf7218b73ee34bfb218b217ebf3d2c3585707fd033f934215d00839b0`.

현재 운영본을 덮어쓰지 말고 별도 임시 폴더에 압축을 풀어 `reference-project/` 안에서 `python3 -B -m unittest discover -s . -p 'test_*.py' -v`를 실행한다. 이 사본의 스킬·지침은 당시 판본을 재현할 때만 적용하며 현재 workspace 지침에 설치하지 않는다. 같은 판본은 위 commit에서도 복원할 수 있다.

원래 Workspace의 날짜별 기록과 receipt 12개는 현재 Reference의 같은 위치에도 보존한다. 역사 기록의 옛 경로는 당시 구조를 뜻하며 archive 내부에서 대조한다. 실행기 제거 때문에 과거 본문·receipt를 새 결론에 맞춰 고치지 않았다. 현재 재개는 [Reference](../../../../../../reference-project/README.md)와 Workspace의 `recover.md`를 따른다.
