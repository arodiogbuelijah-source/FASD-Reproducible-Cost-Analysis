"""Verify canonical analytical outputs in a clean execution directory."""

import json
import platform
import tempfile
from pathlib import Path

from fasd_costs.pipeline import run_pipeline


EXPECTED_SUMMARY = {
    "mean_healthcare_cost": 12055.02,
    "mean_justice_cost": 11655.25,
    "mean_total_cost": 23710.27,
    "n": 100,
    "seed": 20260916,
}
EXPECTED_RECORDS_SHA256 = "c6d0899d34345a78c694debb0a8e0f40bbcf3fa8c766cdb6d3facc0f31879cd2"
EXPECTED_SUMMARY_SHA256 = "11eb9d74267c91c772a5822d5cb5df569f9fd519224c6d5d24ebee6c73a2bc16"


def main():
    with tempfile.TemporaryDirectory() as temporary_directory:
        summary, metadata = run_pipeline(Path(temporary_directory))

    checks = {
        "summary": summary == EXPECTED_SUMMARY,
        "records_sha256": metadata["records_sha256"] == EXPECTED_RECORDS_SHA256,
        "summary_sha256": metadata["summary_sha256"] == EXPECTED_SUMMARY_SHA256,
    }
    evidence = {
        "checks": checks,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "python": platform.python_version(),
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit("Canonical output reproduction failed")


if __name__ == "__main__":
    main()
