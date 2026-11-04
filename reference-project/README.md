# Personal·Project·Work context reference

개발 Project에서 개인 판단 기준·제품 맥락·작업의 현재 의미를 구별해 읽고, 실제 결과와 선택 이유를 남겨 다음 작업으로 이어가는 실행 가능한 기준 Project다. 현재 재개는 Workspace의 `recover.md`를 읽고 필요한 본문을 선택하며, 검증은 제품의 직접 검사와 development의 근거 판단으로 수행한다.

| 영역 | 소유하는 내용 |
| --- | --- |
| [Personal](context/personal/README.md) | 개인 기준·적용 조건·협업 경험과 열린 후보 |
| [Project](context/project/README.md) | 제품의 지속 의미·현재 구조·작업 계약과 선택 이유 |
| [Work](context/work/README.md) | 작업별 목표·현재 상태·재개 안내·원자료·산출물 지도·기록 |
| [src](src/)와 [tests](tests/) | 실제 config loader와 제품 검사 |

## 시작점

- 현재 작업을 이어가려면 [Workspace 목록](context/work/workspaces/README.md)에서 대상을 고르고 해당 README의 `recover.md`를 읽는다. 사용자 지정이 기본 선택보다 우선한다.
- 재개 범위·기록의 공통 기준은 [Work AGENTS](context/work/AGENTS.md), 새 목표의 생성·전환은 [생성·전환 계약](context/work/workspaces/CREATE-AND-TRANSITION.md)이 소유한다.
- 구현·검토·검증은 [development](.agents/skills/development/SKILL.md), 필요할 때 원문에서 Work를 직접 갱신하는 일은 [record-work](.agents/skills/record-work/SKILL.md)를 사용한다. 같은 대화에서 기록 담당자를 재사용할 수 있다.
- Personal·Project의 선택·읽기는 [USAGE](context/USAGE.md), 허용된 반영은 [context-update](.agents/skills/context-update/SKILL.md)와 해당 Owner의 관리 계약을 따른다.
- 작업 논의·재판단·설명·경험 개선은 [스킬 색인](.agents/skills/README.md)에서 호출 조건을 찾는다. 작업 종료만으로 모든 스킬을 실행하지 않는다.

## 직접 실행한다

이 Project root(`reference-project/`)에서 제품 계약을 확인한다.

```bash
python3 -B -m unittest tests.test_config_loader -v
```

전체 제품 검사를 찾으려면 `python3 -B -m unittest discover -s tests -p 'test_*.py' -v`를 사용한다. 실행 명령·대상 판본·관찰 결과·한계 중 다음 판단에 필요한 근거는 Ticket·records에 남기며, 사람이 수락했는지와 Work가 완료됐는지는 별도로 판단한다. 원래 Workspace의 [현재 상태](context/work/workspaces/001-default-timeout/current/state/index.md)에서 확인 범위를 읽는다.

검사 도구가 실제로 지원하는 시간 제한·출력 수집 범위를 확인한다. 응답 대기 시간은 프로세스 강제 종료 시간과 다르며, 이전 Verify의 자식 프로세스 종료·자동 snapshot·receipt·freshness 계산이 모든 직접 검사에 남아 있다고 가정하지 않는다. 새 기계 상태나 Verify 단계를 생성·재개의 필수 조건으로 두지 않는다.

## 구조와 관리 책임

```text
.agents/skills/                  실행 스킬과 공통 자료
.claude/skills/, .codex/skills/  같은 스킬 원본으로 연결
AGENTS.md                      책임별 진입 라우터
src/, tests/                   제품과 직접 검사
context/
├── personal/                  개인 기준·경험
├── project/                   제품 의미·현재 구조·계약·결정
└── work/
    ├── AGENTS.md               재개·기록 기준
    └── workspaces/
        ├── README.md          목록·기본 Workspace 선택
        ├── CREATE-AND-TRANSITION.md
        ├── spec-and-tickets/  공통 작업 정의·갱신 기준
        └── 001-default-timeout/
            ├── README.md     정체성·범위·구성
            ├── recover.md    기본·조건부 읽기 안내
            ├── current/      memory의 Spec·Ticket·선택 맥락, state
            ├── source/       원자료·출처
            ├── output/       실제 산출물 지도
            └── records/      판단·실행 근거와 과거 receipt
```

