"""보존한 입력·질의를 별도 출력 폴더에서 다시 실행한다."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rea", default="/tmp/rea-toast-tools/node_modules/rea-agents/scripts/rea.mjs")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    experiment = Path(__file__).resolve().parent
    previous = experiment.parents[1] / "receipts/rea-toast-20261015"
    output = args.output or Path(tempfile.mkdtemp(prefix="rea-toast-replay-"))
    output.mkdir(parents=True, exist_ok=True)

    def run(name, verb, argument):
        destination = output / f"{name}.json"
        with destination.open("x") as stdout, (output / f"{name}.stderr.txt").open("x") as stderr:
            subprocess.run(
                ["node", args.rea, verb, str(argument), "--format", "json"],
                stdout=stdout, stderr=stderr, check=True, timeout=120,
            )
        return json.loads(destination.read_text())

    evidence = run("rea-analysis", "analyze-javascript-application", experiment / "input")
    for job in json.loads((previous / "query-executions.json").read_text()):
        selection = job["selection"]
        if job["verb"] == "inspect-analysis-view":
            payload = {"source": {"kind": "inline", "evidence": evidence}, **selection}
        else:
            payload = {"application": evidence, **selection}
        request = output / f"{job['name']}-request.json"
        request.write_text(json.dumps(payload))
        run(job["name"], job["verb"], request)
    print(output)


if __name__ == "__main__":
    main()
