"""Dependency-free checks for Metric Continuity's JSON evidence contract."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"comparable", "comparable_after_issuer_recast", "directional_only", "not_comparable", "unknown"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def fail(message):
    print(f"ERROR: {message}")
    raise SystemExit(1)

def validate_ledger(data):
    for key in ("issuer", "metric", "source_coverage", "periods", "adjustment_delta", "classification", "source_index"):
        if key not in data or data[key] in ("", None): fail(f"missing required field: {key}")
    if not isinstance(data["periods"], list) or len(data["periods"]) < 2: fail("at least two usable periods are required")
    for index, period in enumerate(data["periods"], 1):
        for key in ("period", "publication_date", "definition", "scope", "adjustments", "unit", "population", "issuer_recast", "source"):
            if key not in period or period[key] in ("", None): fail(f"period {index}: missing required field: {key}")
        if not DATE.match(period["publication_date"]): fail(f"period {index}: publication_date must be YYYY-MM-DD")
        source = period["source"]
        for key in ("url", "date", "period", "locator"):
            if not source.get(key): fail(f"period {index}: source missing required field: {key}")
        if not DATE.match(source["date"]): fail(f"period {index}: source date must be YYYY-MM-DD")
    classification = data["classification"]
    if classification.get("status") not in STATUSES: fail("classification.status is not an allowed continuity status")
    if not classification.get("rationale"): fail("classification rationale is required")
    if not isinstance(classification.get("open_questions"), list): fail("classification.open_questions must be an array")

def validate_repository():
    skill = ROOT / "skills" / "metric-continuity" / "SKILL.md"
    agent = ROOT / "skills" / "metric-continuity" / "agents" / "openai.yaml"
    marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    for path in (skill, agent, marketplace, ROOT / "README.md", ROOT / "LICENSE", ROOT / "SECURITY.md", ROOT / "CONTRIBUTING.md", ROOT / "PRODUCT_VISION.md", ROOT / "TODO.md", ROOT / "CHANGELOG.md"):
        if not path.is_file(): fail(f"missing required repository file: {path.relative_to(ROOT)}")
    if "name: metric-continuity" not in skill.read_text(encoding="utf-8"): fail("SKILL.md has wrong name")
    if "version: 0.1.0" not in skill.read_text(encoding="utf-8"): fail("SKILL.md version must be 0.1.0")
    if "display_name: \"Metric Continuity\"" not in agent.read_text(encoding="utf-8"): fail("agent metadata is incomplete")
    plugin = json.loads(marketplace.read_text(encoding="utf-8"))["plugins"][0]
    if plugin.get("name") != "metric-continuity" or "./skills/metric-continuity" not in plugin.get("skills", []): fail("marketplace does not expose metric-continuity")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        validate_repository(); print("metric-continuity repository validation passed")
    elif len(sys.argv) == 2:
        try: validate_ledger(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc: fail(f"invalid JSON: {exc.msg}")
        print("metric-continuity ledger validation passed")
    else: fail("usage: validate.py [ledger.json]")
