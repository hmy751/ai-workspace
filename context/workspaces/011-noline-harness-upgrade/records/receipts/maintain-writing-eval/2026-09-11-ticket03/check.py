"""Read-only checks of the blind sample; no model calls or artifact repair."""
import hashlib
import json
from pathlib import Path
import re

RUN = Path(__file__).resolve().parent
manifest = json.loads((RUN / "manifest.json").read_text())
inputs = json.loads((RUN / "inputs.json").read_text())
decision = json.loads((RUN / "02-decision.json").read_text())
thread_id = json.loads((RUN / "thread.json").read_text())["thread_id"]
rollouts = list(Path("/Users/hammyeong-yeon/.codex/sessions/2026/09/11").glob(f"*{thread_id}.jsonl"))
assert len(rollouts) == 1
turns = []
tool_calls = []
user_messages = []
for line_no, line in enumerate(rollouts[0].read_text().splitlines(), 1):
    event = json.loads(line)
    payload = event.get("payload", {})
    if event.get("type") == "turn_context":
        turns.append({"raw_line": line_no, "model": payload.get("model"),
                      "effort": payload.get("effort"), "cwd": payload.get("cwd"),
                      "sandbox_policy": payload.get("sandbox_policy"),
                      "collaboration_mode": payload.get("collaboration_mode")})
    if event.get("type") == "response_item":
        if payload.get("type") in {"function_call", "custom_tool_call", "web_search_call", "computer_call"}:
            tool_calls.append({"raw_line": line_no, "type": payload["type"], "name": payload.get("name")})
        if payload.get("type") == "message" and payload.get("role") == "user":
            user_messages.append("\n".join(p.get("text", "") for p in payload.get("content", [])))

raw = Path(inputs["delta"]["transcript_provenance"]["raw_path"])
original = raw.read_text().splitlines()
message_checks = []
for message in inputs["delta"]["discussion_messages"]:
    source = json.loads(original[message["raw_line"]-1])["payload"]
    original_text = "\n".join(p["text"] for p in source["content"] if "text" in p)
    message_checks.append(message["text"] == original_text)

snapshots = json.loads((RUN / "source-snapshot.json").read_text())
writing = snapshots["context/work/workspaces/DOCUMENT-WRITING.md"]["content"]
prompt_checks = []
for prefix in ("01", "02"):
    prompt = (RUN / f"{prefix}-prompt.txt").read_text()
    prompt_checks.append({"call": prefix, "writing_contract_count": prompt.count(writing),
                          "prompt_present_in_actual_user_message": any(prompt in m for m in user_messages),
                          "sha256": hashlib.sha256(prompt.encode()).hexdigest()})

preimages = {d["path"]: d for d in inputs["bootstrap"]["context_documents"]}
changes = []
links = []
for change in decision["changes"]:
    expected = preimages.get(change["path"], {}).get("sha256")
    content = change["content"]
    changes.append({"path": change["path"], "allowed": change["path"] in inputs["delta"]["allowed_document_paths"],
        "preimage_matches": change["expected_sha256"] == expected,
        "preview_exact": (RUN / "preview" / change["path"]).read_text() == content,
        "eof_newline": content.endswith("\n"),
        "trailing_whitespace_lines": [i for i, line in enumerate(content.splitlines(), 1) if line.rstrip() != line],
        "lines": len(content.splitlines()), "characters": len(content)})
    for line_no, line in enumerate(content.splitlines(), 1):
        for target in re.findall(r"\]\(([^)]+)\)", line):
            if re.match(r"[a-zA-Z]+://|#", target):
                continue
            resolved = ((RUN / "preview" / change["path"]).parent / target).resolve()
            links.append({"source": change["path"], "line": line_no, "target": target,
                          "resolved": str(resolved), "exists": resolved.is_file()})

result = {"rollout": str(rollouts[0]), "thread_id": thread_id, "turn_contexts": turns,
          "terra_high_both_turns": len(turns) == 2 and all(t["model"] == "gpt-5.6-terra" and t["effort"] == "high" for t in turns),
          "tool_calls": tool_calls, "source_messages": len(message_checks), "all_source_text_exact": all(message_checks),
          "prompts": prompt_checks, "changes": changes, "local_links": links,
          "guard_applied": False,
          "isolation_limit": "재개 cwd는 parent 저장소였다. project_doc_max_bytes=0, shell/web 비활성, 고정 입력과 실제 도구 호출 0을 확인했다. OS 파일 읽기 격리를 시험한 것은 아니다."}
(RUN / "checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
