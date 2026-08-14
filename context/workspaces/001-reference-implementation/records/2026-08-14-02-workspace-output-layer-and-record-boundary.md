# Workspace output 층과 records 경계

날짜: `2026-08-14`

## 작업 목적

실행 가능한 reference의 각 Workspace에 goal을 위해 선택된 현재 산출물의 진입점을 두고, 그 산출물을 만들고 고른 과정 기록과 분리한다. Recover는 다음 행동에 필요한 산출물 지도까지만 기본 context에 포함하고, 연결된 코드·문서·테스트 본문은 자동으로 읽지 않게 한다.

## 확정한 책임

- `output/index.md`는 모든 Workspace가 가져야 하는 최소 goal-output 지도다.
- 실제 산출물이 Project root의 코드·문서·테스트에 있으면 Workspace에 복제하지 않고 canonical 상대 경로를 연결한다. Workspace만 소유하는 goal 산출물은 `output/`에 직접 둘 수 있고, 선택된 산출물이 없으면 index에 그 사실을 명시한다.
- 분석 초안·후보 비교·탈락 사유·시행착오·선택 근거·교체된 이전 결과와 실행·검증 기록은 `records/`에 날짜별로 누적한다.
- 파일 형식이나 완성도가 아니라 Workspace goal에서 맡는 역할로 output과 records를 구분한다.
- Output 등재는 현재 선택 관계일 뿐 검증 통과, 사람의 acceptance, Workspace 완료를 뜻하지 않는다.

## 실제 reference 변경

- sample Workspace에 [`output/index.md`](../../../../reference-project/context/work/workspaces/001-default-timeout/output/index.md)를 추가하고 Project root의 [`src/config_loader.py`](../../../../reference-project/src/config_loader.py)를 canonical 산출물로 연결했다.
- 상위 context·Work context·Workspace collection·sample Workspace 진입점에서 `current/source/output/records`의 관계와 output–records 경계를 찾을 수 있게 했다.
- Recover는 Workspace output directory와 `output/index.md`가 없으면 실패하며 symlink를 거부한다.
- Recovery packet schema를 `4`에서 `5`로 올리고 `output.index`와 해당 loaded context path를 추가했다.
- Recover는 output index만 싣고, index가 연결한 제품 파일이나 같은 output 폴더의 다른 산출물 본문은 자동으로 읽지 않는다.
- repo-local `apply-context-harness` skill은 대상 Project에서도 실제 goal 산출물의 canonical 위치를 연결하고 과정 기록을 records에 남기도록 같은 적용·검증 경계를 반영했다.

## 검증

### 전체 reference 테스트

Project root인 `output/`에서 다음 명령을 실행했다.

```bash
python3 -B -m unittest discover -s . -p 'test_*.py' -v
```

총 35개가 통과했다.

- recover 책임 테스트: 19개
- verify 책임 테스트: 9개
- 제품 config loader 테스트: 7개

추가된 recover 테스트는 output index가 필수인지, packet schema `5`와 loaded path에 index가 들어오는지, symlink되거나 비정규 파일인 output index를 거부하는지, 연결된 artifact 본문은 읽지 않는지 확인한다.

repo-local application skill helper 테스트 7개도 통과했다. 기본 `python3`로 skill validator를 실행하면 환경에 PyYAML이 없어 `ModuleNotFoundError: No module named 'yaml'`로 시작하지 못했지만, PyYAML `6.0.3`이 설치된 Python `3.11.15`로 같은 validator를 실행한 결과는 `Skill is valid!`였다.

### 실제 reference 순환과 재복구

이번 변경에서 수행한 `recover → verify → recover`의 최종 product receipt와 machine status를 직접 대조했다.

- 최신 receipt: [`verify-20260814T033807136133Z-6688019152ce406bb6778a58a3417fc2.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/verify-20260814T033807136133Z-6688019152ce406bb6778a58a3417fc2.json)
- receipt result: `pass`
- 제품 unittest: 7개 통과
- machine status: 같은 receipt를 가리키는 `verified_waiting_acceptance`
- 완료 시각: `2026-08-14T03:38:07.135Z`

이어 `python3 -B -m context.work.harness recover --json`을 다시 실행했다. Packet schema는 `5`였고 `loaded_context_paths`에는 `workspaces/001-default-timeout/output/index.md`가 포함됐다. Index가 연결한 `src/config_loader.py`는 loaded context path에 없었고 해당 파일 내용도 packet에 실리지 않았다. Status가 연결한 receipt도 header 정합성만 확인하고 본문을 싣지 않았다.

## 현재 권위와 Git 상태

- 실제 reference 산출물의 현재 canonical은 루트 [`reference-project/`](../../../../reference-project/)다. 이 Workspace의 [`output/index.md`](../output/index.md)는 goal과 canonical 위치의 선택 관계만 소유한다.
- 이 기록은 `2026-08-14` 작업 트리의 실제 파일·테스트·receipt·post-recover 결과를 근거로 한다. 점검 시점에는 이번 output-layer 변경에 새 commit 기준점이 부여되지 않았다.
- Sample Workspace의 검증은 통과했지만 사람 acceptance는 아직 이뤄지지 않았다. 바깥 `001-reference-implementation` Workspace의 완료 상태와 sample Workspace의 `verified_waiting_acceptance`를 같은 lifecycle 상태로 해석하지 않는다.

## 검증 상한

- 이 검증은 한 reference Project에서 output 지도 존재·복구 경계와 제품 테스트 통과를 확인한다. 다른 실제 Project에서의 이식 가능성이나 운영 효과를 증명하지 않는다.
- Recover는 output index가 연결한 산출물의 존재·내용·의미 적합성을 검증하지 않는다. 필요한 artifact 본문을 읽고 acceptance를 판단하는 일은 별도 사람 또는 후속 작업의 책임이다.
- Workspace 생성·전환·완료·보관, Project canonical 반영, concurrent verify, receipt와 status의 단일 transaction은 여전히 구현하지 않았다.
