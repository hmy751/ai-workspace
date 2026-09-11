"""Parallel blind samples; keep the prior prompt and vary only model/effort."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

RUN = Path(__file__).resolve().parent
BASE = RUN.parent / "2026-09-11-ticket03"
REPO = next(p for p in RUN.parents if (p / "reference-project").is_dir())
sys.path.insert(0, str(REPO / "reference-project"))
from context.work.harness.maintain.codex_session import CodexMaintainSession

CANDIDATES = {"terra-xhigh": ("gpt-5.6-terra", "xhigh"), "sol-medium": ("gpt-5.6-sol", "medium")}
INPUTS = json.loads((BASE / "inputs.json").read_text())
SNAPSHOT = json.loads((BASE / "source-snapshot.json").read_text())
WS_ID = INPUTS["bootstrap"]["workspace_id"]
WS_REL = Path("context/work/workspaces") / WS_ID
TARGET = Path("/Users/hammyeong-yeon/Desktop/10_work/noline") / WS_REL
ALLOWED = set(INPUTS["delta"]["allowed_document_paths"])


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare() -> None:
    if (RUN / "manifest.json").exists():
        raise RuntimeError("Do not overwrite an existing experiment")
    source_match = {name: sha(REPO / "reference-project" / name) == entry["sha256"] for name, entry in SNAPSHOT.items()}
    assert all(source_match.values()), "Source contract/runtime changed since baseline"
    candidates = {}
    for name, (model, effort) in CANDIDATES.items():
        folder = RUN / name
        folder.mkdir()
        project = Path(tempfile.mkdtemp(prefix=f"ticket03-{name}-"))
        for owner in INPUTS["bootstrap"]["context_documents"]:
            path = project / WS_REL / owner["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(owner["content"], encoding="utf-8")
            assert sha(path) == owner["sha256"]
        session = CodexMaintainSession(project, WS_ID)
        for prefix, prompt in [("01", session._grounding_prompt(INPUTS["bootstrap"])),
                              ("02", session._decision_prompt(INPUTS["delta"]))]:
            assert prompt == (BASE / f"{prefix}-prompt.txt").read_text(), "Prompt differs from baseline"
            (folder / f"{prefix}-prompt.txt").write_text(prompt, encoding="utf-8")
        candidates[name] = {"model": model, "effort": effort, "project_root": str(project)}
    save(RUN / "manifest.json", {"candidates": candidates, "baseline": str(BASE),
        "inputs_sha256": sha(BASE / "inputs.json"), "source_snapshot_sha256": sha(BASE / "source-snapshot.json"),
        "source_matches_baseline": source_match,
        "target_before": {p: sha(TARGET / p) for p in sorted(ALLOWED)},
        "method": "Fresh session per candidate, identical baseline user prompts, two parallel start/resume sequences, one draft each, no retry or repair, no Guard apply."})
    print(json.dumps(candidates, ensure_ascii=False), flush=True)


def candidate(name: str) -> dict:
    manifest = json.loads((RUN / "manifest.json").read_text())
    settings = manifest["candidates"][name]
    folder = RUN / name
    calls = 0

    def runner(command: list[str], **kwargs):
        nonlocal calls
        calls += 1
        prefix = f"{calls:02}"
        assert not (folder / f"{prefix}-command.json").exists(), "No retry of an attempted sample"
        effective = list(command)
        effective[effective.index("--model") + 1] = settings["model"]
        effort_indices = [i for i, arg in enumerate(effective) if arg.startswith("model_reasoning_effort=")]
        assert len(effort_indices) == 1
        effective[effort_indices[0]] = f'model_reasoning_effort={json.dumps(settings["effort"])}'
        isolation = ["--skip-git-repo-check", "-c", "project_doc_max_bytes=0",
                     "-c", "features.shell_tool=false", "-c", 'web_search="disabled"']
        effective = effective[:-1] + isolation + effective[-1:]
        assert kwargs["input"] == (folder / f"{prefix}-prompt.txt").read_text()
        save(folder / f"{prefix}-command.json", {"adapter_command": command, "effective_command": effective,
             "experiment_model_override": settings, "experiment_isolation_options": isolation})
        started = datetime.now(timezone.utc).isoformat()
        tic = time.monotonic()
        print(f"{name} {prefix}: start {started}", flush=True)
        result = subprocess.run(effective, **kwargs)
        (folder / f"{prefix}-events.jsonl").write_text(result.stdout, encoding="utf-8")
        (folder / f"{prefix}-stderr.txt").write_text(result.stderr, encoding="utf-8")
        save(folder / f"{prefix}-execution.json", {"returncode": result.returncode,
             "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
             "elapsed_seconds": time.monotonic() - tic})
        print(f"{name} {prefix}: done exit={result.returncode}", flush=True)
        return result

    session = CodexMaintainSession(Path(settings["project_root"]), WS_ID, runner=runner)
    try:
        grounding = session.start(INPUTS["bootstrap"], output_path=folder / "01-grounding.json")
        save(folder / "thread.json", {"thread_id": session.thread_id, "grounding_status": grounding["status"]})
        decision = session.resume(INPUTS["delta"], output_path=folder / "02-decision.json")
        for change in decision["changes"]:
            if change["path"] not in ALLOWED:
                continue
            path = folder / "preview" / change["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(change["content"], encoding="utf-8")
        return {"candidate": name, "thread_id": session.thread_id, "outcome": decision["outcome"],
                "paths": [c["path"] for c in decision["changes"]]}
    except Exception as exc:
        result = {"candidate": name, "thread_id": session.thread_id, "error": str(exc)}
        save(folder / "failure.json", result)
        return result


def run() -> None:
    if any((RUN / name / "01-command.json").exists() for name in CANDIDATES):
        raise RuntimeError("One run only; no implicit model retry")
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(candidate, name) for name in CANDIDATES]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
    manifest = json.loads((RUN / "manifest.json").read_text())
    after = {p: sha(TARGET / p) for p in sorted(ALLOWED)}
    save(RUN / "completion.json", {"results": results, "target_after": after,
         "target_unchanged": manifest["target_before"] == after, "guard_applied": False})


def check() -> None:
    manifest = json.loads((RUN / "manifest.json").read_text())
    results = {}
    for name, settings in manifest["candidates"].items():
        folder = RUN / name
        if (folder / "failure.json").exists():
            results[name] = json.loads((folder / "failure.json").read_text())
            continue
        thread_id = json.loads((folder / "thread.json").read_text())["thread_id"]
        paths = list(Path("/Users/hammyeong-yeon/.codex/sessions").glob(f"*/*/*/*{thread_id}.jsonl"))
        assert len(paths) == 1
        turns, tools, actual_prompts = [], [], []
        for i, line in enumerate(paths[0].read_text().splitlines(), 1):
            event = json.loads(line)
            p = event.get("payload", {})
            if event.get("type") == "turn_context":
                turns.append({"line": i, "model": p.get("model"), "effort": p.get("effort"),
                              "cwd": p.get("cwd"), "sandbox_policy": p.get("sandbox_policy")})
            if event.get("type") == "response_item":
                if p.get("type") in {"function_call", "custom_tool_call", "web_search_call", "computer_call"}:
                    tools.append({"line": i, "name": p.get("name"), "type": p["type"]})
                if p.get("type") == "message" and p.get("role") == "user":
                    actual_prompts.append("\n".join(c.get("text", "") for c in p.get("content", [])))
        call_results = []
        for prefix in ("01", "02"):
            prompt = (folder / f"{prefix}-prompt.txt").read_text()
            usage = [json.loads(line)["usage"] for line in (folder / f"{prefix}-events.jsonl").read_text().splitlines()
                     if json.loads(line).get("type") == "turn.completed"]
            assert len(usage) == 1
            u = usage[0]
            assert u.get("cache_write_input_tokens", 0) == 0, "Price cache writes separately if observed"
            rate_input, rate_cached, rate_output = (50, 5, 300) if name == "terra-xhigh" else (100, 10, 500)
            credits = ((u["input_tokens"]-u["cached_input_tokens"]) * rate_input + u["cached_input_tokens"] * rate_cached + u["output_tokens"] * rate_output) / 1_000_000
            call_results.append({"call": prefix, "usage": u, "standard_rate_credit_estimate": credits,
                "prompt_equals_baseline": prompt == (BASE / f"{prefix}-prompt.txt").read_text(),
                "actual_prompt_confirmed": any(prompt in p for p in actual_prompts),
                **json.loads((folder / f"{prefix}-execution.json").read_text())})
        decision = json.loads((folder / "02-decision.json").read_text())
        owners = {d["path"]: d for d in INPUTS["bootstrap"]["context_documents"]}
        checks, links = [], []
        for change in decision["changes"]:
            content = change["content"]
            preview = folder / "preview" / change["path"]
            checks.append({"path": change["path"], "allowed": change["path"] in ALLOWED,
                "preimage_matches": change["expected_sha256"] == owners.get(change["path"], {}).get("sha256"),
                "preview_exact": preview.exists() and preview.read_text() == content,
                "eof_newline": content.endswith("\n"), "lines": len(content.splitlines()), "characters": len(content),
                "trailing_whitespace_lines": [i for i, line in enumerate(content.splitlines(), 1) if line.rstrip() != line]})
            for i, line in enumerate(content.splitlines(), 1):
                for link in re.findall(r"\]\(([^)]+)\)", line):
                    if re.match(r"[A-Za-z]+://|#", link):
                        continue
                    target = (preview.parent / link.split("#", 1)[0]).resolve()
                    links.append({"source": change["path"], "line": i, "target": link, "exists": target.is_file()})
        results[name] = {"thread_id": thread_id, "rollout": str(paths[0]), "turn_contexts": turns,
            "model_effort_verified": len(turns) == 2 and all(t["model"] == settings["model"] and t["effort"] == settings["effort"] for t in turns),
            "tool_calls": tools, "calls": call_results, "changes": checks, "links": links,
            "total_standard_rate_credit_estimate": sum(c["standard_rate_credit_estimate"] for c in call_results),
            "outcome": decision["outcome"], "unresolved": decision["unresolved"]}
    results["source_still_matches_baseline"] = all(sha(REPO / "reference-project" / n) == e["sha256"] for n, e in SNAPSHOT.items())
    save(RUN / "checks.json", results)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "run": run, "check": check}[sys.argv[1]]()
