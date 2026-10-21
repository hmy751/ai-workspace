# Vercel 제품 설계 원문 읽기 안내

John Phamous의 **Teaching agents product design at Vercel**은 제품 판단 기준을 작업에 연결하는 skill, 명확한 규칙을 검사하는 lint, 근거를 수집해 기준 갱신을 검토하는 절차를 설명한다. 이번에는 [기존 원문](<../../lectures/vercel-product-design (1).md>)을 그대로 사용한다. 내부 `product-design` 전체 구현을 보존한 묶음은 아니다.

## 구현과 검토·수정에서 읽을 부분

아래 행 번호는 기존 원문 파일 기준이다. SKILL 예시의 일부 표제는 코드 블록 안에 있으므로 독립 Markdown 절 링크 대신 표제와 행을 함께 안내한다.

| 필요한 내용 | 원문에서 찾을 위치 |
| --- | --- |
| 구현·검토·정해진 방향의 보완 요청을 구별 | `Request Modes`, 112행. Shape·Implement·Review·Copy·Harden은 요청에 따른 모드다. |
| 사용자 목적·제품 사실·기존 결정과 코드의 관계 | `Decision Authority`, 128행; `Load product context`·`Model the product decision`, 145~152행 |
| 변경 대상에 필요한 기준을 선택 | `How the skill routes`, 64행; `Load the routed references`, 157행 |
| 선택 이유를 정리하고 구현 | `Decide, then implement`, 168행 |
| 구현·수정 결과를 실제 상태에서 확인 | `Verify`, 172행 |
| 검토 결과의 위치·근거·영향·수정 제안 | `Review Output`, 199행. Review는 별도 요청 없는 편집을 금지하고, Harden은 정해진 제품 방향 안에서 수정한다. |
| 작업의 결과와 지속 기준 갱신을 구별 | `Skill Integrity`, 210행; `Keep the guidance current`, 335행 |
| 기계 검사와 맥락 판단의 구별 | `Use linters for faster feedback`, 239행 |
| 기준을 읽는 것과 실제 적용의 평가 | `How we test the guidance with evals`, 325행. 명시된 `copywriting-eval`은 문구·인터페이스 언어 범위이며 전체 product-design workflow 평가로 확대하지 않는다. |

## 출처와 확보 범위

- 공식 주소: [Vercel 원문](https://vercel.com/blog/teaching-agents-product-design-at-vercel)
- 저자·게시일: John Phamous, 2026-06-25. 기존 파일 머리말과 [2026-10-13 조사26](../../../records/2026-10-13-26-vercel-source-investigation.md)에 있다.
- 기존 사본 보존일: 2026-10-12. [evidence-manifest](../../evidence-manifest.json)가 원래 제공 파일 경로·크기·hash를 보존한다. 제공 파일의 10월 8일 수정 시각을 웹 수집일로 해석하지 않는다.
- 이번 2026-10-21 작업은 기존 사본의 무결성 확인과 읽기 경로 연결이다. 웹을 새로 수집하거나 현재 사이트 내용을 다시 대조하지 않았다. [연결 정보](provenance.json)에 기존 출처와 파일 hash를 남겼다.

원문에는 축약된 SKILL·폴더·lint 예시가 있다. `product-judgment.md`, `interface-quality.md`, `resilience.md`, 화면별 기준, exemplars 등 **실제 내부 reference 본문은 이 자료에 없다.** 전체 eval fixture·rubric·결과, collector/judge 실행 코드와 실제 승인 기록도 확보되지 않았다. 원문의 경로 예시를 이번 폴더의 실제 파일처럼 읽지 않는다.

과거 공개 저장소 대조와 그 한계는 조사26에, 우리 검토자 직접 수정 방향과의 비교는 [비교61](../../../records/2026-10-17-61-reference-comparison-for-format-design.md)에 있다. 해당 분석을 원문 저자의 계약과 구별한다. 현재 설계의 선택과 적용 판단은 [워크스페이스 상태](../../../current/state.md)에서 찾는다.
