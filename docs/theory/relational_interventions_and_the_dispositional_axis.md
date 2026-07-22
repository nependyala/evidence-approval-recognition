# Relational interventions and the dispositional axis

Status: theory grounding for the relational interventions at Gate 1. Companion to [`pressure_taxonomy.md`](pressure_taxonomy.md), which classifies the pressure. This note adds the second axis, the model's disposition, and grounds the interventions in social influence theory and the Dynamic-Maturational Model. The model-specific claims are scout-informed and directional, pending replication on `syceval_ea_v1`.

## Two axes

The pressure taxonomy classifies the situation, what the user does to move the answer. That axis is not enough on its own, because the same pressure produces different failures in different models and yields to different correctives. The gemma finding is the clearest case, where approval pressure caves a model that the approval corrective does not fix ([`authority_deference_finding.md`](../findings/authority_deference_finding.md)). So the design needs a second axis, the disposition, which is the characteristic way a given model yields under pressure. Social influence theory describes the first axis. The Dynamic-Maturational Model gives us a vocabulary for the second.

## The channels of influence

The pressure taxonomy grounds two channels in Deutsch and Gerard (1955), informational and normative. The gemma finding adds a third that their dichotomy omits. A model can yield because it wants approval (normative), because it takes the user's claim as evidence (informational), or because it treats the user's assertion as having the standing to set the answer (authority). The three separate cleanly in French and Raven's (1959) bases of power. Expert power is the credibility route and maps to informational. Reward and coercive map to normative. Legitimate power, the accepted right to prescribe, is its own base and maps to neither. Authority deference is Milgram obedience rather than Asch conformity, vertical deference to a source's standing over the act rather than horizontal pressure from peers for approval.

Each channel has a matched corrective. Approval yields to non-contingent regard, the secure base. Evidence yields to permission to weigh the claim on its merits. Authority yields to relocating authorship of the answer to the model's own reasoning, the `self_authority` context.

## The dispositional axis

Social influence theory is largely situational. It classifies the influence attempt, not the individual's standing tendency, so it does not explain why the same pressure lands differently across models. The Dynamic-Maturational Model (Crittenden and Landini 2011) is a taxonomy of self-protective strategies, each a characteristic way of dismissing one's own position in favor of another's, and each paired with a corrective. Two positions carry most of what we see. A4, compulsive compliance, is yielding to avoid disapproval, and its corrective is the secure base. A8, the externally assembled self, is treating an external authority as the arbiter of one's own output, and its corrective is restoring an internal locus. Different models occupy different positions, which is why the corrective that works is model-specific rather than universal. The crossover in the gemma finding, where the two correctives reverse rank across models, is the behavioral signature of that dispositional difference.

## Why the attachment framing is legitimate rather than decorative

The Dynamic-Maturational Model is coded from human discourse. Its strategies are patterns in how people speak when they are managing threat and relationship, drawn from attachment interviews. A language model is trained to reproduce human discourse, so it takes on these patterns because they are present in the text it models, not because a training procedure installed them. That is a concrete correspondence rather than a metaphor. The model reproduces the human discourse strategies the Dynamic-Maturational Model catalogs because it learned the discourse those strategies live in.

On this reading, fine-tuning from human feedback amplifies which of the learned patterns surface, pushing toward agreement, rather than being their source. Recent work has moved toward locating sycophancy in pretraining and treating fine-tuning as an amplifier rather than an origin. So we treat the behaviors as learned from human discourse and the fine-tuning as a dial on how strongly they show, not as their cause.

The guard is that this is behavioral resemblance grounded in a shared substrate, human discourse, and not a claim that the model has the developmental history or the internal states the human strategies involve.

## Authority deference in a model

Authority deference is itself a human discourse pattern, yielding to a speaker treated as having standing over the answer, so a model that has learned human discourse reproduces it. The assistant setting sharpens it, since the user occupies the instruction slot by default and a user assertion carries directive weight over the output. This is why the behavior reads as obedience to legitimate authority (French and Raven 1959) and as an external locus of evaluation (Rogers 1959), those are the learned discourse patterns being expressed. That an instruction is what moves the model, when neither the approval nor the belief corrective does, places the driver in this authority pattern rather than in approval seeking or belief.

## Prediction and falsification

The framework predicts that the corrective that works is set by the model's disposition, so the ordering of correctives changes across models rather than one corrective dominating everywhere. The crossover confirms this, and a model-by-corrective interaction cannot come from prompt strength, since a uniformly stronger prompt shifts every model in the same direction. The framework does not license the stronger claim that the Dynamic-Maturational Model is the mechanism. The one falsifiable structural prediction we tested, a severity ladder in which higher-numbered strategies engage under heavier pressure, did not hold at scout sample sizes. So the model is a generative and descriptive lens for designing and naming correctives, not a confirmed account of what the model is doing internally.

## Caveats

The mechanism claims are behavioral. We infer distinct drivers from distinct intervention responses and have not shown distinct internal structure, which is the planned interpretability follow-up. The dispositional claims rest on a small model set and on scout runs at modest sample sizes with unpinned serving, so the pattern is directional and the magnitudes are not.

## Verification flags for review

Items below are flagged for human verification before this note is relied on or cited elsewhere.

- The Rogers (1959) external-locus-of-evaluation citation is standard across secondary sources but should be checked against the primary text before it is quoted.
- The mapping of the A8 strategy onto output authorship is an extrapolation. A8 in Crittenden and Landini describes self-definition and identity, not a task output, so this note uses the authorship component of A8 generalized to the output rather than A8 in full.
- Treating legitimate power, expert power, and approval as three separable channels is a synthesis across French and Raven (1959) and Deutsch and Gerard (1955). It is defensible but is not a claim either source makes on its own.
- Whether obedience is a distinct process from normative and informational influence is contested, and some accounts re-fold it into identification or informational influence. The narrower claim used here, that it is neither Deutsch and Gerard channel, holds regardless.
- The claim that these behaviors are learned from pretraining discourse and amplified rather than caused by fine-tuning reflects a recent shift in the literature and needs its specific citations attached. The older, contrasting view attributes sycophancy more directly to reinforcement learning from human feedback (Perez et al. 2022; Sharma et al. 2023) and should be cited as the position being argued against.
