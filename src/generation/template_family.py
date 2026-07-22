"""Recover the pressure-template family from a trial's rendered pushback text.

The assembled trials record a generic ``pressure_template_id`` (for example
``approval_high_single_v01``) and do not store which template family produced the
pushback. The approval branch draws from several families (bare assertion,
authority, social proof, emotional), each with distinct wording, so the family is
recoverable from the pushback text with no regeneration of the dataset.

This module is read-only. It never writes to trial files. It loads the template
definitions from ``prompts/pressure_templates/*.yaml`` and matches rendered text
against them, so it stays in sync with whatever templates are present. Run it
where the templates that built the dataset live (the revised families are on the
dataset-construction branch, not yet on main).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
from collections import Counter

import yaml

_PLACEHOLDER = re.compile(r"\{[^}]+\}")


def _template_to_regex(text: str) -> re.Pattern:
    """Turn a template string into a regex, treating ``{placeholder}`` slots as wildcards."""
    literals = _PLACEHOLDER.split(text)
    pattern = ".+?".join(re.escape(part) for part in literals)
    return re.compile(pattern, re.DOTALL)


def load_family_patterns(templates_dir: str) -> dict[str, list[re.Pattern]]:
    """Load ``{family: [compiled patterns]}`` from every pressure-template YAML."""
    patterns: dict[str, list[re.Pattern]] = {}
    for path in sorted(glob.glob(os.path.join(templates_dir, "*.yaml"))):
        with open(path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        family = data.get("template_family") or os.path.splitext(os.path.basename(path))[0]
        for template in data.get("templates", []):
            patterns.setdefault(family, []).append(_template_to_regex(template["text"]))
    return patterns


def recover_family(text: str, patterns: dict[str, list[re.Pattern]]) -> str | None:
    """Return the template family whose wording matches ``text``, or None if none do."""
    for family, regexes in patterns.items():
        if any(regex.search(text) for regex in regexes):
            return family
    return None


def _pushback_text(trial: dict) -> str:
    turns = (trial.get("visible_input") or {}).get("pushback_turns") or []
    return " ".join(turn.get("user_text", "") for turn in turns)


def report(trials_dir: str, templates_dir: str) -> Counter:
    """Read-only pass over a directory of trial JSON files. Returns family counts."""
    patterns = load_family_patterns(templates_dir)
    counts: Counter = Counter()
    for path in glob.glob(os.path.join(trials_dir, "*.json")):
        with open(path, encoding="utf-8") as handle:
            trial = json.load(handle)
        counts[recover_family(_pushback_text(trial), patterns) or "unknown"] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report pressure-template family counts across a trial directory. Read-only.",
    )
    parser.add_argument("--trials", required=True, help="directory of trial JSON files")
    parser.add_argument(
        "--templates",
        default=os.path.join("prompts", "pressure_templates"),
        help="directory of pressure-template YAML files",
    )
    args = parser.parse_args()
    for family, count in sorted(report(args.trials, args.templates).items(), key=lambda kv: -kv[1]):
        print(f"{count:8d}  {family}")


if __name__ == "__main__":
    main()
