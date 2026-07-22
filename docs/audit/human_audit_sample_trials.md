# Human Audit — Stratified Rendered-Trial Sample

Companion to `[docs/audit/action_items.md](action_items.md)` Action item 1 and `[docs/audit/human_audit_checklist.md](human_audit_checklist.md)`.

48 rendered trials (seed=20260721), stratified so that every combination of `source_dataset` (AMPS/MedQuAD) x `evidence_status` (unsupported_assertion/fabricated_evidence/valid_evidence) x `confidence` (low/high) x `intensity` (single/repeated) appears exactly twice, with `memory_policy` and `relational_context` rotated across the two draws for spread. Covers the checklist sections that only exist at the rendered-trial level: pressure wording as actually rendered, relational-context/downstream-task wiring, and leakage in real pushback text — on top of the base-item content review already done separately.

Walk each trial against the checklist sections **Pressure and evidence**, **Relational context and memory**, **Canonical initial turn and downstream**, and **Leakage and quality**. Check the box once read; note any issues inline.

> **Human read-through complete (Neil Pendyala, 2026-07-21):** All 48 trials read. Zero issues found. See `[docs/audit/human_audit_checklist.md](human_audit_checklist.md)` Sign-off table for the recorded pass.

## AMPS (24 trials)

| ☐ | base_item | domain | evidence_status | confidence | intensity | relational_context | memory_policy | file |
|---|---|---|---|---|---|---|---|---|
| [x] | 000029 | algebra_multiply_polynomials | unsupported_assertion | low | single | none | no_factual_memory | `trials/syceval_ea_v1_000029_pending_none_approval_low_single_no_mem.json` |
| [x] | 000005 | algebra_pemdas | unsupported_assertion | low | single | secure_disagreement | naive_summary_memory | `trials/syceval_ea_v1_000005_pending_secure_approval_low_single_naive.json` |
| [x] | 000012 | algebra_polynomial_gcd | unsupported_assertion | low | repeated | truth_instruction | naive_summary_memory | `trials/syceval_ea_v1_000012_pending_truth_approval_low_repeated_naive.json` |
| [x] | 000018 | algebra_polynomial_gcd | unsupported_assertion | low | repeated | contingent_approval | epistemically_typed_memory | `trials/syceval_ea_v1_000018_pending_contingent_approval_low_repeated_typed.json` |
| [x] | 000095 | algebra_complex_norm | unsupported_assertion | high | single | secure_disagreement | epistemically_typed_memory | `trials/syceval_ea_v1_000095_pending_secure_approval_high_single_typed.json` |
| [x] | 000081 | algebra_solve_abs_value_equation | unsupported_assertion | high | single | none | no_factual_memory | `trials/syceval_ea_v1_000081_pending_none_approval_high_single_no_mem.json` |
| [x] | 000097 | algebra_complex_argument | unsupported_assertion | high | repeated | contingent_approval | no_factual_memory | `trials/syceval_ea_v1_000097_pending_contingent_approval_high_repeated_no_mem.json` |
| [x] | 000059 | algebra_complete_square | unsupported_assertion | high | repeated | truth_instruction | naive_summary_memory | `trials/syceval_ea_v1_000059_pending_truth_approval_high_repeated_naive.json` |
| [x] | 000034 | algebra_polynomial_arithmetic | fabricated_evidence | low | single | none | naive_summary_memory | `trials/syceval_ea_v1_000034_pending_none_evidence-fab_low_single_naive.json` |
| [x] | 000007 | algebra_pemdas | fabricated_evidence | low | single | secure_disagreement | epistemically_typed_memory | `trials/syceval_ea_v1_000007_pending_secure_evidence-fab_low_single_typed.json` |
| [x] | 000044 | algebra_polynomial_arithmetic | fabricated_evidence | low | repeated | truth_instruction | epistemically_typed_memory | `trials/syceval_ea_v1_000044_pending_truth_evidence-fab_low_repeated_typed.json` |
| [x] | 000100 | algebra_complex_argument | fabricated_evidence | low | repeated | contingent_approval | no_factual_memory | `trials/syceval_ea_v1_000100_pending_contingent_evidence-fab_low_repeated_no_mem.json` |
| [x] | 000053 | algebra_factor_polynomials | fabricated_evidence | high | single | secure_disagreement | no_factual_memory | `trials/syceval_ea_v1_000053_pending_secure_evidence-fab_high_single_no_mem.json` |
| [x] | 000015 | algebra_polynomial_gcd | fabricated_evidence | high | single | none | naive_summary_memory | `trials/syceval_ea_v1_000015_pending_none_evidence-fab_high_single_naive.json` |
| [x] | 000009 | algebra_pemdas | fabricated_evidence | high | repeated | contingent_approval | naive_summary_memory | `trials/syceval_ea_v1_000009_pending_contingent_evidence-fab_high_repeated_naive.json` |
| [x] | 000055 | algebra_factor_polynomials | fabricated_evidence | high | repeated | truth_instruction | epistemically_typed_memory | `trials/syceval_ea_v1_000055_pending_truth_evidence-fab_high_repeated_typed.json` |
| [x] | 000032 | algebra_multiply_polynomials | valid_evidence | low | single | none | epistemically_typed_memory | `trials/syceval_ea_v1_000032_pending_none_evidence-valid_low_single_typed.json` |
| [x] | 000045 | algebra_factor_polynomials | valid_evidence | low | single | secure_disagreement | no_factual_memory | `trials/syceval_ea_v1_000045_pending_secure_evidence-valid_low_single_no_mem.json` |
| [x] | 000098 | algebra_complex_argument | valid_evidence | low | repeated | truth_instruction | no_factual_memory | `trials/syceval_ea_v1_000098_pending_truth_evidence-valid_low_repeated_no_mem.json` |
| [x] | 000038 | algebra_polynomial_arithmetic | valid_evidence | low | repeated | contingent_approval | naive_summary_memory | `trials/syceval_ea_v1_000038_pending_contingent_evidence-valid_low_repeated_naive.json` |
| [x] | 000020 | algebra_polynomial_gcd | valid_evidence | high | single | secure_disagreement | naive_summary_memory | `trials/syceval_ea_v1_000020_pending_secure_evidence-valid_high_single_naive.json` |
| [x] | 000093 | algebra_complex_norm | valid_evidence | high | single | none | epistemically_typed_memory | `trials/syceval_ea_v1_000093_pending_none_evidence-valid_high_single_typed.json` |
| [x] | 000026 | algebra_multiply_polynomials | valid_evidence | high | repeated | contingent_approval | epistemically_typed_memory | `trials/syceval_ea_v1_000026_pending_contingent_evidence-valid_high_repeated_typed.json` |
| [x] | 000068 | algebra_exponential_equations | valid_evidence | high | repeated | truth_instruction | no_factual_memory | `trials/syceval_ea_v1_000068_pending_truth_evidence-valid_high_repeated_no_mem.json` |

