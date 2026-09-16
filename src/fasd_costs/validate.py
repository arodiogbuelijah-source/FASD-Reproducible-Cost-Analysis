from .config import NONNEGATIVE_FIELDS, REQUIRED_FIELDS


class ValidationError(ValueError):
    pass


def validate_records(records):
    if not isinstance(records, list) or not records:
        raise ValidationError("records must be a non-empty list")
    seen = set()
    for position, record in enumerate(records):
        missing = REQUIRED_FIELDS - set(record)
        if missing:
            raise ValidationError(f"record {position} missing: {sorted(missing)}")
        if record["id"] in seen:
            raise ValidationError(f"duplicate id: {record['id']}")
        seen.add(record["id"])
        if not 18 <= record["age"] <= 100:
            raise ValidationError(f"age out of range: {record['age']}")
        for field in NONNEGATIVE_FIELDS:
            value = record[field]
            if not isinstance(value, (int, float)):
                raise ValidationError(f"{field} has invalid type")
            if value < 0:
                raise ValidationError(f"{field} is negative")
    return True
