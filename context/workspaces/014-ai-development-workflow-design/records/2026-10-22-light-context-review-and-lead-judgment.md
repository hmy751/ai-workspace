# 검토자의 문서 입력을 줄이고 Main이 적용을 판단하는 후보

2026-10-22. [직전 입력안](2026-10-22-role-inputs-and-dynamic-context-proposal.md)에 대한 사용자 대안과 보존 레퍼런스 재대조다. 기존안은 구현자·검토자 모두 Spec·Project 본문을 읽고 Personal 입력을 달리하는 방식이었다. 사용자는 구현자가 정책을 반영한 결과를 만들고, 검토자는 세부 문서를 덜 읽은 일반 관점에서 판단하며, 전체 맥락을 아는 lead가 적용·폐기·논의를 정하는 안을 제시했다.

> 검토자는 이미 구현되어 있는게 코드가 정책이 어느정도 반영되어 있을거잖아?
> 토큰 효율 그리고 객관성 두가지를 생각하면 이 안도 괜찮을 수 있다 보거든?

사용자는 가능성을 제안하고 의견·유사 레퍼런스 조사를 요청했다. 다음 내용은 Main의 권고이며 운영 채택이나 효과 확인은 아니다. 구현 단계의 검토자와 이후 별도 검증자, 서브의 프론티어보다 한 단계 아래 모델·medium 방향은 이어받는다.

## 원문에서 확인한 유사점과 차이

- pstack [interrogate](../source/workflow-references/pstack/repository/skills/interrogate/SKILL.md)는 한 문단의 작업 의도, diff 또는 파일, 코드를 이해하는 데 필요한 주변 맥락과 일반 검토 기준을 제공한다. Personal·Project 정책 전체를 항상 전달하라는 계약은 확인되지 않는다. 그렇다고 정책 문서 읽기를 금지하거나 의도적으로 숨기라는 지침도 아니다.
- [reviewer prompt](../source/workflow-references/pstack/repository/skills/interrogate/references/reviewer-prompt.md)는 목적을 전제로 실행의 질을 검토하고 실제 코드·근거를 붙이게 한다. 발견 없음도 유효한 결과다. [rubric](../source/workflow-references/pstack/repository/skills/interrogate/references/rubric.md)은 호출부·피호출부·타입·주변 모듈을 직접 읽어 원인과 구조를 판단하게 한다.
- [lead judgment](../source/workflow-references/pstack/repository/skills/interrogate/references/lead-judgment.md)는 제한된 맥락 때문에 나온 오해, lead가 아는 제약과 충돌하는 제안, 선호 차이·과잉 추상화를 걸러내게 한다. 동시에 불편한 지적을 자동 기각하지 말고 실제 경로와 자신의 이해 공백을 확인하라고 한다. 사용자 구상의 가장 가까운 근거다.
- pstack의 [no-comments](../source/workflow-references/pstack/repository/skills/no-comments/SKILL.md)와 [Comment Sicko](../source/workflow-references/pstack/repository/agents/comment-sicko.md)는 특정 관점의 전문 역할에 범위·파일을 주고 호출자가 결과를 재심사하는 더 좁은 사례다. 전문 역할도 주변 코드와 필요시 how/why를 읽으며 주석 삭제 권한이 있어 일반 읽기 전용 검토와 같지는 않다.
- Matt [code-review](../source/workflow-references/matt-pocock/repository/skills/engineering/code-review/SKILL.md)는 Spec 담당에게 Spec을, Standards 담당에게 저장소 기준과 일반 smell 기준을 준다. 관점별 입력 분리는 참고할 수 있지만 정책을 덜 주는 검토를 직접 지지하는 예는 아니다.
- [Vercel 보존 글](<../source/lectures/vercel-product-design (1).md>)은 full Review에서도 제품 판단·관련 품질 기준을 읽는다. 제품 적합성까지 맡는 리뷰이며 이번 일반 코드 관점의 역할보다 넓다. 필요에 따른 선택은 참고하되 최소 문서 입력 방식의 직접 근거로 쓰지 않는다.

위 자료는 보존판에서 읽었으며 온라인 최신판이나 다른 Desktop 저장소로 범위를 넓히지 않았다. 같은 저장소에 있는 Cursor Team Kit의 deslop도 확인했지만 Lauren의 pstack 본문과 혼동하지 않는다.

## Main의 권고

이번 검토자의 목적에는 사용자 안을 우선 후보로 삼는 것이 타당하다. 앞선 제안은 검토자에게 요구·정책 대조까지 많이 맡겼다. 일반 코드 관점에서 대안·불필요한 복잡성·책임·호출·오류 관계를 다시 보고, Main이 제품·개인 기준과 종합하는 분업으로 좁힐 수 있다.

첫 입력 후보는 짧은 작업 목적, 검토 범위와 정확한 코드 상태, 실제 코드·사용처 접근점, 일반 검토 관점, 발견·대안·근거·전제를 반환할 책임이다. 공개 API 유지처럼 결론을 좌우하고 코드에서 알 수 없는 필수 제약은 짧게 포함한다. Personal 상세·기존 해법 사례·Project 정책 전체·Spec 전체·구현자의 긴 정당화는 기본 선제공하지 않는다. 적용되는 실제 실행 환경의 지침을 우회하거나 무시하라는 뜻은 아니다.

검토자는 주변 코드와 타입·사용처를 먼저 확인한다. 정책 의존 쟁점은 전제를 붙인 후보로 돌려주거나 그 쟁점의 정본만 추가 확인할 수 있다. 일반 코드 판단을 하기 전에 모든 정책을 다시 읽도록 요구하면 분업 목적이 사라진다. Main은 제안의 근거·전제와 실제 요구·정책을 대조해 적용·폐기·논의·필요한 추가 확인을 판단한다. 문서에 기존 선택이 있다는 사실만으로 타당한 개선 의견을 기각하지 않는다.

현재 코드에는 반영된 정책의 결과가 보이지만 빠진 요구·선택 이유·허용 범위까지 복원되지는 않는다. 따라서 이 검토 결과를 정책 준수나 요구 충족의 통과로 취급하지 않는다. 전체 대조의 책임은 Main과 후속 별도 검증자의 설계에서 명시한다.

문서 입력을 줄이면 기존 해법에 동조하는 압력을 줄일 가능성이 있다. 한편 일반적 선호·모델의 편향과 맥락 부족에 따른 오해가 남으므로 객관성 향상 자체는 미입증이다. 초기 읽기 토큰 감소도 총비용 절감을 보장하지 않는다. Main의 재조사·기각·재검토 비용과 실제 유효한 제안을 함께 보아야 한다. 비교 실험은 이번에 수행하지 않았다.

후속은 정책 문서 전체를 다시 넣는 대신 실제 짧은 의뢰문과 일반 관점 기준을 구성하는 논의다. 원칙 발췌를 검토자 필수 입력으로 둔 직전안은 비교 후보로 보존하며 자동 확정하지 않는다. 프로토타입·실행 스킬·모델 설정은 변경하지 않았다.
