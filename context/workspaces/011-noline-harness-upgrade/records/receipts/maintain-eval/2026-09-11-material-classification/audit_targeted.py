"""Audit the narrowed third replay and its fresh reentry reader."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
SETUP = json.loads((OUT / "setup-v3.json").read_text())
PROJECT = Path(SETUP["project"])
PREFIX = "context/work/workspaces/" + SETUP["workspace_id"] + "/"
RUN = OUT / "run03"


def read(path):
    return json.loads(path.read_text())


def rollout(thread_id):
    matches = list(Path("/Users/hammyeong-yeon/.codex/sessions/2026/09/11").glob("*" + thread_id + ".jsonl"))
    assert len(matches) == 1, matches
    return matches[0]


def contexts(path):
    result = []
    for line in path.read_text().splitlines():
        event = json.loads(line)
        if event["type"] == "turn_context":
            payload = event["payload"]
            result.append({key: payload.get(key) for key in (
                "turn_id", "cwd", "model", "effort", "approval_policy", "sandbox_policy"
            )})
    return result


def main():
    initial = read(OUT / "fixture-manifest-v3.json")
    summary = read(RUN / "summary.json")
    rows = []
    for result in summary["results"]:
        phase = result["phase"]
        folder = RUN / phase
        before = read(folder / "before-hashes.json")
        after = read(folder / "after-hashes.json")
        decision = read(folder / "decision.json")
        actual = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
        declared = sorted(PREFIX + change["path"] for change in decision["changes"])
        assert actual == sorted(result["changed"])
        assert actual == declared
        for change in decision["changes"]:
            path = PREFIX + change["path"]
            assert before.get(path) == change["expected_sha256"]
            assert after[path] == hashlib.sha256(change["content"].encode()).hexdigest()
        rows.append({"phase": phase, "declared_matches_actual": True, "changed_paths": actual})

    final = read(RUN / "08-progression/after-hashes.json")
    changed = sorted(path for path in set(initial) | set(final) if initial.get(path) != final.get(path))
    assert changed == summary["all_changed_paths"]
    allowed_prefixes = (PREFIX + "current/", PREFIX + "records/")
    assert all(path.startswith(allowed_prefixes) for path in changed)
    live = {
        path.relative_to(PROJECT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in PROJECT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(PROJECT).parts
    }
    assert live == final

    current = PROJECT / PREFIX / "current"
    records = PROJECT / PREFIX / "records"
    current_text = "\n".join(path.read_text() for path in current.rglob("*.md"))
    records_text = "\n".join(path.read_text() for path in records.rglob("*.md"))
    assert "사용자는 2026-09-11 “그래 좋아" not in current_text
    assert "그래 좋아 그럼 이렇게 진행하는걸로" in records_text
    assert "/private/tmp" not in current_text

    maintainer_contexts = contexts(rollout(summary["thread_id"]))
    assert len(maintainer_contexts) == 4
    assert all(item["sandbox_policy"] == {"type": "read-only"} for item in maintainer_contexts)
    reentry_thread = json.loads((OUT / "reentry03/stdout.jsonl").read_text().splitlines()[0])["thread_id"]
    reentry_contexts = contexts(rollout(reentry_thread))
    assert len(reentry_contexts) == 1
    assert reentry_contexts[0]["sandbox_policy"] == {"type": "read-only"}

    value = {
        "phases": rows,
        "changed_paths": changed,
        "all_changes_current_or_records_markdown_only": True,
        "live_fixture_matches_final_guarded_state": True,
        "exact_adoption_utterance_absent_from_current": True,
        "exact_adoption_utterance_preserved_in_records": True,
        "temporary_absolute_path_absent_from_current": True,
        "state_utf8_bytes": {
            "before_adoption": (RUN / "before/current/state/index.md").stat().st_size,
            "after_progression": (RUN / "08-progression/current/state/index.md").stat().st_size,
        },
        "maintainer_turn_contexts": maintainer_contexts,
        "reentry_thread_id": reentry_thread,
        "reentry_turn_contexts": reentry_contexts,
    }
    (OUT / "audit-v3.json").write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value[key] for key in value if key not in (
        "phases", "maintainer_turn_contexts", "reentry_turn_contexts"
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
