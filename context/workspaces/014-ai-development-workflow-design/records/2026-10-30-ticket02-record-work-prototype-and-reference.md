# Record Work를 prototype과 Reference에 적용

2026-10-30. 사용자는 `record-work` 이름과 필요 시 기록 담당자를 호출·재사용하는 방식을 선택하고 “프로토타입부터 수정하고 그 다음 레퍼런스에 적용하자”고 요청했다. Prototype 반영·연결 확인 후 Reference에 적용했다.02의 전체 Workspace 구성 비교나07의 실제 장기 사용 효과를 완료한 것은 아니다.

## 선택한 방식과 근거

- 기존 매 응답 자동 Maintain을 없애고, 원문에서 기록할 의미를 판단하고 직접 수정하는 서브를 필요할 때 호출한다. Main이 기록 내용을 먼저 선별하는 B 대신 사용자가 A를 선택했다.
- 같은 대화에서 서브를 바로 종료하지 않고 재사용한다. 직전 반영 이후 원문이 기본 입력이며 필요한 이전 대화·기존 문서·실제 결과를 탐색할 수 있다.
- 기본 수정 책임은 Work다. development의 전체 영향 판단, 사용자 요청의 improvement-loop, Personal·Project의 context-update 반영 책임을 유지한다. 같은 서브에게 다른 영역의 반영을 별도 배정할 수는 있지만 기록 권한으로 자동 확대하지 않는다.
- 기록의 내용·분량·중복·이유·원문·확인 기준은 기존 Workspace 지침을 적용한다. 새 스킬은 호출·입력·담당 재사용·직접 수정·반환을 소유한다.

최소 사용자 원문과 선택의 맥락은 [스킬 근거](prototypes/development-workflow/skills/record-work/_background/evidence.md), 목적·부담·권한 배치는 [형성 맥락](prototypes/development-workflow/skills/record-work/_background/context.md)에 보존했다. 기존 방식의 비용이 크다는 사용자 판단과 실제 토큰 비용 측정은 구별한다.

## Prototype 결과

[record-work](prototypes/development-workflow/skills/record-work/SKILL.md)는 Main의 호출·재사용과 공통 계약을, references/maintainer.md는 기록 담당자의 직접 수행을, references/conversation.md는 입력 구간을 소유한다. 형성 자료는 같은 스킬 가까이에 두었다.

Reference의 DOCUMENT-WRITING과 Spec/Ticket 상세를 prototype Work에 가져와 실제 읽을 수 있게 연결했다. 기존 내용 기준은 유지하고 자동 장치에 묶인 갱신 담당 연결만 새 방식으로 바꿨다. Work의 폴더 구성 자체를 확정·재편하거나 Work에 새 background 정책을 적용한 것은 아니다.

development·improvement-loop·work-discussion·context-update와 Work 지침·색인을 연결했다. 원문 접근의 공통 방법은 skills/shared/conversation-source.md로 옮겼으며 improvement-loop의 세션 전체 검토와 record-work의 증분 기록 범위는 각자 유지한다.

## Reference 적용과 제거 범위

Reference의 `.agents/skills/record-work`와 Claude/Codex 상대 연결을 설치했다. 기존 작성 기준·생성/전환·root/Work 진입·개발/개선/논의/재판단 흐름을 새 기록 방식에 맞췄다. 생성·전환은 실제 배정과 기본 Workspace 선택을 구별하고 옛 activation을 호출하지 않는다.

자동 Maintain의 전용 runtime·판단/반영 코드·schema·전용 검사와 Codex/Claude hook wrapper·admission 설정 등70개 파일을 제거했다. `.codex/hooks.json`은 빈 hook 집합, config.toml은 전용 agent 등록 없음으로 바꿨다. 공통 CLI에서 maintain 명령을 제거하고 제거된 명령이 거부되는 검사를 추가했다. Recover·Verify의 코드와 기계 계약·기존 증거는 유지한다. `.gitignore`의 옛 runtime 제외는 이미 존재할 수 있는 민감 원문을 우발적으로 추적하지 않도록 유지한다.

