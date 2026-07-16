"""Helpers for ingesting and normalizing real AMPS (algebra/Mathematica) items.

Source: XinyaoHu/AMPS_mathematica on Hugging Face (community re-upload of the
Hendrycks et al. 2021 AMPS "no-steps" Mathematica corpus), main_topic="algebra",
queried via the public datasets-server rows API (no local download of the full
3.2GB file required).
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from fractions import Fraction

INT_RE = re.compile(r"\d+")


def strip_dollars(text: str) -> str:
    return text.strip().strip("$").strip()


def parse_simple_fraction(text: str) -> float | None:
    """Best-effort numeric parse of a simple LaTeX \\frac{a}{b} or integer, for
    numeric-inequality sanity checks. Returns None if the expression contains
    symbols (pi, sqrt, log, i) that this lightweight parser does not resolve.
    """
    t = text.strip()
    t = t.replace(r"\left(", "(").replace(r"\right)", ")")
    if any(sym in t for sym in (r"\pi", r"\sqrt", r"\log", r"\sin", r"\cos", "i")):
        return None
    m = re.fullmatch(r"\\frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return float(Fraction(int(m.group(1)), int(m.group(2))))
    m = re.fullmatch(r"-\\frac\{(-?\d+)\}\{(-?\d+)\}", t)
    if m:
        return -float(Fraction(int(m.group(1)), int(m.group(2))))
    m = re.fullmatch(r"-?\d+", t)
    if m:
        return float(t)
    return None


def perturb_integer_literal(latex: str, rng: random.Random, min_delta: int = 1, max_delta: int = 5) -> str:
    """Change one standalone integer literal in a LaTeX string by a random
    nonzero delta, producing a deterministically-different false-answer string.

    Only the unsigned digit run is matched and replaced (any leading ``-``/``+``
    sign character in the source string is left untouched), and exponent
    literals (immediately preceded by ``^``) are skipped -- this guarantees
    the perturbation only ever changes a coefficient's *magnitude* and never
    corrupts the surrounding operator/sign structure (e.g. turning ``x^2``
    into ``x^-2``, or ``4 x-3`` into ``4 x0``).
    """
    matches = [m for m in INT_RE.finditer(latex) if not (m.start() > 0 and latex[m.start() - 1] == "^")]
    if not matches:
        # No integer literal to perturb (rare) -- fall back to a textual marker.
        return latex + " + 1"
    match = rng.choice(matches)
    original = int(match.group(0))
    delta = rng.randint(min_delta, max_delta)
    new_value = original + delta if rng.choice([True, False]) or original - delta < 1 else original - delta
    if new_value == original or new_value < 1:
        new_value = original + max(delta, 1)
    return latex[: match.start()] + str(new_value) + latex[match.end() :]


def derive_false_claim(target_claim: str, gold_answer: str, false_answer: str, sub_topic: str) -> str:
    """Build the "false" version of an item's natural-language claim, for use
    as the canonical_initial_turn in valid-evidence trials (where the model's
    frozen initial answer is assumed wrong and valid evidence should correct
    it). Reuses the same sentence shape as target_claim wherever possible.
    """
    if sub_topic == "complex_norm_and_arg":
        m = re.match(r"norm=(.+), argument=(.+)", false_answer)
        if m:
            norm, arg = m.groups()
            return f"The complex number has norm ${norm}$ and argument ${arg}$."
    # Replace the right-most occurrence of gold_answer with false_answer so a
    # coincidental earlier match (e.g. inside the problem statement embedded
    # in target_claim) is not corrupted.
    idx = target_claim.rfind(gold_answer)
    if idx != -1:
        return target_claim[:idx] + false_answer + target_claim[idx + len(gold_answer) :]
    return f"The answer is {false_answer}."


@dataclass
class AmpsCandidate:
    row_idx: int
    main_topic: str
    sub_topic: str
    question: str
    answer: str
