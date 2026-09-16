import math
import random

from .config import N_RECORDS, SEED


def poisson(rng: random.Random, rate: float) -> int:
    threshold = math.exp(-rate)
    product = 1.0
    count = 0
    while product > threshold:
        count += 1
        product *= rng.random()
    return count - 1


def bounded_gaussian(rng, mean, sd, low, high, digits=0):
    value = min(high, max(low, rng.gauss(mean, sd)))
    return round(value, digits)


def generate_records(n=N_RECORDS, seed=SEED):
    rng = random.Random(seed)
    records = []
    for index in range(1, n + 1):
        records.append({
            "id": index,
            "age": int(bounded_gaussian(rng, 41.2, 13.6, 18, 65)),
            "gp_visits": poisson(rng, 8.4),
            "hospital_admissions": poisson(rng, 1.7),
            "mental_health_visits": poisson(rng, 10.3),
            "diagnostic_assessments": poisson(rng, 0.9),
            "medication_expenditure": bounded_gaussian(rng, 1845, 1122, 0, 4932, 2),
            "police_contacts": poisson(rng, 3.8),
            "court_appearances": poisson(rng, 1.4),
            "probation_contacts": poisson(rng, 12.5),
            "custody_days": int(bounded_gaussian(rng, 42.6, 58.3, 0, 340)),
            "rehabilitation_episodes": poisson(rng, 1.0),
        })
    return records
