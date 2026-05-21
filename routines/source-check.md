# Source Check Routine

## Purpose

Check whether donor-facing, board-facing, or public-facing claims are supported.

## Inputs To Review

1. the draft text
2. cited sources
3. source documents provided by the user
4. relevant memory files, treated as context only

## Output

Produce a claim table:

| Claim | Support Level | Source | Risk | Revision |
|---|---|---|---|---|

Support levels:

- `Verified`
- `Partially supported`
- `Unsourced`
- `Overstated`
- `Conflicting sources`
- `Out of scope`

Then provide a revised version that:

- keeps verified claims
- narrows overstated claims
- marks missing support as `[SOURCE NEEDED]`
- removes claims that create unnecessary risk

## Rules

- Do not treat memory as verification.
- Do not invent citations.
- Do not turn contribution into causality.
- Do not smooth over conflicting evidence.

