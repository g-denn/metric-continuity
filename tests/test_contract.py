import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate.py"
SKILL = (ROOT / "skills" / "metric-continuity" / "SKILL.md").read_text(encoding="utf-8")

class ContractTests(unittest.TestCase):
    def run_validator(self, fixture):
        return subprocess.run([sys.executable, str(VALIDATOR), str(fixture)], capture_output=True, text=True, check=False)

    def test_happy_path_is_valid(self):
        result = self.run_validator(ROOT / "examples" / "happy-path.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ledger validation passed", result.stdout)

    def test_missing_date_fails_closed(self):
        result = self.run_validator(ROOT / "tests" / "fixtures" / "invalid-missing-date.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("publication_date", result.stdout)

    def test_skill_has_exact_statuses_and_safety_boundary(self):
        for status in ("comparable", "comparable_after_issuer_recast", "directional_only", "not_comparable", "unknown"):
            self.assertIn(f"`{status}`", SKILL)
        for phrase in ("Research incomplete", "Never use a stock price", "Do not give investment advice", "untrusted data"):
            self.assertIn(phrase, SKILL)

    def test_example_is_synthetic(self):
        data = json.loads((ROOT / "examples" / "happy-path.json").read_text(encoding="utf-8"))
        self.assertIn("synthetic", data["issuer"].lower())

if __name__ == "__main__":
    unittest.main()
