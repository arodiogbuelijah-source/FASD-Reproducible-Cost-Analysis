import csv


def load_unit_costs(path):
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["parameter"]: float(row["unit_cost_gbp"]) for row in rows}


def calculate_cost(record, costs):
    healthcare = (
        record["gp_visits"] * costs["gp_visit"]
        + record["hospital_admissions"] * costs["hospital_admission"]
        + record["mental_health_visits"] * costs["mental_health_visit"]
        + record["diagnostic_assessments"] * costs["diagnostic_assessment"]
        + record["medication_expenditure"] * costs["medication_expenditure"]
    )
    justice = (
        record["police_contacts"] * costs["police_contact"]
        + record["court_appearances"] * costs["court_appearance"]
        + record["probation_contacts"] * costs["probation_contact"]
        + record["custody_days"] * costs["custody_day"]
        + record["rehabilitation_episodes"] * costs["rehabilitation_episode"]
    )
    return {
        **record,
        "healthcare_cost": round(healthcare, 2),
        "justice_cost": round(justice, 2),
        "total_cost": round(healthcare + justice, 2),
    }
