"""시험 입력 열람과 입력 무결성 확인을 기록한다. 접근 격리를 보장하지는 않는다."""

import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", nargs="?", const="")
    parser.add_argument("--search")
    parser.add_argument("--prefix", default="")
    parser.add_argument("--images", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("path", nargs="?")
    parser.add_argument("chunk", type=int, nargs="?", default=1)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    inventory = json.loads((root / "inventory.json").read_text())
    output = root / "output"
    output.mkdir(exist_ok=True)
    log = output / "read-events.jsonl"

    def record(event):
        event["time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with log.open("a") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")

    if args.images:
        print((root / "images.json").read_text())
        record({"kind": "image-list"})
        return
    if args.check:
        events = (
            [json.loads(line) for line in log.read_text().splitlines()]
            if log.exists()
            else []
        )
        seen = {
            (event["path"], event["chunk"])
            for event in events
            if event["kind"] == "read"
        }
        required = json.loads((root / "required.json").read_text())
        missing = [
            [path, chunk]
            for path in required
            for chunk in range(1, inventory[path]["chunks"] + 1)
            if (path, chunk) not in seen
        ]
        changed = [
            path
            for path, meta in inventory.items()
            if hashlib.sha256((root / "input" / path).read_bytes()).hexdigest()
            != meta["sha256"]
        ]
        opened = sorted({path for path, _ in seen})
        partial = {
            path: [
                chunk
                for chunk in range(1, inventory[path]["chunks"] + 1)
                if (path, chunk) not in seen
            ]
            for path in opened
        }
        result = {
            "complete": not missing and not changed,
            "missing_required": missing,
            "changed_inputs": changed,
            "opened_files": len(opened),
            "partially_read": {
                path: chunks for path, chunks in partial.items() if chunks
            },
        }
        (output / "read-check.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        )
        print(json.dumps(result, ensure_ascii=False))
        raise SystemExit(0 if result["complete"] else 1)
    if args.search:
        pattern = re.compile(args.search)
        matches = []
        total = 0
        for path in sorted(inventory):
            if not path.startswith(args.prefix):
                continue
            for number, line in enumerate(
                (root / "input" / path).read_text().splitlines(), 1
            ):
                if pattern.search(line):
                    total += 1
                    if len(matches) < 40:
                        matches.append(f"{path}:{number}: {line[:260]}")
        print("\n".join(matches))
        print(f"표시 {len(matches)}/{total} matches; refine prefix/pattern for more.")
        record(
            {
                "kind": "search",
                "pattern": args.search,
                "prefix": args.prefix,
                "matches": total,
                "returned": len(matches),
            }
        )
        return
    if args.list is not None or args.path is None:
        prefix = args.list or ""
        rows = [
            f"{path} | {meta['chunks']} chunks"
            for path, meta in sorted(inventory.items())
            if path.startswith(prefix)
        ]
        print("\n".join(rows[:80]))
        print(
            f"표시 {min(80, len(rows))}/{len(rows)} files; --list 경로접두어로 좁힌다."
        )
        return
    if args.path not in inventory:
        raise SystemExit("허용된 input 상대 경로만 읽을 수 있다.")
    meta = inventory[args.path]
    if not 1 <= args.chunk <= meta["chunks"]:
        raise SystemExit("조각 번호가 범위 밖이다.")
    text = (root / "input" / args.path).read_text()
    content = text[(args.chunk - 1) * 3000 : args.chunk * 3000]
    record(
        {
            "kind": "read",
            "path": args.path,
            "chunk": args.chunk,
            "sha256": hashlib.sha256(content.encode()).hexdigest(),
        }
    )
    print(f"BEGIN {args.path} chunk {args.chunk}/{meta['chunks']}")
    print(content)
    print(f"END {args.path} chunk {args.chunk}/{meta['chunks']}")


if __name__ == "__main__":
    main()
