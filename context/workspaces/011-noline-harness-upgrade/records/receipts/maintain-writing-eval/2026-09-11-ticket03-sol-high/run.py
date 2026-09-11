"""The user-requested Sol high sample, reusing the unchanged comparison runner."""
import importlib.util
from pathlib import Path
import sys

RUN = Path(__file__).resolve().parent
RUNNER = RUN.parent / "2026-09-11-ticket03-model-comparison" / "run.py"
spec = importlib.util.spec_from_file_location("ticket03_comparison_runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

# Only this experiment's destination and candidate change. The source inputs,
# runtime, contracts, isolation options and checks remain the same.
runner.RUN = RUN
runner.CANDIDATES = {"sol-high": ("gpt-5.6-sol", "high")}

if __name__ == "__main__":
    {"prepare": runner.prepare, "run": runner.run, "check": runner.check}[sys.argv[1]]()
