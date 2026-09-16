import argparse
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fasd_costs.pipeline import run_pipeline


def git_value(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=30)
    args = parser.parse_args()
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    durations = []
    hashes = []
    summary = None
    for number in range(1, args.runs + 1):
        target = out / f"run-{number:03d}"
        if target.exists():
            shutil.rmtree(target)
        started = time.perf_counter()
        summary, metadata = run_pipeline(target)
        durations.append(time.perf_counter() - started)
        hashes.append((metadata["records_sha256"], metadata["summary_sha256"]))
    report = {
        "runs": args.runs,
        "successful_runs": len(durations),
        "identical_output_hashes": len(set(hashes)) == 1,
        "mean_seconds": round(statistics.fmean(durations), 6),
        "median_seconds": round(statistics.median(durations), 6),
        "minimum_seconds": round(min(durations), 6),
        "maximum_seconds": round(max(durations), 6),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "random_seed": 20260916,
        "summary": summary,
        "git_commit": git_value("rev-parse", "HEAD"),
    }
    (out / "benchmark.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
