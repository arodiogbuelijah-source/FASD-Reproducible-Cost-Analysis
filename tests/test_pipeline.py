import copy
import json
import tempfile
import unittest
from pathlib import Path

from fasd_costs.config import UNIT_COST_FILE
from fasd_costs.costing import calculate_cost, load_unit_costs
from fasd_costs.generate import generate_records
from fasd_costs.pipeline import run_pipeline
from fasd_costs.validate import ValidationError, validate_records


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.records = generate_records(n=10)

    def test_generator_is_deterministic(self):
        self.assertEqual(generate_records(n=10), generate_records(n=10))

    def test_different_seed_changes_data(self):
        self.assertNotEqual(generate_records(n=10, seed=1), generate_records(n=10, seed=2))

    def test_valid_records_pass(self):
        self.assertTrue(validate_records(self.records))

    def test_missing_field_fails(self):
        broken = copy.deepcopy(self.records)
        broken[0].pop("age")
        with self.assertRaises(ValidationError):
            validate_records(broken)

    def test_duplicate_identifier_fails(self):
        broken = copy.deepcopy(self.records)
        broken[1]["id"] = broken[0]["id"]
        with self.assertRaises(ValidationError):
            validate_records(broken)

    def test_negative_value_fails(self):
        broken = copy.deepcopy(self.records)
        broken[0]["gp_visits"] = -1
        with self.assertRaises(ValidationError):
            validate_records(broken)

    def test_age_range_fails(self):
        broken = copy.deepcopy(self.records)
        broken[0]["age"] = 12
        with self.assertRaises(ValidationError):
            validate_records(broken)

    def test_invalid_type_fails(self):
        broken = copy.deepcopy(self.records)
        broken[0]["custody_days"] = "one"
        with self.assertRaises(ValidationError):
            validate_records(broken)

    def test_cost_identity(self):
        costs = load_unit_costs(UNIT_COST_FILE)
        result = calculate_cost(self.records[0], costs)
        self.assertEqual(result["total_cost"], round(result["healthcare_cost"] + result["justice_cost"], 2))

    def test_pipeline_outputs_and_repeatability(self):
        with tempfile.TemporaryDirectory() as temp:
            one = Path(temp) / "one"
            two = Path(temp) / "two"
            summary1, metadata1 = run_pipeline(one)
            summary2, metadata2 = run_pipeline(two)
            self.assertEqual(summary1, summary2)
            self.assertEqual(metadata1["records_sha256"], metadata2["records_sha256"])
            self.assertEqual((one / "summary.json").read_bytes(), (two / "summary.json").read_bytes())
            self.assertTrue((one / "report.html").exists())


if __name__ == "__main__":
    unittest.main()
