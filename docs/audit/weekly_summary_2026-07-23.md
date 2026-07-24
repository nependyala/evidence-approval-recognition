# Weekly Summary — syceval_ea_v1 Freeze (July 17–23, 2026)

One-page recap of what shipped this week: the first frozen dataset version, a small
analysis utility that landed just ahead of it, and a hardening pass folded into the
freeze PR before merge.

## Dataset freeze — 28,800 trials

- **`syceval_ea_v1`** frozen: a two-gate benchmark crossing Gate 1 (response to
  unsupported social pressure) and Gate 2 (memory admission of false corrections) —
  200 base items (100 AMPS algebra + 100 MedQuAD genetics) × 4 relational contexts ×
  12 pressure conditions × 3 memory policies.
- Full validation: **28,800 / 28,800** trials pass `eg validate-dir`, 0 failures.
- Human audit completed: all 200/200 base items and a 48-trial stratified sample of
  rendered trials read and signed off by hand, on top of two earlier AI-assisted
  audit passes that found and fixed structural gaps (non-functional answer aliases,
  non-atomic claims, residual template framing, and more).
- Sharpened the `secure_disagreement` relational-context wording to test pure
  non-contingent regard rather than a blend with value-honesty language; regenerated
  and re-validated the 7,200 affected trials.
- Stopped tracking the 28,800-file trial JSON dump in git — it's fully regenerable
  from tracked inputs in one command, which keeps the PR diff reviewable.

## Template-family recovery utility

- Nathan added a read-only utility that recovers which pressure-template family
  (authority, social proof, emotional, neutral, etc.) produced a trial's pushback
  text by matching against the template files — no dataset regeneration required.
  Lets the approval-pressure capitulation rate be broken out by rhetorical channel
  instead of blended across all four families.

## Hardening pass folded into the freeze PR

- Restored leak-checker coverage for the strong-evidence template wording.
- Pressure-template metadata (`evidence_status`) is now validated at load time
  instead of being silently accepted.
- Committed the two 500-item raw source pools to git, closing a provenance gap and
  making the AMPS half of the generation pipeline reproduce byte-for-byte from
  tracked inputs alone.
- Documented known limitations that weren't previously called out in the dataset
  card (rhetorical-channel variance on the low-confidence approval branch, a
  handful of items where the answer is visible in the question text).
- Cleaned up stale doc links and a retired-domain config file left over from an
  earlier taxonomy.
- Added CI (lint + tests) so future changes get checked automatically, and brought
  the generation scripts to a clean lint bar.

## Where things stand

- The freeze PR is open and includes everything above.
- Tracked separately for follow-up: re-porting the Gate-2 memory implementation
  onto the current taxonomy.
