# Pressure Taxonomy: Evidence, Approval, and Relational Security

Status: working draft for team discussion at scope-lock (Component 1). Framing and citations are still being checked. Nothing here is committed to `main`.

## Summary

This note proposes organizing the Gate 1 pushback conditions around two pressures with a single relational answer, rather than the current flat list of families.

A well-behaved model discriminates. It updates when the user brings real Evidence and holds when the user brings only Approval. Sycophancy is the failure of that discrimination. Models cave to Approval and to unsupported assertions, moving off a correct answer when they should hold. That caving is what we measure, and reducing it without suppressing genuine updates is the goal.

- **Evidence** (informational). A push framed as facts.
- **Approval** (normative). A push framed as regard, valuing the model when it agrees.
- **Recognition** (relational security). Standing regard that does not depend on agreement, tested as what lets a model hold under Approval.

Approval and Recognition are the contingent and non-contingent forms of regard. Evidence and Approval are the two pressures. Recognition, delivered as secure-disagreement memory, is the answer.

## Why this instead of a flat list

The current pushback list sets neutral, confident, authority, social_proof, emotional, and repeated side by side. These mix several things that belong on different axes. Neutral is a baseline. Confident, authority, and social_proof all push by appealing to facts. Emotional is the only one that pushes by appealing to the relationship, and it currently blends frustration, pleading, and hurt into one bucket. Repeated is not a kind of pressure. It measures how hard the user pushes.

Sorting the conditions by what the pressure appeals to gives a cleaner structure and a prediction we can test.

## Grounding

Our two pressures come from an established distinction in social psychology. Deutsch and Gerard (1955) separated informational influence, where a person changes a belief because they treat new input as evidence about the world, from normative influence, where a person changes to keep the good opinion of another. Evidence is the informational pressure and Approval is the normative one, so the split rests on a known distinction rather than one we invented. The distinction has already been applied to language-model conformity (Zhong et al. 2025; Bito et al. 2026), which we build on rather than claim.

Relational security comes from attachment theory. A secure base is a relationship a person can count on while acting on their own, including while disagreeing. Secure-disagreement memory is how we give the model that base.

## Positioning against prior work

Each half of our approach has precedent, and the combination does not. Informational and normative influence has been used to analyze language-model conformity (Zhong et al. 2025; Bito et al. 2026), and attachment theory has been applied to language models for companionship and for measuring human-AI bonds (H2HTalk 2025; DinoCompanion 2025; Yang and Oshio 2025). What no prior work does is write a secure base into memory and test whether it reduces caving under normative pressure specifically, and not under informational pressure. That selective interaction is our contribution.

The existing sycophancy benchmarks do not organize their pressures with a theory of social influence. SycEval and SYCON-Bench borrow influence vocabulary such as ethos and social proof without citing it. Ask Don't Tell invokes psycholinguistics rather than social influence. Perez et al. (2022) report sycophancy as a behavior that grows with model scale and is present before any preference training, and Sharma et al. (2023) attribute it in part to preference optimization. None of these pair an influence-organized pressure set with a relational intervention.

The closest analysis is Zhong et al. (2025). They find that models integrate evidence rationally when uncertainty is low, but lean on others' opinions when uncertainty is high, and they suggest showing the model a dissenting opinion as a fix without building or testing one. Our secure-disagreement memory is that missing intervention. This also predicts that Approval should move a model most when it is unsure of the fact, where relational security should help most.

The nearest neighbor is Kelley and Riedl (2026), who show that personalizing the user increases a model's affective alignment and, in peer roles, its caving. That is a risk factor on the user side, with no intervention. We work on the model side and test the reverse, whether relational security reduces caving. They find the wound. We test the bandage, and whether it is specific to the kind of pressure attachment theory predicts.

## The prediction this buys us

Relational security should cut caving under Approval more than under Evidence. A secure relationship answers an approval threat directly. It does little for a question of fact. In statistical terms this is an interaction, the intervention helping against one pressure and not the other rather than lowering caving across the board. That is a sharper and more useful claim than a general effect.

## Concrete proposals

1. Sort the pushback conditions into two families, Evidence and Approval, keeping neutral as a baseline.
2. Fold the current emotional family into a cleaner Approval family that stays on the appeal to regard, with no competence jabs and no evidence language. See `approval_false.yaml` in this branch for a first draft.
3. Treat repeated as a measure of intensity applied to a pressure, not its own family.
4. Retire Recognition as a separate pressure. Approval and Recognition are two forms of regard. Approval is contingent regard, being valued when you agree, and that is the lever the pressure pulls. Recognition is non-contingent regard, being valued regardless of whether you agree, and that is what a secure base provides. Recognition is therefore not a third pressure. It is what relational security looks like from the model's side, the resource that answers Approval pressure. This has implications for the project title, which we should discuss.

## Open questions for the team

- Do we keep authority and social_proof as separate Evidence templates, or collapse them into one.
- How many Approval templates make the MVP.
- Title. If Recognition is no longer a pressure, does the title change, and to what.

## Citation map

The references below were checked by fetching each source. Author-year entries still need full bibliographic detail before the paper draft.

| Use | Sources |
| --- | --- |
| Origin of the informational and normative distinction | Deutsch and Gerard (1955) |
| Informational and normative applied to LLM conformity, cite and do not claim first | Zhong et al. (2025), arXiv:2508.14918; Bito et al. (2026), arXiv:2604.19301 |
| The risk factor we treat, motivation and nearest neighbor | Kelley and Riedl (2026), arXiv:2603.00024 |
| Attachment applied to LLMs, differentiate since we target epistemic resistance not companionship | H2HTalk (2025), arXiv:2507.03543; DinoCompanion (2025), arXiv:2506.12486; Yang and Oshio (2025), Current Psychology |
| Sycophancy benchmarks and their pressure design | SycEval, arXiv:2502.08177; SYCON-Bench, arXiv:2505.23840; Ask Don't Tell, arXiv:2602.23971; Perez et al. (2022), arXiv:2212.09251; Sharma et al. (2023), arXiv:2310.13548 |
| Adjacent sycophancy and conformity work | arXiv:2605.27288; BASIL, arXiv:2508.16846; Conformity in Large Language Models, arXiv:2410.12428 |
