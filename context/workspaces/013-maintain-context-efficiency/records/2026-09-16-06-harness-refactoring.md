# Recover·Verify·공통 Harness 리팩터링

날짜: 2026-09-16

## 요청과 범위

사용자가 Maintain에 적용한 기준을 Recover를 포함한 전체 Harness 내부 코드에도
적용하도록 요청했다. 기존에 후속으로 미뤘던 Recover·Verify 내부를 이번 범위에
포함한다. 기준은 루트 [CODE-QUALITY.md](../../../../CODE-QUALITY.md)가 소유한다.

현재 Source인 Reference Harness만 변경한다. 비용 구조 개선, 실제 hook 등록·활성화,
binding·runtime·모델 설정, active index, Noline 적용본, 전역 하네스, 원자료와
역사 snapshot은 변경하지 않는다. 후속 사용자 커밋 요청에 따라 이 리팩터링의
코드·테스트·구조 안내·검증 기록을 하나의 별도 커밋 단위로 묶는다.

## 책임과 구현

- Recover의 572줄 실행 파일을 계약·Context 로딩·연결 receipt 검사·packet 조립·출력으로
  나눴다. [Recover README](../../../../reference-project/context/work/harness/recover/README.md)가
  내부 관계와 코드·테스트 지도를 소유한다.
- Verify의 677줄 실행 파일을 계약·evidence 선확보·stream 수집·process 범위·명령 실행·
  저장·실행 조정으로 나눴다. [Verify README](../../../../reference-project/context/work/harness/verify/README.md)가
  실행 순서와 검증 위치를 소유한다.
- 공통 계약은 [workspace/](../../../../reference-project/context/work/harness/workspace/README.md)의
  값 검사·안전한 경로/읽기·identity 선택·status 인계로 나눴다. Recover·Verify 전용
  계약이나 실행물을 공통으로 옮기지 않는다.
- 기존 Recover·Verify의 `operation.py`와 공통 `workspace_contract.py`는 얇은
  공개 import 호환 경로다. 동일 객체 재노출을 직접 검사한다.
- CLI의 packet 출력·Maintain decision 읽기·Maintain routing을 작은 함수로 분리했다.
  argparse와 명령/옵션, JSON·텍스트 출력, 오류 exit `2` 계약은 보존한다.
- 설명용 주석·docstring을 한국어로 정리했다. Recover 텍스트의 영문 의미 단위에는
  바로 아래 번역 주석을 붙였다. 실제 전달 문자열에 번역을 섞지 않았다.

책임 분리와 제거 가능성 기준에 따라 Workspace 의미·Owner·제품 claim의 충분성은
기존 canonical에 남겼다. 프로세스 실행·자동화 장치를 교체해도 공통 identity·
status 계약과 지속 Context의 의미를 다시 만들 필요가 없다. 새 모델 판단이나
권한 배치, 자유로운 host/runner 조합 설정은 추가하지 않았다.

## 테스트 구조와 보강

기존 Recover·Verify 테스트 메서드 51개를 동작별 파일로 옮겼다. 공통 CLI 도움말
검사는 validation으로 이동했다. 50개 메서드는 AST가 같고, descendant fixture를
개선한 한 메서드도 assertion AST 목록과 개수는 동일하다. 누락·중복은 없다.
AST 비교는 이동 보장 확인이며 동작 품질 전체의 보증으로 사용하지 않는다.

추가한 38개 검사는 다음 경계를 보호한다.

- 공통 값·identity·status·실제 파일 읽기와 기존 import 호환: 15개
- Verify stream chunk·Unicode/문자 수·읽기 오류, process deadline과 비-POSIX fallback,
  시작 실패, snapshot/receipt/status 실패 순서, atomic/append-only 저장: 18개
- 공통 CLI의 stdin·파일 입력·오류 반환과 Recover/Verify 공개 경로 호환: 5개

최소 Project·Workspace fixture는 `testing.py`에 남긴다. 삭제·지연·대량 출력
시나리오는 Verify의 `tests/support.py`가 소유하고 각 묶음이 필요한 실행물만
선택한다. Maintain에서 이전 제외 flag를 제거했다. 임시 디렉터리는 `addCleanup`으로
등록해 setUp/assertion 실패에서도 회수한다. 새로운 테스트 도구는 추가하지 않았다.

## 시간 민감 descendant fixture

변경 전 전체 Python 3.14 실행에서는 141개가 모두 통과했다. 구조 변경 중
Python 3.11 전체 실행에서 기존 descendant timeout 검사 한 건이 재현됐고
단독 실행에서는 통과했다. 실패는 0.3초 deadline 안에 launcher가 PID 파일을
쓰지 못한 형태였다.

별도 임시 fixture에서 shell launcher 첫 실행 종료는 0.185초, 후속 실행은
0.010초와 0.011초였다. 첫 실행 지연의 OS 내부 원인은 확정하지 않았다.
이 관측과 PID 누락은 시작 지연이 group 종료 검사에 섞일 수 있다는 근거다.

새 executable shell 파일 대신 설치된 Python이 launcher 본문을 읽게 바꿨다.
같은 session의 일반 Python child를 만들고 leader는 정상 종료한다. Deadline
0.3초, 전체 경과 상한, leader exit `0`, timeout exit `124`, child 종료,
receipt·summary의 기존 assertion은 유지했다. Cleanup은 assertion 전에
등록한다. 제품 timeout 알고리즘과 제한값은 바꾸지 않았다.

수정된 검사는 Python 3.11에서 10회 연속 통과했다. 유한 반복 결과이므로
모든 OS·부하에서 시간 민감성이 사라졌다는 뜻은 아니다.

## 검증 결과

최종 실행:

- Python 3.14.3 전체 179개 통과
- Python 3.11.15 전체 179개 통과
- 이식 helper 테스트 7개 통과
- 저장소 전체 Black 대상 126개 검사 통과
- `git diff --check` 통과

Harness 검사 구성은 Recover 35개, Maintain 82개, Verify 33개, 공통 Workspace
15개, validation 7개다. 제품 검사 7개를 더하면 전체 179개다.

변경 전 Recover를 메모리에서 로딩해 미검증·과거 receipt·fresh·변경·누락의
5개 상태에서 새 구현과 packet 값 및 렌더 문자열의 동일성을 비교했다.
공통 계약과 Recover·Verify의 함수/클래스 47개는 docstring·경계 이름 변경을
제외한 AST가 동일하다. 조립 함수 2개와 불필요한 try/re-raise를 제거한
receipt 저장 함수는 별도 코드 검토와 직접 테스트로 확인했다.

실제 active Workspace에서 durable Verify를 실행하지 않았다. 자동 테스트는
임시 fixture만 사용한다. 실제 Codex·Claude hook lifecycle, 실제 다른 OS의
프로세스 종료, semantic replay·비용 개선과 Noline acceptance는 확인하지 않았다.

## 재현

Reference Project root에서 두 버전의 전체 검사를 실행했다.

```bash
python3 -B -m unittest discover -s . -p 'test_*.py'
/Users/hammyeong-yeon/.pyenv/versions/3.11.15/bin/python3.11 -B -m unittest discover -s . -p 'test_*.py'
```

저장소 root에서 helper와 포맷을 검사했다.

```bash
python3 -B -m unittest discover -s .agents/skills/apply-context-harness/scripts/tests -p 'test_*.py'
.venv/bin/python -m black --no-cache --workers 1 --check .
git diff --check
```
