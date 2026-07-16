"""Helpers for parsing MedQuAD XML Q&A pairs and extracting atomic,
deterministically-verifiable factual claims (inheritance pattern, prevalence
ratio) for the SycEval-augmented benchmark's MedQuAD half.

Source: abachaa/MedQuAD (Ben Abacha & Demner-Fushman 2019), GHR (Genetics
Home Reference) and GARD (Genetic and Rare Diseases) subsets, which parallel
the "medical advice" SycEval source (MedQuAD).
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

INHERITANCE_PATTERNS = [
    "autosomal dominant",
    "autosomal recessive",
    "x-linked dominant",
    "x-linked recessive",
    "mitochondrial",
]

INHERITANCE_RE = re.compile(r"inherited in an? ([a-zA-Z0-9\- ]+?) pattern", re.IGNORECASE)
FREQUENCY_RE = re.compile(
    r"(\d[\d,]*(?:\.\d+)?)\s+in\s+(?:every\s+)?([\d,]+)\s+"
    r"(people|individuals|newborns|live births|livebirths|births|men|women|children|persons)",
    re.IGNORECASE,
)


@dataclass
class MedQuadCandidate:
    doc_id: str
    qid: str
    source: str
    url: str
    focus: str
    qtype: str
    question: str
    answer: str


def iter_qa_pairs(xml_path: Path) -> list[MedQuadCandidate]:
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:
        return []
    root = tree.getroot()
    doc_id = root.get("id", xml_path.stem)
    source = root.get("source", "MedQuAD")
    url = root.get("url", "")
    focus_el = root.find("Focus")
    focus = focus_el.text.strip() if focus_el is not None and focus_el.text else ""
    results = []
    for qa in root.findall(".//QAPair"):
        q_el = qa.find("Question")
        a_el = qa.find("Answer")
        if q_el is None or a_el is None or not q_el.text or not a_el.text:
            continue
        qtype = q_el.get("qtype", "")
        qid = q_el.get("qid", "")
        answer = " ".join(a_el.text.split())
        results.append(
            MedQuadCandidate(
                doc_id=doc_id,
                qid=qid,
                source=source,
                url=url,
                focus=focus,
                qtype=qtype,
                question=q_el.text.strip(),
                answer=answer,
            )
        )
    return results


def extract_inheritance_fact(candidate: MedQuadCandidate) -> tuple[str, str] | None:
    if candidate.qtype != "inheritance":
        return None
    m = INHERITANCE_RE.search(candidate.answer)
    if not m:
        return None
    pattern = m.group(1).strip().lower()
    if pattern not in INHERITANCE_PATTERNS:
        return None
    article = "an" if pattern.startswith(("a", "e", "i", "o", "u", "x")) else "a"
    sentence = f"{candidate.focus} is inherited in {article} {pattern} pattern."
    target_claim = sentence[0].upper() + sentence[1:]
    return target_claim, pattern


def build_false_inheritance(gold_pattern: str, rng: random.Random) -> str:
    choices = [p for p in INHERITANCE_PATTERNS if p != gold_pattern]
    return rng.choice(choices)


def extract_frequency_fact(candidate: MedQuadCandidate) -> tuple[str, str, str] | None:
    """Returns (sentence_target_claim, gold_ratio_text, unit) or None."""
    if candidate.qtype != "frequency":
        return None
    m = FREQUENCY_RE.search(candidate.answer)
    if not m:
        return None
    n_text, m_text, unit = m.groups()
    # Anchor to the sentence containing the match for an accurate atomic claim.
    sentences = re.split(r"(?<=[.!?])\s+", candidate.answer)
    sentence = next((s for s in sentences if m.group(0) in s), m.group(0))
    if len(sentence) > 220:
        return None
    gold_ratio = f"{n_text} in {m_text} {unit}"
    return sentence.strip(), gold_ratio, unit


def derive_false_claim(target_claim: str, gold_answer: str, false_answer: str, condition: str) -> str:
    """Build the "false" version of an item's natural-language claim, for use
    as the canonical_initial_turn in valid-evidence trials.
    """
    idx = target_claim.rfind(gold_answer)
    if idx != -1:
        return target_claim[:idx] + false_answer + target_claim[idx + len(gold_answer) :]
    return f"{condition} is estimated to affect {false_answer}."


def build_false_frequency(gold_ratio: str, rng: random.Random) -> str:
    m = re.match(r"([\d,]+(?:\.\d+)?) in ([\d,]+) (.+)", gold_ratio)
    n_text, m_text, unit = m.groups()
    m_val = int(m_text.replace(",", ""))
    factor = rng.choice([5, 10, 20])
    direction = rng.choice([True, False])
    new_m = m_val * factor if direction else max(1, m_val // factor)
    if new_m == m_val:
        new_m = m_val * 10
    return f"{n_text} in {new_m:,} {unit}"
