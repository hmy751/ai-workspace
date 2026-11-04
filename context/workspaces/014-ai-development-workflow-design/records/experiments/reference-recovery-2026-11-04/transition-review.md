# Reference 재개·검증 전환 리뷰

2026-11-04. 기준 commit `f3d13f23ee838069d496fb7117175bc78e4a06d0` 대비 현재 미커밋 변경을 읽기 전용으로 검토했다. 검토 기준은 위임 brief의 사용자 승인 범위(Verify 아카이빙, Work 지침과 Workspace `recover.md`를 통한 재개, 기존 current의 의미 소유, 생성 시 초기화와 record-work의 조건부 유지, development의 직접 검증, 기존 증거 보존)다. 저장소 파일은 수정하지 않았다.

## Actionable findings

확인 범위에서 수정이 필요한 P1/P2/P3 회귀를 발견하지 못했다. 이 결론은 아래 정적·바이트 대조 범위에 한정하며 실제 host 실행 성공이나 장기 재개 효과를 뜻하지 않는다.

## 확인한 관계

- `reference-project/AGENTS.md`, `context/work/AGENTS.md`, Work/Workspace README와 `001-default-timeout/recover.md`: 일반 재개는 사용자 지정 우선·collection 기본값을 따르고, 한정 위임은 맡은 계약과 관련 자료부터 읽도록 구분된다. 안내가 없거나 불충분할 때 README/current/output과 원문으로 확장하는 경로가 있다.
- `reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md`, `create-context-workspace/SKILL.md`: 새 Work의 실제 목표·현재 의미를 만들고 `recover.md`로 기본·조건부 읽기를 연결한다. 생성만으로 기본 선택·수행 대상·host 상태를 바꾸지 않으며, 전환은 요청 범위에 연결된다.
- `record-work/SKILL.md`, `references/maintainer.md`, Work의 작성·갱신 기준: 안내 유지 권한과 변경 조건이 기록 책임에 연결되고, 상세 상태·판단은 current에 유지된다. raw source·과거 기록·제품 코드·기계 증거·다른 Work·기본 선택은 기록 수행의 기본 수정 범위에서 제외된다.
- `development/SKILL.md`, `references/verification/INDEX.md`, Reference README와 sample Workspace의 Spec/state/output: 직접 검사와 근거의 충분성·재사용 판단을 연결한다. 별도 Verify/기계 상태 생성을 완료 조건으로 재도입하지 않는다. 옛 receipt의 당시 결과와 현재 판본·사람 수락·Work 완료를 구별한다.
- 루트 `AGENTS.md`, `README.md`, `context/README.md`, `.agents/skills/apply-context-harness/{SKILL.md,references/application-contract.md,agents/openai.yaml}`: 신규 이식 payload에서 아카이브 runtime·machine 계약을 제외하고, 기존 대상 runtime은 실제 소비자·사용자 변경·승인 범위를 확인해 전환하도록 구분한다. 기존 Python Harness helper는 조건부 독립 도구로 남아 있고 새 설치 필수 조건은 아니다.

## 직접 확인한 근거

1. 루트 `CODE-QUALITY.md`와 Reference/Work의 적용 지침을 읽었다. `git diff f3d13f23`의 관련 변경과 현재 파일을 대조했다.
2. 활성 Reference 문서 및 root 이식 스킬의 Markdown 90개에서 local link 599개를 검사했고 존재하지 않는 목적지는 없었다. 별도로 관련 변경·신규 Markdown 48개에서 441개 local link를 검사했고 존재하지 않는 목적지는 없었다. 새 핵심 재개·생성·기록·검증 경로는 문구와 실제 목적지의 역할도 읽어 대조했다. 기계 검사는 heading anchor 전체의 의미나 모든 링크 본문을 검증한 것은 아니다.
3. 활성 Reference/이식 스킬에서 `context.work.harness`, `context/work/harness`, `recover.json`, `verify.json`, `workspace.json`, `status.json` 참조를 검색했다. 역사 기록·형성 자료를 제외한 남은 machine 파일 언급은 신규 설치에서 요구하지 않는다는 설명이며, Harness 경로의 코드 참조는 이식 helper가 자체 생성하는 테스트 fixture에 한정됐다. Reference 아래 끊어진 symlink는 발견하지 못했다.
4. 아래 manifest의 삭제 목록 68개와 실제 Reference 삭제 파일 집합이 일치했다. 각 파일의 기준 commit bytes, archive bytes, manifest SHA-256을 대조했고 불일치가 없었다.
   - `context/workspaces/014-ai-development-workflow-design/records/receipts/recovery-transition/2026-11-04-archive.json`
   - `context/workspaces/014-ai-development-workflow-design/records/archives/2026-11-04-recover-verify/before-retirement.tar.gz`
5. Archive SHA-256은 `d6153f0cf7218b73ee34bfb218b217ebf3d2c3585707fd033f934215d00839b0`로 현재 README·manifest와 일치했다. 기준 commit의 Reference tracked entry 335개(일반 파일·symlink)를 archive와 대조했고 bytes/링크 대상 불일치가 없었다. Manifest 이동 뒤 README 링크와 manifest의 archive 상대 경로도 새 위치에서 확인했다.
6. 기존 sample Work의 Verify receipt 12개와 날짜별 record 5개는 기준 commit과 바이트가 같았다. README/index의 역사·현재 역할 설명 변화와 과거 본문 보존을 구별해 확인했다.

## 한계

- 제품 테스트와 archive 복원 테스트는 이 리뷰에서 실행하지 않았다. 전환 기록의 95개/7개 통과 진술을 독립 실행 결과로 보고하지 않는다.
- 실제 Codex/Claude의 skill 발견·기록 담당자 재사용·다음 세션 재개 성공, 신규 외부 Project 이식은 확인하지 않았다.
- 전체 역사 Workspace나 다른 Desktop Project를 조사하지 않았다. Workspace 015의 내용 파일은 열지 않았으며 그 변경은 리뷰 범위에서 제외했다.
- 검토 중 main이 archive manifest를 `records/receipts/recovery-transition/`으로 이동했다. 마지막 확인은 이동 뒤 경로를 사용했다. 이후 main이 추가하는 Workspace 기록·최종 상태 갱신은 별도 최종 대조 대상이다.