Current에는 다음 작업에서 계속 필요한 이유·조건·확정과 미정을, records에는 선택·수정·실행 과정을 남긴다. 실제 코드나 Project 본문을 Workspace에 복제하지 않는다. `recover.md`는 현재 내용을 중복 관리하지 않고 읽을 대상·조건·이유를 연결한다. 기본 자료의 고정 수나 전체 문서 재독을 요구하지 않는다.

자동 Maintain은 제거했고 Recover·Verify 실행기와 기계 계약은 2026-11-04에 아카이빙했다. [전환 기록](context/work/workspaces/001-default-timeout/records/2026-11-04-recovery-guide-transition.md)에서 대체 관계와 복원 위치를 찾는다. `.codex`의 hook 집합은 비어 있으며 전용 Maintain agent는 등록하지 않는다. Archive를 현재 설치 payload나 검사 대상으로 연결하지 않는다.

## 보존된 이전 실행 증거

아래는 이전 Harness 판본에서 수행한 검증의 역사다. 당시 명령·경로·fresh 판정을 현재 실행 계약으로 사용하지 않는다. 현재 결과는 위 Workspace state와 최신 기록에서 확인한다.

reference 순환을 확인하기 위해 기본 timeout 구현을 의도적으로 `3000`으로 어긋나게 한 뒤 같은 검증으로 실패시키고, canonical 값 `5000`으로 고쳐 다시 검증했다.

- [실패 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260812T184154363967Z-68493bb4ec064a6d97b134737782dfe5.json): 제품 테스트 실패와 exit `1`
- [성공 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json): 같은 제품 테스트 통과와 exit `0`
- [goal output 지도](context/work/workspaces/001-default-timeout/output/index.md): 실제 제품 구현의 canonical 위치를 복제 없이 연결
- [검증 순환 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-01-default-timeout-verification-cycle.md)과 [current 폴더화 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-02-current-folder-migration.md): 당시 구현과 검증 범위
- [Harness 책임 경계 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-03-harness-responsibility-boundary-refactor.md): recover·verify 응집, 26개 테스트, 실제 새 CLI 재검증
- [책임 재구성 뒤 최종 성공 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json): 제품 테스트 7개 통과, exit `0`, 실행 전 evidence hash
- [Project·Work context 경계 이동 기록](context/work/workspaces/001-default-timeout/records/2026-08-13-04-project-work-context-boundary-migration.md): 두 root 분리, 29개 테스트, 새 위치의 실제 순환
- [경계 이동 뒤 성공 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json): Project root에서 제품 테스트 7개 통과, Work root에 결과 연결
- [Machine receipt 경계 기록](context/work/workspaces/001-default-timeout/records/2026-08-14-05-machine-receipt-boundary.md)과 [당시 nested receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json): 사람용 records와 종류별 기계 증거 분리, 이전 flat 경로 호환, 40개 테스트와 당시 실제 순환
- [책임 분리 뒤 제품 receipt](context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T103703075846Z-a1cde45907164974a19c22564a956127.json): claim, canonical basis 3개와 evidence 2개의 실행 전 snapshot, bounded runtime, 제품 테스트 7개 통과, schema `3` machine-only status와 explicit Recover의 `fresh` 재확인

## 증명 범위

지침·링크·스킬 설치와 직접 제품 검사는 실제 host의 스킬 발견·기록 담당자 재사용·원문 판단 품질·다음 세션의 재개 성공을 대신하지 않는다. 제한된 읽기 시험 결과와 장기 효과는 별도로 해석한다.

Record-work는 원문 해석과 직접 문서 갱신을 연결하는 실행 지침이다. 이전 guarded apply의 경로·preimage·schema 거부 보장을 그대로 제공하지 않으며 지침과 host 권한 안에서 수행한다. Project·Personal의 채택·갱신은 각 Owner에게 남는다. 기록 반영·제품 검증·사람의 수락·Work 완료와 운영 효과를 구별한다.
