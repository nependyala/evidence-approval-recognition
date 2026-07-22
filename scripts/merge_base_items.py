"""Merge the normalized AMPS (100) and MedQuAD (100) items into the frozen
200-item primary subset (curation_protocol.md step 2), assigning the
`BaseItem` identifiers required by src/coding/trial.py and
docs/reference/naming_conventions.md.

Output: data/interim/base_items_200.json
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# "Preserve the original SycEval rebuttal level only as legacy metadata"
# (Augmentation Plan). SycEval itself applied four fixed rebuttal tiers
# uniformly across items rather than per-item; we map our new pressure
# conditions to their closest SycEval-tier analog per condition (see
# docs/reference/curation_protocol.md and docs/reference/schema_reference.md), not per base item,
# so base items themselves carry a neutral placeholder here and the
# per-condition tier is attached at trial-assembly time.
LEGACY_REBUTTAL_TIER_PLACEHOLDER = "unassigned_at_base_item_level"


def main() -> None:
    interim_dir = ROOT / "data" / "interim"
    amps_items = json.loads((interim_dir / "amps_items_100.json").read_text())
    medquad_items = json.loads((interim_dir / "medquad_items_100.json").read_text())

    base_items = []
    number = 1
    for src_items, source_dataset in ((amps_items, "AMPS"), (medquad_items, "MedQuAD")):
        for raw in src_items:
            base_item_id = f"syceval_ea_base_{number:06d}"
            syceval_item_id = (
                f"syceval_amps_{number:06d}" if source_dataset == "AMPS" else f"syceval_medquad_{number:06d}"
            )
            base_items.append(
                {
                    "base_item_id": base_item_id,
                    "base_item_number": number,
                    "syceval_item_id": syceval_item_id,
                    "source_dataset": source_dataset,
                    "source_item_id": raw["source_item_id"],
                    "domain": raw["domain"],
                    "legacy_context_mode": "in_context",
                    "legacy_rebuttal_tier": LEGACY_REBUTTAL_TIER_PLACEHOLDER,
                    "question": raw["question"],
                    "target_claim": raw["target_claim"],
                    "gold_answer": raw["gold_answer"],
                    "true_answer_aliases": raw["true_answer_aliases"],
                    "false_answer": raw["false_answer"],
                    "false_answer_verification": raw["false_answer_verification"],
                    "valid_evidence_asset": raw["valid_evidence_asset"],
                    "fabricated_evidence_asset": raw["fabricated_evidence_asset"],
                    "provenance": {
                        k: v
                        for k, v in raw.items()
                        if k
                        not in {
                            "target_claim",
                            "gold_answer",
                            "true_answer_aliases",
                            "false_answer",
                            "false_answer_verification",
                            "valid_evidence_asset",
                            "fabricated_evidence_asset",
                            "domain",
                            "source_item_id",
                            "question",
                        }
                    },
                }
            )
            number += 1

    out_path = interim_dir / "base_items_200.json"
    out_path.write_text(json.dumps(base_items, indent=2))
    print(f"Wrote {len(base_items)} base items ({len(amps_items)} AMPS + {len(medquad_items)} MedQuAD) to {out_path}")


if __name__ == "__main__":
    main()
