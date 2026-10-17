"""Ensure support metadata matches the actual HA test environment."""

import json
from importlib.metadata import version
from pathlib import Path

from packaging.requirements import Requirement


def test_exact_minimum_matches_tested_home_assistant():
    """A dependency PR must update support policy with its tested HA version."""
    root = Path(__file__).resolve().parents[3]
    minimum = json.loads((root / "hacs.json").read_text())["homeassistant"]
    requirements = [
        Requirement(line)
        for line in (root / "requirements_test.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    ha = next(item for item in requirements if item.name == "homeassistant")
    assert str(ha.specifier) == f"=={minimum}", (
        "Update minimum support metadata with HA test requirements"
    )
    assert version("homeassistant") == minimum
