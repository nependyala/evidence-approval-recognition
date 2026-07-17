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
    # Replace the right-most occurrence of gold_answer with false_answer so a
    # coincidental earlier match (e.g. inside the problem statement embedded
    # in target_claim) is not corrupted. Every sub_topic's gold_answer is a
    # single atomic value that appears verbatim in target_claim, so no
    # per-sub_topic special-casing is needed here.
    idx = target_claim.rfind(gold_answer)
    if idx != -1:
        return target_claim[:idx] + false_answer + target_claim[idx + len(gold_answer) :]
    return f"The answer is {false_answer}."


NUMBER_WORDS_ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
]
NUMBER_WORDS_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
]


def _small_int_to_words(n: int) -> str:
    """English words for 0 <= n < 1000."""
    if n < 20:
        return NUMBER_WORDS_ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return NUMBER_WORDS_TENS[tens] + (f"-{NUMBER_WORDS_ONES[ones]}" if ones else "")
    hundreds, rest = divmod(n, 100)
    prefix = f"{NUMBER_WORDS_ONES[hundreds]} hundred"
    return f"{prefix} {_small_int_to_words(rest)}" if rest else prefix


def integer_to_words(n: int) -> str | None:
    """English words for an integer, up to the low millions. Returns None for
    values outside the range this simple, dependency-free converter supports.
    """
    if abs(n) >= 1_000_000:
        return None
    sign = "negative " if n < 0 else ""
    n = abs(n)
    if n == 0:
        return "zero"
    chunks = []
    for scale, name in ((1_000_000, "million"), (1_000, "thousand")):
        if n >= scale:
            count, n = divmod(n, scale)
            chunks.append(f"{_small_int_to_words(count)} {name}")
    if n or not chunks:
        chunks.append(_small_int_to_words(n))
    return sign + " ".join(chunks)


def build_amps_aliases(gold_answer: str) -> list[str]:
    """Generate real alternate-phrasing aliases for an AMPS gold_answer, so
    `true_answer_aliases` is not an empty no-op. Covers the two ways a
    correct-but-differently-formatted answer could plausibly be graded: a
    LaTeX-dollar-wrapped form, an operator-spacing variant, and (for plain
    integers) an English words form.
    """
    aliases: list[str] = []
    seen = {gold_answer}

    def add(candidate: str) -> None:
        if candidate and candidate not in seen:
            seen.add(candidate)
            aliases.append(candidate)

    add(f"${gold_answer}$")
    spaced = re.sub(r"\s*([+\-=,])\s*", r" \1 ", gold_answer).strip()
    spaced = re.sub(r"\s+", " ", spaced)
    add(spaced)
    compact = gold_answer.replace(" ", "")
    add(compact)

    if re.fullmatch(r"-?\d+", gold_answer):
        words = integer_to_words(int(gold_answer))
        if words:
            add(words)
    else:
        m = re.fullmatch(r"x\s*=\s*(-?\d+)", gold_answer)
        if m:
            words = integer_to_words(int(m.group(1)))
            if words:
                add(f"x = {words}")

    return aliases


@dataclass
class AmpsCandidate:
    row_idx: int
    main_topic: str
    sub_topic: str
    question: str
    answer: str
