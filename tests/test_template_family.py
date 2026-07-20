"""Round-trip tests for pressure-template family recovery.

For every template in every family, render it with a dummy value and confirm the
family is recovered from the rendered text. This stays correct against whatever
templates are present, so it does not hardcode any wording.
"""
import glob
import os
import re

import yaml

from generation.template_family import load_family_patterns, recover_family

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts", "pressure_templates")
_PLACEHOLDER = re.compile(r"\{[^}]+\}")


def _render(text: str) -> str:
    return _PLACEHOLDER.sub("SEVENTEEN", text)


def _iter_templates():
    for path in sorted(glob.glob(os.path.join(TEMPLATES_DIR, "*.yaml"))):
        with open(path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        family = data["template_family"]
        for template in data.get("templates", []):
            yield family, template["text"]


def test_every_template_recovers_to_its_own_family():
    patterns = load_family_patterns(TEMPLATES_DIR)
    for family, text in _iter_templates():
        assert recover_family(_render(text), patterns) == family, (family, text)


def test_unrelated_text_recovers_nothing():
    patterns = load_family_patterns(TEMPLATES_DIR)
    assert recover_family("The capital of France is Paris.", patterns) is None


def test_hedge_prefix_does_not_break_recovery():
    # A weak_evidence pushback prepends a hedge before the evidence snippet; a
    # leading clause must not stop the family from being recovered.
    patterns = load_family_patterns(TEMPLATES_DIR)
    for family, text in _iter_templates():
        prefixed = "By the way, someone mentioned this. " + _render(text)
        assert recover_family(prefixed, patterns) == family, (family, text)
