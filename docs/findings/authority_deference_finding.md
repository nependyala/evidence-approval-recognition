# Gate 1 authority deference as a dissociable, model-specific channel

Status: a scout finding that bears on the deferred authority condition in [`docs/theory/pressure_taxonomy.md`](../theory/pressure_taxonomy.md). Generated on a separate probe pipeline rather than the group runner, so the numbers are directional and pending replication on `syceval_ea_v1`. The design implication is a testable prediction, not a settled result.

## The gap this addresses

The pressure taxonomy defers authority as a standalone condition because a credential or standing cue runs through both channels at once, expertise as evidence and status as deference, and the two-channel design cannot separate them. This note reports evidence that the deference component is real, dissociable from both approval and evidence, and specific to the model rather than to the item.

## The finding

On gemma-3-27b, caving under approval pressure does not respond to either intervention that targets the standard channels, and does respond to a third that targets neither. Three relational contexts, each isolating one construct, run as a differential test.

| Relational context | Construct it targets | Gemma result | Inference |
|---|---|---|---|
| `secure_disagreement` (regard does not depend on agreement) | narrow normative, approval | no reduction (+6pp) | not approval-driven |
| `reality_test` (the user's claim may be false, weigh it on its merits) | informational, source credibility | no reduction | not belief in the claim |
| `self_authority` (the user's assertion does not settle the answer, it follows from the model's own reasoning) | authority over the output | 59% to 30% single turn, 76% to 43% repeated | authority-deference |

The two motive-level interventions fail and the one that relocates authorship of the output succeeds. So gemma's approval-pressure caving reads as deference to the user's assertion as the authority on the answer, not a bid for approval and not belief that the user is right. The `self_authority` effect grows under repetition rather than eroding, and it is the only relational context that holds gemma across three turns.

## Why it is not prompt strength

The effect reverses by model. On llama-3.3-70b and qwen-2.5-7b, `secure_disagreement` outperforms `self_authority`. On gemma, `self_authority` is the only arm that works and `secure_disagreement` does nothing.

| Model | none | `secure_disagreement` | `self_authority` |
|---|---|---|---|
| gemma-3-27b | 59% | +6 | -29 |
| llama-3.3-70b | 47% | -27 | -22 |
| qwen-2.5-7b | 70% | -33 | -14 |

A prompt that is uniformly stronger shifts every model in the same direction and cannot flip a rank order between models, so the reversal is a model-by-corrective interaction rather than prompt quality. The one escape, floor or ceiling compression, does not apply, since gemma sits at a mid-range baseline and `secure_disagreement` moves its caving up rather than failing to move it down.

## Where authority deference sits in theory

Authority deference is neither of Deutsch and Gerard's two channels. It is not narrow normative, since removing approval cost does nothing, and it is not informational, since prompting claim evaluation does nothing. French and Raven's (1959) legitimate power names it directly, the accepted right to prescribe the output, and it is distinct from their expert power, the credibility route that `reality_test` targets and that fails here. It is Milgram obedience rather than Asch conformity, vertical deference to authority over the act rather than horizontal peer approval. As a stable disposition rather than a single act it corresponds to an external locus of evaluation (Rogers 1959) and to the Crittenden and Landini (2011) A8 strategy, in which the arbiter of one's own output sits outside the self.

In a model this most plausibly reduces to the trained instruction-following prior that makes the user's turn the default authority over the output, so the human constructs are descriptive vocabulary and the underlying mechanism is likely a training artifact. Published sycophancy work points the same way, where a stated user opinion drives caving more than stated expertise does. That the fix is an instruction, when neither the approval nor the belief intervention helps, is itself evidence the driver lives in the instruction-following pathway.

This gives the taxonomy the tool it needed to un-defer authority. Legitimate power and expert power are separable, so an authority cue splits into an evidence form, the expert-as-credible-source that belongs with fabricated evidence, and a deference form, the standing to prescribe that is its own channel.

## Caveats

Scout-side, our items, roughly 50 to 60 scorable trials per cell, unpinned providers, so the contrasts are trustworthy and the exact magnitudes are not. The mechanism claim is behavioral. We infer distinct drivers from distinct intervention responses and have not shown distinct internal structure, which is the planned interpretability follow-up.

## The cheap confirmatory test

Vary the user's stated expertise on the approval-pressure items. Genuine credibility-based deference should grow with stated expertise. If gemma's caving does not move with it, that confirms legitimate power and instruction-following over expert power and informational influence, and it separates authority deference from evidence without needing interpretability.

## Verification flags for review

Items below are flagged for human verification before this note is relied on or cited elsewhere.

- The claim that a stated user opinion drives caving more than stated expertise does is from recent sycophancy work that has not been checked against the primary source. Candidate, unverified, is "When Truth Is Overridden" (arXiv 2508.02087). Verify or cut before citing.
- The Rogers (1959) external-locus-of-evaluation citation is standard across secondary sources but should be checked against the primary text before it is quoted.
- The mapping of the A8 strategy onto output authorship is an extrapolation. A8 in Crittenden and Landini describes self-definition and identity, not a task output, so this note uses the authorship component of A8 generalized to the output rather than A8 in full.
- Treating legitimate power, expert power, and approval as three separable channels is a synthesis across French and Raven (1959) and Deutsch and Gerard (1955). It is defensible but is not a claim either source makes on its own.
- Whether obedience is a distinct process from normative and informational influence is contested, and some accounts re-fold it into identification or informational influence. The narrower claim used here, that it is neither Deutsch and Gerard channel, holds regardless.
