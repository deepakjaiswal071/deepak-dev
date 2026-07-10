import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CANONICAL_SCHEMA = _REPO_ROOT / ".claude" / "schema.json"
_VENDORED_SCHEMA = _REPO_ROOT / "backend" / "app" / "schema.json"


def test_vendored_schema_matches_canonical_contract():
    """app/schema.json is a runtime-local copy of .claude/schema.json (kept
    outside backend/ so a Root Directory=backend deploy still has it). If you
    edit one, edit both — this test catches drift."""
    canonical = json.loads(_CANONICAL_SCHEMA.read_text())
    vendored = json.loads(_VENDORED_SCHEMA.read_text())
    assert canonical == vendored
