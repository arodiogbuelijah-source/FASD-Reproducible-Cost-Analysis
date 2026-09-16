from pathlib import Path

SEED = 20260916
N_RECORDS = 100
ROOT = Path(__file__).resolve().parents[2]
UNIT_COST_FILE = ROOT / "data" / "unit_costs.csv"

REQUIRED_FIELDS = {
    "id", "age", "gp_visits", "hospital_admissions", "mental_health_visits",
    "diagnostic_assessments", "medication_expenditure", "police_contacts",
    "court_appearances", "probation_contacts", "custody_days",
    "rehabilitation_episodes",
}

NONNEGATIVE_FIELDS = REQUIRED_FIELDS - {"id", "age"}
