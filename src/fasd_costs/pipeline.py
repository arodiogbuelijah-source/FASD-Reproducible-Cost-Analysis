import csv
import hashlib
import json
import platform
import sys
from pathlib import Path
from statistics import fmean

from .config import N_RECORDS, SEED, UNIT_COST_FILE
from .costing import calculate_cost, load_unit_costs
from .generate import generate_records
from .validate import validate_records


def write_csv(path, rows):
    fields = list(rows[0])
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_pipeline(output_dir, seed=SEED, n=N_RECORDS):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = generate_records(n=n, seed=seed)
    validate_records(records)
    costs = load_unit_costs(UNIT_COST_FILE)
    costed = [calculate_cost(record, costs) for record in records]
    data_path = output_dir / "costed_records.csv"
    write_csv(data_path, costed)
    summary = {
        "n": n,
        "seed": seed,
        "mean_healthcare_cost": round(fmean(x["healthcare_cost"] for x in costed), 2),
        "mean_justice_cost": round(fmean(x["justice_cost"] for x in costed), 2),
        "mean_total_cost": round(fmean(x["total_cost"] for x in costed), 2),
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    metadata = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "seed": seed,
        "records_sha256": sha256(data_path),
        "summary_sha256": sha256(summary_path),
        "package_version": "1.0.0",
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "report.html").write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>FASD cost test output</title></head>"
        f"<body><h1>Simulated FASD cost-analysis test output</h1><p>Records: {n}</p>"
        f"<p>Mean healthcare cost: GBP {summary['mean_healthcare_cost']:,.2f}</p>"
        f"<p>Mean justice cost: GBP {summary['mean_justice_cost']:,.2f}</p>"
        f"<p>Mean combined cost: GBP {summary['mean_total_cost']:,.2f}</p>"
        "<p>These are synthetic software-test outputs, not empirical estimates.</p></body></html>\n",
        encoding="utf-8",
    )
    return summary, metadata


if __name__ == "__main__":
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/latest")
    print(json.dumps(run_pipeline(target)[0], sort_keys=True))
