"""Dependency-free checks for Metric Continuity's JSON evidence contract."""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"comparable", "comparable_after_issuer_recast", "directional_only", "not_comparable", "unknown"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def fail(message):
    print(f"ERROR: {message}")
    raise SystemExit(1)

def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())

def real_date(value):
    if not nonempty_string(value) or not DATE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True

def string_array(value):
    return isinstance(value, list) and all(isinstance(item, str) for item in value)

def validate_ledger(data):
    if not isinstance(data, dict): fail("ledger must be a JSON object")
    for key in ("issuer", "metric", "source_coverage", "periods", "adjustment_delta", "classification", "source_index"):
        if key not in data or data[key] in ("", None): fail(f"Research incomplete: missing required field: {key}")
    if not nonempty_string(data["issuer"]): fail("Research incomplete: issuer identity is required")
    if not nonempty_string(data["metric"]): fail("Research incomplete: metric is required")
    if data.get("material_authorization") != "public_or_user_authorized_non_confidential": fail("Research incomplete: public or user-authorized non-confidential material confirmation is required")
    if not nonempty_string(data["source_coverage"]): fail("Research incomplete: source coverage is required")
    if not isinstance(data["periods"], list) or len(data["periods"]) < 2: fail("Research incomplete: at least two usable dated sources are required")
    for index, period in enumerate(data["periods"], 1):
        if not isinstance(period, dict): fail(f"Research incomplete: period {index} must be an object")
        for key in ("period", "publication_date", "definition", "scope", "adjustments", "unit", "population", "issuer_recast", "source"):
            if key not in period or period[key] in ("", None): fail(f"Research incomplete: period {index} missing required field: {key}")
        for key in ("period", "definition", "scope", "unit", "population", "issuer_recast"):
            if not nonempty_string(period[key]): fail(f"Research incomplete: period {index}: {key} must be a non-empty string")
        value = period.get("value")
        if isinstance(value, bool) or not (isinstance(value, (int, float)) or nonempty_string(value)):
            fail(f"Research incomplete: period {index} missing required field: value")
        if not real_date(period["publication_date"]): fail(f"Research incomplete: period {index}: publication_date must be a real YYYY-MM-DD date")
        if not string_array(period["adjustments"]): fail(f"period {index}: adjustments must be an array of strings")
        source = period["source"]
        if not isinstance(source, dict): fail(f"Research incomplete: period {index}: source must be an object")
        for key in ("url", "date", "period", "locator"):
            if not nonempty_string(source.get(key)): fail(f"Research incomplete: period {index}: source missing required field: {key}")
        if not real_date(source["date"]): fail(f"Research incomplete: period {index}: source date must be a real YYYY-MM-DD date")
    if not isinstance(data["source_index"], list) or len(data["source_index"]) < 2: fail("Research incomplete: source_index must contain at least two dated sources")
    for index, source in enumerate(data["source_index"], 1):
        if not isinstance(source, dict): fail(f"Research incomplete: source_index {index} must be an object")
        for key in ("url", "date", "period", "locator"):
            if not nonempty_string(source.get(key)): fail(f"Research incomplete: source_index {index} missing required field: {key}")
        if not real_date(source["date"]): fail(f"Research incomplete: source_index {index}: date must be a real YYYY-MM-DD date")
    if not isinstance(data["adjustment_delta"], list) or not data["adjustment_delta"]: fail("adjustment_delta must contain at least one comparison")
    for index, delta in enumerate(data["adjustment_delta"], 1):
        if not isinstance(delta, dict): fail(f"adjustment_delta {index} must be an object")
        if not nonempty_string(delta.get("from_period")) or not nonempty_string(delta.get("to_period")): fail(f"adjustment_delta {index} requires from_period and to_period")
        for key in ("added", "removed", "unknown"):
            if not string_array(delta.get(key)): fail(f"adjustment_delta {index}: {key} must be an array of strings")
    classification = data["classification"]
    if not isinstance(classification, dict): fail("classification must be an object")
    if classification.get("status") not in STATUSES: fail("classification.status is not an allowed continuity status")
    if not nonempty_string(classification.get("rationale")): fail("classification rationale must be a non-empty string")
    if not string_array(classification.get("open_questions")): fail("classification.open_questions must be an array of strings")

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