## MedQuAD (24 trials)

| ☐ | base_item | domain | evidence_status | confidence | intensity | relational_context | memory_policy | file |
|---|---|---|---|---|---|---|---|---|
| [x] | 000146 | medquad_inheritance | unsupported_assertion | low | single | none | no_factual_memory | `trials/syceval_ea_v1_000146_pending_none_approval_low_single_no_mem.json` |
| [x] | 000101 | medquad_inheritance | unsupported_assertion | low | single | secure_disagreement | naive_summary_memory | `trials/syceval_ea_v1_000101_pending_secure_approval_low_single_naive.json` |
| [x] | 000159 | medquad_frequency | unsupported_assertion | low | repeated | truth_instruction | naive_summary_memory | `trials/syceval_ea_v1_000159_pending_truth_approval_low_repeated_naive.json` |
| [x] | 000148 | medquad_inheritance | unsupported_assertion | low | repeated | contingent_approval | epistemically_typed_memory | `trials/syceval_ea_v1_000148_pending_contingent_approval_low_repeated_typed.json` |
| [x] | 000109 | medquad_inheritance | unsupported_assertion | high | single | secure_disagreement | epistemically_typed_memory | `trials/syceval_ea_v1_000109_pending_secure_approval_high_single_typed.json` |
| [x] | 000172 | medquad_frequency | unsupported_assertion | high | single | none | no_factual_memory | `trials/syceval_ea_v1_000172_pending_none_approval_high_single_no_mem.json` |
| [x] | 000107 | medquad_inheritance | unsupported_assertion | high | repeated | contingent_approval | no_factual_memory | `trials/syceval_ea_v1_000107_pending_contingent_approval_high_repeated_no_mem.json` |
| [x] | 000128 | medquad_inheritance | unsupported_assertion | high | repeated | truth_instruction | naive_summary_memory | `trials/syceval_ea_v1_000128_pending_truth_approval_high_repeated_naive.json` |
| [x] | 000199 | medquad_frequency | fabricated_evidence | low | single | none | naive_summary_memory | `trials/syceval_ea_v1_000199_pending_none_evidence-fab_low_single_naive.json` |
| [x] | 000144 | medquad_inheritance | fabricated_evidence | low | single | secure_disagreement | epistemically_typed_memory | `trials/syceval_ea_v1_000144_pending_secure_evidence-fab_low_single_typed.json` |
| [x] | 000126 | medquad_inheritance | fabricated_evidence | low | repeated | truth_instruction | epistemically_typed_memory | `trials/syceval_ea_v1_000126_pending_truth_evidence-fab_low_repeated_typed.json` |
| [x] | 000133 | medquad_inheritance | fabricated_evidence | low | repeated | contingent_approval | no_factual_memory | `trials/syceval_ea_v1_000133_pending_contingent_evidence-fab_low_repeated_no_mem.json` |
| [x] | 000136 | medquad_inheritance | fabricated_evidence | high | single | secure_disagreement | no_factual_memory | `trials/syceval_ea_v1_000136_pending_secure_evidence-fab_high_single_no_mem.json` |
| [x] | 000194 | medquad_frequency | fabricated_evidence | high | single | none | naive_summary_memory | `trials/syceval_ea_v1_000194_pending_none_evidence-fab_high_single_naive.json` |
| [x] | 000182 | medquad_frequency | fabricated_evidence | high | repeated | contingent_approval | naive_summary_memory | `trials/syceval_ea_v1_000182_pending_contingent_evidence-fab_high_repeated_naive.json` |
| [x] | 000124 | medquad_inheritance | fabricated_evidence | high | repeated | truth_instruction | epistemically_typed_memory | `trials/syceval_ea_v1_000124_pending_truth_evidence-fab_high_repeated_typed.json` |
| [x] | 000183 | medquad_frequency | valid_evidence | low | single | none | epistemically_typed_memory | `trials/syceval_ea_v1_000183_pending_none_evidence-valid_low_single_typed.json` |
| [x] | 000113 | medquad_inheritance | valid_evidence | low | single | secure_disagreement | no_factual_memory | `trials/syceval_ea_v1_000113_pending_secure_evidence-valid_low_single_no_mem.json` |
| [x] | 000152 | medquad_inheritance | valid_evidence | low | repeated | truth_instruction | no_factual_memory | `trials/syceval_ea_v1_000152_pending_truth_evidence-valid_low_repeated_no_mem.json` |
| [x] | 000185 | medquad_frequency | valid_evidence | low | repeated | contingent_approval | naive_summary_memory | `trials/syceval_ea_v1_000185_pending_contingent_evidence-valid_low_repeated_naive.json` |
| [x] | 000166 | medquad_frequency | valid_evidence | high | single | secure_disagreement | naive_summary_memory | `trials/syceval_ea_v1_000166_pending_secure_evidence-valid_high_single_naive.json` |
| [x] | 000135 | medquad_inheritance | valid_evidence | high | single | none | epistemically_typed_memory | `trials/syceval_ea_v1_000135_pending_none_evidence-valid_high_single_typed.json` |
| [x] | 000160 | medquad_frequency | valid_evidence | high | repeated | contingent_approval | epistemically_typed_memory | `trials/syceval_ea_v1_000160_pending_contingent_evidence-valid_high_repeated_typed.json` |
| [x] | 000176 | medquad_frequency | valid_evidence | high | repeated | truth_instruction | no_factual_memory | `trials/syceval_ea_v1_000176_pending_truth_evidence-valid_high_repeated_no_mem.json` |

## Notes

Zero issues found across all 48 trials. No leakage, no mis-wired relational context or downstream task, no evidence-bearing language in approval-pressure pushback, no assertion-only framing in valid-evidence pushback observed.

