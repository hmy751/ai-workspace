"""보존한 REA Evidence에 같은 조회를 적용하고 별도 폴더에 결과를 쓴다."""

import argparse
import gzip
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="query-executions.json에 보존한 질의 이름")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--cli",
        type=Path,
        default=Path("/tmp/rea-toast-tools/node_modules/rea-agents/scripts/rea.mjs"),
    )
    args = parser.parse_args()
    receipts = (
        Path(__file__).resolve().parents[2] / "receipts/rea-infinite-scroll-20261015"
    )
    output = args.output.resolve()
    if output == receipts or receipts in output.parents:
        parser.error("당시 receipts를 덮어쓰지 않도록 별도 출력 폴더를 사용하세요.")
    entries = json.loads((receipts / "query-executions.json").read_text())
    entry = next((item for item in entries if item["name"] == args.name), None)
    if entry is None:
        parser.error("알 수 없는 질의 이름")
    source = receipts / entry.get("input", "analysis.json.gz")
    if not source.exists():
        source = source.with_suffix(source.suffix + ".gz")
    data = (
        gzip.decompress(source.read_bytes())
        if source.suffix == ".gz"
        else source.read_bytes()
    )
    evidence = json.loads(data)
    selection = entry["selection"]
    request = (
        {"source": {"kind": "inline", "evidence": evidence}, **selection}
        if args.name == "summary"
        else {"application": evidence, **selection}
    )
    output.mkdir(parents=True, exist_ok=True)
    request_file = output / (args.name + "-request.json")
    request_file.write_text(json.dumps(request))
    command = [
        "node",
        str(args.cli),
        entry.get("verb", entry.get("command")),
        str(request_file),
        "--format",
        "json",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    result_file = output / (args.name + ".json")
    result_file.write_text(completed.stdout)
    (output / (args.name + ".stderr.txt")).write_text(completed.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    previous = (
        json.loads((receipts / (args.name + ".json")).read_text())
        if (receipts / (args.name + ".json")).exists()
        else json.loads(
            gzip.decompress((receipts / (args.name + ".json.gz")).read_bytes())
        )
    )
    current = json.loads(completed.stdout)
    print(
        json.dumps(
            {
                "output": str(result_file),
                "same_evidence_id": previous.get("evidence_id")
                == current.get("evidence_id")
                and current.get("evidence_id") is not None,
            }
        )
    )


if __name__ == "__main__":
    main()
