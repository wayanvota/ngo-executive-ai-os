# End-to-End Test Report

Repository: `wayanvota/ngo-executive-ai-os`  
Branch: `test/e2e-harness-2026-09-11`  
Date: 2026-09-11  
Environment: macOS, Python 3.12.14 and 3.14.3; CI pinned to Python 3.12

## Result

PASS. All 20 fresh-copy and operating-contract categories passed using only the
Python standard library. Python compilation also passed. No credential, model,
private account, or network service was used.

Before this change, the repository had no executable validation. A missing
file reference, accidentally tracked private note, weakened approval rule, or
incomplete template could be published without a failing check.

## Test boundary

The harness uses Git's tracked-file list to assemble a temporary workspace with
no `.git` directory. All assertions run against that distribution copy, which
models the starter kit a user receives after cloning or downloading the
repository.

## User-behavior categories

| ID | Behavior | Final |
| --- | --- | --- |
| U01 | Install the required top-level structure | PASS |
| U02 | Name the license file that actually exists | PASS |
| U03 | Preserve role and source-discipline instructions | PASS |
| U04 | Preserve explicit human approval gates | PASS |
| U05 | Install every core memory file and folder | PASS |
| U06 | Install all six profile and review templates | PASS |
| U07 | Resolve the morning brief's memory inputs | PASS |
| U08 | Preserve donor-review operating columns and intent controls | PASS |
| U09 | Keep meeting drafts and memory edits approval-gated | PASS |
| U10 | Preserve evidence and tradeoff requirements in decision routines | PASS |

## Adversarial categories

| ID | Behavior | Final |
| --- | --- | --- |
| A01 | Publish no symbolic links | PASS |
| A02 | Publish no secret-shaped values | PASS |
| A03 | Publish only the README from private memory | PASS |
| A04 | Publish no user-specific absolute paths | PASS |
| A05 | Resolve every relative Markdown link | PASS |
| A06 | Publish no dangerous bootstrap command | PASS |
| A07 | Preserve source/evidence and decision placeholders in templates | PASS |
| A08 | Keep examples synthetic and source-qualified | PASS |
| A09 | Give every routine Purpose, Output, and Rules contracts | PASS |
| A10 | Exclude Git state while retaining all documented routines | PASS |

## Failures found and fixed

1. The README referred to `LICENSE.md`; the repository contains `LICENSE`.
2. `templates/weekly-review.md` contained decisions and assumptions but no
   evidence/source section. It now records evidence used, claims needing
   sources, and conflicting or stale information.
3. `templates/meeting-note.md` contained decisions and memory updates but no
   source trail. It now records source documents or recordings, claims needing
   verification, and update time.
4. The first harness pass reported 18 passes and two failures. One was a test
   path-calculation error, which was fixed. The added weekly evidence section
   exposed the same omission in the meeting-note template on the second pass.
   The final run passed all 20 categories.

## Verification evidence

```text
$ python3 -m compileall -q tests
exit 0

$ python3 -m unittest -v tests.test_e2e
Ran 20 tests in 0.048s
OK

$ Python 3.12.14 -m unittest -v tests.test_e2e
Ran 20 tests in 0.049s
OK
```

## Known boundary

The suite verifies the package, its instructions, and its human-control
contracts. It does not ask a live model to execute a routine because model
output would make pull-request CI variable, costly, and dependent on a private
credential. Live model evaluation remains a separate, explicitly authorized
quality check.