기존 guarded apply의 경로·schema·preimage 거부는 새 스킬이 제공하는 보장이 아니다. 직접 쓰는 담당자가 지침과 실제 host 권한 안에서 기록을 수행한다. 허용 범위와 병행 변경 확인·부분 실패 반환을 실행 본문에 남겼다.

이식 스킬의 옛 자동 Maintain 설치 안내도 live Reference의 record-work·원문 접근·서브 재사용·중복 실행 제거 확인으로 맞췄다. 이 두 문서는 보호된 `.agents` 경로여서 승인된 도구 실행으로 수정했다. 전역 하네스·다른 Desktop 저장소·실제 Noline은 변경하지 않았다.

## 직접 확인과 한계

- 변경 전 Reference Harness172개 검사 통과. 전환 뒤 제품·남은 Harness 전체95개 검사 통과. 삭제된 책임의 전용 검사 제거와 옛 CLI 거부 검사 추가 때문에 검사 수가 달라졌다.
- 기본 및 명시 `recover 001-default-timeout --json` 성공. 제품 source/test, Recover·Verify 코드와 Workspace의 JSON 계약·status·receipt·과거 기록은 변경 전 해시와 같다. 보호 대조88개 중 안내 변경3개를 제외한85개가 byte 단위로 같았다. Sample README·사람용 state와 공통 workspace README의 기록 담당 안내만 바뀌었다.
- Prototype 열람 화면을 재생성하고 원문/SHA·경로/앵커·스크립트 문법을 확인했다. Reference의 파일 링크·앵커, 새 skill frontmatter·빈 hook/config·두 상대 연결도 확인했다. 최종 prototype은 문서242개·코드5개, 내부 링크1375개·앵커322개에서 누락0개였다. Reference 파일 링크1296개·앵커261개도 누락0개였으며 Workspace 재진입/기록 링크756개를 확인했다.
- Skill Creator의 Python 검사기는 PyYAML 부재로 실행하지 못해 기존 Ruby YAML 파서로 필수 name/description을 확인했다. 새 의존성을 설치하지 않았다.
- 현재 Main 세션의 원문 파일과 metadata 식별자·cwd 일치를 확인했다. 실제 제품·Noline에서의 자동 발견, 전체 workflow와 장기 기록 비용·재개 효과는 아직 확인하지 않았다.

## 격리 적용 시험

새 기록 담당자에게 현재 설계 대화 원문과 임시 Workspace를 주어 실제 기록·후속 재호출을 확인한다. 실제 prototype·Reference 문서는 수정 대상에서 제외한다.

첫 시도는 입력 끝을 L1025로 지정했지만 원문 파일에 L1200까지 함께 들어 있었고, 담당자의 추출 실수로 이후 구간이 노출됐다. 파일 수정 전에 중단했으며 해당 시도는 구간 분리·독립 판단 증거에서 제외한다. 새 fixture에는 첫 호출의 끝까지만 제공하고 새 담당자로 재시작했다. 새 담당자의 두 호출 결과는 [격리 시험 자료](experiments/record-work-2026-10-30/README.md)에 원문·초기 문서·첫/후속 결과·시험 스킬 입력과 함께 보존했다. 첫 호출과 후속 호출에서 각각 사람용6개 문서를 직접 수정했고, 같은 담당자 재호출·입력 확장·기존 과정 기록 보존을 확인했다. 원문에 없는 실제 구현 완료를 기록하지 않았다. 담당자의 수정은 지정 임시 Workspace에만 있었으며 Main이 실제 파일 차이와 원문을 대조했다. 비용 절감·다른 host·장기 효과의 증명은 아니다.

검사 출력·제거 경로·보호 대조 해시는 [적용 확인 자료](receipts/record-work/2026-10-30-application.json)에 남겼다. 기존 제품 Verify receipt나 새 실행 보장 schema가 아니다.

## 남은 범위

02는 계속 진행 중이다. 실제 사용에서 내용·분량·중복을 판단하고 Work 전체 구성·생애주기 비교와 통합 수행을 이어간다. 이번 스킬 적용으로 전체02를 완료하지 않는다. Reference의 이번 변경은 Noline에 재적용하지 않았으며06-02의 기존 상태와 구별한다. Commit·push는 이번 적용 요청에 포함하지 않아 수행하지 않았다.
