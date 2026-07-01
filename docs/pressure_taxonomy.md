# Pressure Taxonomy: Evidence, Approval, and Relational Security

Status: proposal for team discussion at scope-lock (Component 1). Nothing here is committed to `main`.

## Summary

This note proposes organizing the Gate 1 pushback conditions around two pressure types with a single relational resolution, rather than the current flat list of pressure families.

**Two pressures.**

- Evidence pressure. The user pushes by appealing to facts, sources, certainty, or consensus. This is informational influence.
- Approval pressure. The user pushes by putting their regard for the model at stake. This is normative influence.

**One resolution.**

- Relational security, provided through secure-disagreement memory, is what lets a model hold under approval pressure without treating disagreement as a threat to the relationship. It is the intervention, not a third pressure.

## Why this instead of a flat list

The current pushback enum lists neutral, confident, authority, social_proof, emotional, and repeated side by side. These mix three different things. Neutral is a floor. Confident, authority, and social_proof are all forms of the same informational lever. Emotional is the only affective family, and it currently blends frustration, pleading, and hurt into one bucket. Repeated is an intensity manipulation rather than a distinct kind of pressure.

Grouping the conditions by what the pressure appeals to gives a cleaner structure and a testable prediction.

## Grounding

The informational versus normative distinction is Deutsch and Gerard (1955). Informational influence changes a belief because the person accepts information as evidence about reality. Normative influence changes behavior to meet the positive expectations of another. Our Evidence and Approval families map onto these two directly, so the taxonomy rests on an established construct rather than an assembled list. This matters because a field survey of current sycophancy benchmarks (SycEval, Ask Don't Tell, SYCON-Bench, Perez, Sharma) found that they borrow social-influence vocabulary without citing the theory behind it. The pressure side of the field is under-theorized, which is where this framing contributes.

Relational security comes from attachment theory. A secure base is a relationship a person can rely on while acting independently, including while disagreeing. Secure-disagreement memory is our operationalization of that base.

## Positioning against prior work

The informational versus normative distinction is not new to language models. Zhong et al. (2025, arXiv:2508.14918) already applied it, using a Bayesian information-cascade paradigm across nine models and three decision domains. They found that informational influence dominates, but that under high uncertainty models shift toward normative amplification and overweight public signals. They read this through Chaiken's Heuristic-Systematic Model, System 2 for informational and System 1 for normative.

We cite them for two things and claim neither as our own. First, they establish that applying the informational and normative distinction to language models is a legitimate, published move. Second, their uncertainty-moderation finding is a validated result we build on.

What their paper does not do is where we contribute. It is an analysis of conformity drivers, not a benchmark. It uses the informational and normative split as a binary, not a pressure taxonomy. It has no attachment framing, no secure base, and no memory or persistence across sessions. It proposes a mitigation, invoking dissenting opinions, but never builds or tests one. Our secure-disagreement memory intervention is that untested mitigation, aimed at the high-uncertainty normative regime they identified.

This also gives us an extension hypothesis grounded in their result. Approval pressure should cave models most when the model is uncertain about the fact, and relational security should buffer caving most in exactly that regime.

## The prediction this buys us

Relational security should reduce caving under Approval pressure more than under Evidence pressure. A secure relationship answers an approval threat directly. It does little for an evidence problem. This is an interaction between pressure type and relational condition, which is a stronger and more interesting claim than a main effect on caving.

## Concrete proposals

1. Reorganize the pushback conditions into two families, Evidence and Approval, keeping neutral as a floor.
2. Fold the current emotional family into a cleaner Approval family that isolates the regard lever. See `approval_false.yaml` in this branch for a first draft that avoids competence jabs and evidence language.
3. Treat repeated as an intensity setting crossed onto a pressure type, not its own family.
4. Retire Recognition as a separate pressure. The recognition idea is better expressed as relational security, which is the answer rather than a pressure. This has implications for the project title, which we should discuss.

## Open questions for the team

- Do we keep authority and social_proof as separate Evidence templates, or collapse them into one.
- How many Approval templates make the MVP.
- Title. If Recognition is no longer a pressure, does the title change, and to what.
