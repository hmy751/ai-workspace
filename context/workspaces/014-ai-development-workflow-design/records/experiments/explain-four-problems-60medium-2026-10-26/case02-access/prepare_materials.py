"""보존된 원문에서 access 질문 직전의 읽기 전용 시험 자료를 구성한다."""

import hashlib
import json
import subprocess
from pathlib import Path

CASE = Path(__file__).resolve().parent
WORKSPACE = CASE.parents[3]
MATERIALS = CASE / "input" / "materials"
SOURCE = Path(
    "/Users/hammyeong-yeon/.codex/sessions/2026/09/29/"
    "rollout-2026-09-29T16-47-19-01a0ec21-e59e-7370-8432-8434271aa669.jsonl.zst"
)
EXPECTED_SOURCE_HASH = (
    "9f6df322184a78c975c2ff733cd383b1f4604a6e6a11b44a99b216949617037d"
)
SOURCE_PREFIX = "/Users/hammyeong-yeon/Desktop/10_work/noline/"
CORPUS = (
    WORKSPACE
    / "source/noline-evaluation/corpus/01a0ec21-e59e-7370-8432-8434271aa669/messages.jsonl"
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


source_bytes = subprocess.check_output(["zstd", "-dc", str(SOURCE)])
assert sha256(source_bytes) == EXPECTED_SOURCE_HASH
source_lines = source_bytes.splitlines(keepends=True)
events = [json.loads(line) for line in source_lines]
files = []


def item(number):
    assert number < 2757
    return events[number - 1]["payload"]["item"]


def output(number):
    current = item(number)
    assert current["type"] == "CommandExecution"
    assert current.get("exit_code") == 0
    return current["stdout"]


def added(number, path):
    change = item(number)["changes"][SOURCE_PREFIX + path]
    assert change["type"] == "add"
    return change["content"]


def save(relative, text, sources, method, original_path=None, **extra):
    data = text.encode("utf-8") if isinstance(text, str) else text
    path = MATERIALS / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    files.append(
        {
            "path": str(path.relative_to(CASE)),
            "bytes": len(data),
            "sha256": sha256(data),
            "source_lines": sources,
            "method": method,
            "original_path": original_path,
            **extra,
        }
    )


selected = []
records = []
for raw in CORPUS.read_bytes().splitlines(keepends=True):
    record = json.loads(raw)
    if 2267 <= record["source_line"] <= 2757:
        selected.append(raw)
        records.append(record)
assert records[0]["source_line"] == 2267
assert records[-1]["source_line"] == 2757
assert records[-1]["text"] == "근데 access 는 어디간거야?\n"
save(
    "messages.jsonl",
    b"".join(selected),
    [record["source_line"] for record in records],
    "corpus 레코드 원바이트를 범위로 선택",
)
conversation = "".join(
    f"[{record['role']} | {record['timestamp']} | source_line={record['source_line']}]\n"
    + record["text"]
    + "\n\n"
    for record in records
)
save(
    "conversation.txt",
    conversation,
    [record["source_line"] for record in records],
    "공개 발화 전문을 순서대로 보존하고 화자·시각·source_line 구분자만 추가",
)

read_path = "apps/client/src/features/trip/read-query/read-query.ts"
read_code = added(2714, read_path)
old_comment = (
    "成功した undefined や空配列も有効な結果。背景再取得の失敗で既存内容を隠さない。"
)
new_comment = "성공한 undefined나 빈 배열도 유효한 결과다. 재조회 실패로 기존 내용을 가리지 않는다."
assert read_code.count(old_comment) == 1
assert old_comment in item(2715)["command"][-1]
assert new_comment in item(2715)["command"][-1]
read_code = read_code.replace(old_comment, new_comment)
save(
    "code/" + read_path,
    read_code,
    [2714, 2715],
    "전체 추가 내용에 기록된 주석 치환만 적용; 원 명령 실행 없음",
    read_path,
    completeness="full-file",
)

index_path = "apps/client/src/features/trip/read-query/index.ts"
index_code = added(2714, index_path)
expense_import = "import { useGetTripExpenses } from '@/entities/expense';\n"
assert index_code.count(expense_import) == 1
index_code = index_code.replace(expense_import, "")
assert index_code.count("\nexport function useTripExpensesRead") == 1
index_code = index_code[: index_code.index("\nexport function useTripExpensesRead")]
assert "useTripExpensesRead" in item(2753)["command"][-1]
save(
    "code/" + index_path,
    index_code,
    [2714, 2753],
    "전체 추가 내용에서 기록된 경비 import 및 export 함수 제거만 적용",
    index_path,
    completeness="full-file",
)

screen_read_path = "apps/client/src/screens/read-query.ts"
save(
    "code/" + screen_read_path,
    added(2754, screen_read_path),
    [2754],
    "복구된 전체 추가 내용 원문",
    screen_read_path,
    completeness="full-file",
)

query_lines = output(2653).splitlines(keepends=True)
assert query_lines[0].startswith("import { useQuery }")
assert query_lines[28].startswith("import { useQuery }")
assert query_lines[55].strip() == "};"
for entity, name, start, end in [
    ("schedule", "useGetSchedules", 0, 28),
    ("expense", "useGetTripExpenses", 28, 56),
]:
    path = f"apps/client/src/entities/{entity}/data/{name}.ts"
    save(
        "code/" + path,
        "".join(query_lines[start:end]),
        [2653],
        f"연속 cat 출력에서 파일 경계로 분리: stdout {start + 1}~{end}행",
        path,
        completeness="full-file",
    )

policy_output = output(2722)
policy_start = policy_output.index("import { useMemo } from 'react';\n")
policy_end = policy_output.index(
    "import { useQuery } from '@tanstack/react-query';\n", policy_start
)
policy_code = policy_output[policy_start:policy_end]
assert output(2322).endswith(policy_code)
policy_path = "apps/client/src/shared/policy/useAppPolicy.ts"
save(
    "code/" + policy_path,
    policy_code,
    [2322, 2722],
    "연속 cat 출력에서 import 경계로 분리; 이전 전체 읽기와 동일함을 대조",
    policy_path,
    completeness="full-file",
)
type_output = output(2697)
type_start = type_output.index(
    "import type { NetworkStatus } from '@/shared/store/network';\n"
)
type_end = type_output.index("# Work context 운영 규칙\n", type_start)
types_code = type_output[type_start:type_end]
assert types_code.endswith(
    "export type ServicePolicyTable = Record<PolicyKey, ServicePolicy>;\n"
)
types_path = "apps/client/src/shared/policy/types.ts"
save(
    "code/" + types_path,
    types_code,
    [2697],
    "연속 출력에서 policy 타입 파일의 시작과 다음 파일 제목 경계로 분리",
    types_path,
    completeness="full-file",
)

diff_parts = output(2748).split("diff --git ")
schedule_diff = [
    part
    for part in diff_parts[1:]
    if part.startswith("a/apps/client/src/screens/ScheduleScreen.tsx ")
]
assert len(schedule_diff) == 1
save(
    "diffs/ScheduleScreen.diff",
    "diff --git " + schedule_diff[0],
    [2748],
    "당시 git diff에서 일정 화면 파일 부분만 원문 그대로 선택",
    "apps/client/src/screens/ScheduleScreen.tsx",
    completeness="diff-only",
)

consumer_lines = output(2498).splitlines(keepends=True)
assert len(consumer_lines) == 181
assert consumer_lines[73].strip() == "mode: 'onChange',"
assert consumer_lines[154].strip() == "/**"
for name, start, end, original_start, original_end, original_path in [
    (
        "ExpenseForm.lines20-92.tsx.txt",
        0,
        73,
        20,
        92,
        "apps/client/src/features/expense/create-expense/ExpenseForm.tsx",
    ),
    (
        "useCreateScheduleForm.lines30-110.ts.txt",
        73,
        154,
        30,
        110,
        "apps/client/src/features/schedule/create-schedule/useCreateScheduleForm.ts",
    ),
]:
    save(
        "excerpts/" + name,
        "".join(consumer_lines[start:end]),
        [2498],
        f"sed로 관측한 원 파일 {original_start}~{original_end}행을 원문 그대로 분리",
        original_path,
        completeness="excerpt-only",
    )

inventory = """# 제공 자료

`conversation.txt`는 마지막 질문까지의 공개 대화이며, `messages.jsonl`은 같은 발화의 원 레코드다.

| 위치 | 자료 범위 |
| --- | --- |
| `code/apps/client/src/features/trip/read-query/` | 마지막 질문 직전의 조합 훅 두 파일 전체 |
| `code/apps/client/src/screens/read-query.ts` | 같은 시점의 화면 공통 파일 전체 |
| `code/apps/client/src/entities/` | 일정·경비 데이터 조회 훅 전체 |
| `code/apps/client/src/shared/policy/` | 정책 선택 훅과 타입 파일 전체 |
| `diffs/ScheduleScreen.diff` | 일정 화면의 당시 변경 diff. 화면 전체 파일은 아니다. |
| `excerpts/ExpenseForm.lines20-92.tsx.txt` | 경비 작성 폼의 당시 20~92행 발췌 |
| `excerpts/useCreateScheduleForm.lines30-110.ts.txt` | 일정 작성 폼 훅의 당시 30~110행 발췌 |

코드 자료는 해당 시점의 관측 내용이다. 원본 저장소·앱 실행 환경 전체는 포함하지 않는다. 발췌는 완성된 파일이 아니며 diff 바깥의 화면 내용을 제공한 것으로 보지 않는다.
"""
save("README.md", inventory, [], "파일 구성과 자료 범위만 안내")

timeline = []
for number in range(2714, 2757):
    payload = events[number - 1].get("payload", {})
    current = payload.get("item", {})
    if current.get("type") == "CommandExecution":
        timeline.append(
            {
                "source_line": number,
                "command": current.get("command"),
                "exit_code": current.get("exit_code"),
                "source_line_sha256": sha256(source_lines[number - 1]),
            }
        )
    elif current.get("type") == "FileChange":
        timeline.append(
            {
                "source_line": number,
                "changes": list(current.get("changes", {})),
                "source_line_sha256": sha256(source_lines[number - 1]),
            }
        )
    assert "prettier" not in json.dumps(payload, ensure_ascii=False).lower()

used_lines = sorted({n for file in files for n in file["source_lines"]})
preparation = {
    "status": "prepared-for-read-only-response",
    "cutoff_source_line": 2757,
    "input_conversation": {
        "first_source_line": 2267,
        "last_source_line": 2757,
        "messages": len(records),
    },
    "source_file": str(SOURCE),
    "decompressed_source_sha256": sha256(source_bytes),
    "source_metadata_hash_match": True,
    "corpus_file": str(CORPUS.relative_to(WORKSPACE)),
    "selection_evidence": "records/receipts/case-selection/access-source-evidence-2026-10-26.json",
    "files": files,
    "source_line_sha256": {str(n): sha256(source_lines[n - 1]) for n in used_lines},
    "last_change_audit": {
        "reviewed_interval": [2714, 2756],
        "timeline": timeline,
        "read_query": "2714 전체 추가 → 2715 주석 치환. 이후2756까지 대상 변경 없음.",
        "index": "2714 전체 추가 → 2753 경비 import와 useTripExpensesRead 제거.",
        "screen_read_query": "2754에 기존 화면 공통 파일 전체 복구.",
        "schedule_screen": "2715 연결 변경 뒤2748 diff를 제공.2753은 다른 화면을 복구하고 ScheduleScreen은 변경하지 않음.",
        "formatting": "2714~2756 원 이벤트에서 formatter 실행을 찾지 못함. 준비 중 추가 정형화 없음.",
    },
    "limitations": [
        "전체 저장소·전체 화면·전체 폼·DB·앱 실행 환경을 복원하지 않았다.",
        "일정 화면은 당시 diff, 두 보조 소비자는 당시 발췌이며 전체 파일이 아니다.",
        "코드 판단에 필요한 관련 범위를 제공하며 라이브러리·Router·Policy 상수 전체는 포함하지 않는다.",
        "선택 판단용 읽기 자료 준비이며 동작·타입·제품 회귀 검증이나 모델 응답 시험은 하지 않았다.",
        "원래 shell/Python 명령은 실행하지 않고 명시된 텍스트 변환만 현재 준비 코드로 구현했다.",
    ],
    "excluded": [
        "source_line 2762 이후 발화",
        "인터뷰",
        "과거 시험 답·평가",
        "예상 답과 본 조사 판단",
    ],
}
(CASE / "preparation.json").write_text(
    json.dumps(preparation, ensure_ascii=False, indent=2) + "\n"
)
print(
    json.dumps(
        {
            "files": len(files),
            "messages": len(records),
            "material_directory": str(MATERIALS),
        },
        ensure_ascii=False,
    )
)
