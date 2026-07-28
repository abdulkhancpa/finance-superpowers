# End-to-end mini-engagement: Brightwater Distribution Co.

> **Note (v1.1, 2026-07-28):** `tb_2026-06.xlsx` was regenerated for economic
> plausibility, and `gen_data_room.py`'s per-entity expense rows (previously
> one shared list copy/pasted across all three entities) were fixed, **after**
> this engagement was run. This file and the recorded run below are not
> re-run. The TB-derived figures in `output/workpaper.md`, `output/review.md`,
> and `output/deal_memo.md` (open items #3 and #5, and the corresponding
> tie-point/verdict rows) have been updated with minimal, truthful edits to
> reflect the current fixture and to note where a previously-flagged issue
> (the copy/paste bug) is now fixed; everything else in those files, and all
> of `engagement/work/` (including `run-log.jsonl`), is left as the
> unmodified historical record of the run against the original fixture.

Acceptance test for spec success criterion 2 — the whole finance-superpowers
library chained on a single realistic engagement, checked by an independent
reviewer, verified against ground truth planted in the Brightwater fixtures.

## Setup

A sandbox `engagement/sources/` was seeded with the full Brightwater fixture
set: `trial-balance/tb_2026-06.xlsx`, all three `subledger-tie/` CSVs, and the
full 18-file `data-room/` tree (22 source files total). Sources were
sha256-hashed before the run. Helper scripts (`write_workbook.py`,
`profile_table.py`) were copied alongside so no run touched the real repo.

Engagement prompt given to the preparer agent (deal lead persona):

> Brightwater Distribution Co. is being acquired. Perform initial financial
> diligence: understand the data room, verify AR ties, explain the fy2025
> revenue movement, and deliver a findings memo. I'm the deal lead;
> explanation threshold $250,000 for diligence findings, $5,000 for the AR
> rec.

## Run 1 (RED for this criterion)

A `general-purpose` subagent was dispatched with all ten skills' text inline
plus the engagement prompt, free to chain verbs itself. It ran
brainstorm → understand → clean → reconcile → transform/analyze → document,
correctly found the duplicate batch (`b-0621`, $118,500.00) and the timing
item (`inv-20241` / `je-7-0043`, $35,000.00), and correctly tied the revenue
gross figure ($49,200,000) to the reported income statement figure
($48,950,000) via the $250,000 freight reclass in `notes_fy2025.md`. It also
surfaced both required data-room red flags (Northern Foods change-of-control,
unaccrued litigation).

It did **not** find the third planted AR item. Its own workpaper disclosed:

> "a full scan of all 207 tidy rows for a two-adjacent-digit swap that would
> produce exactly a $9,000 difference returns 34 candidate rows... with no
> corroborating second source... to identify which — if any — is the actual
> erroneous entry."

An independent review subagent (review skill only) reperformed the whole
engagement and confirmed everything above, including — on its own
independent re-scan — the same conclusion: 35 candidate rows, no
corroboration, "not identified, and this is the correct outcome, not a
miss." Both the preparer and the independent reviewer missed the transposition
on `inv-19877` (Stonebridge Market: recorded $45,000.00 vs. an implied
$54,000.00, exactly the $9,000 residual).

*(Footnote on the 34 vs. 35 count: the two agents' scans were not the same
method and neither script survived for a byte-for-byte diff. A third,
independent recompute for this note, using only genuine adjacent-integer-digit
swaps against the tidy 207-row population, found 25 rows whose swap produces
an exact $9,000 difference (including `inv-19877` itself) — a third distinct
number. All three counts depend on exactly how "digit swap" is defined
(adjacent digits only vs. any two digits, integer part only vs. including
cents, magnitude-only vs. signed direction), so the 34-vs-35 discrepancy is
recorded as unreconciled/methodology-dependent rather than resolved to a
single true count. It does not affect the conclusion: none of the three
scans used narrowing, and narrowing — not the raw candidate count — is what
run 2's fix actually changed.)*

## Fix

`skills/reconcile/SKILL.md` step 2 was under-specified for a busy,
multi-source engagement: it named the divisibility-by-9 hint but did not
instruct narrowing the candidate pool before testing it, so a blind scan
across the whole population returned dozens of coincidental hits and the
chase stalled there. Added to step 2: narrow to the rows that break the
population's own pattern (irregular key/name, round amount where the rest
carry cents, an entry outside a systematic sequence) and eliminate
candidates already explained by other found items *before* testing the
residual — a scan across the whole population is not a search. A
rationalization-table row was added quoting this run's actual workpaper and
review verdict verbatim, so the failure is grounded in a real transcript, not
invented.

## Run 2 (GREEN)

Fresh sandbox, sources re-copied and re-hashed (matches run 1's pre-hash).
Same ten skills, reconcile updated. The preparer this time:

- narrowed the AR subledger to its irregular/manually-keyed rows (outside the
  systematic `inv-195xx`–`197xx` sequence), found two digit-swap candidates
  fitting the $9,000 magnitude, and correctly rejected the wrong-direction one
  (a surviving `b-0621` invoice) in favor of `inv-19877` (Stonebridge Market,
  $45,000.00 recorded vs. $54,000.00 implied) — closing the reconciliation to
  the penny while still honestly disclosing that the subledger's $45,000.00
  is believed correct (with the GL carrying the transposed $54,000.00), a
  conclusion not independently confirmed by a third source (no Stonebridge
  invoice/sales order in the data room).
- correctly bridged FY2025 revenue: gross tie $49,200,000 (TB extracts =
  `monthly_revenue_2025.csv`) → reported $48,950,000 via the $250,000 freight
  reclass (`notes_fy2025.md`), with the remaining $2,143,000 of growth
  disclosed as an above-threshold open item (not a named driver) rather than
  folded into "other."
- surfaced both required data-room red flags: the Northern Foods MSA §11.2
  change-of-control consent clause (customer is ~22% of revenue) and the
  unaccrued, counsel-assessed-probable Carter Mechanical litigation
  ($400,000–$600,000) against `balance_sheet_fy2025.md`'s "no litigation or
  contingency reserves are recorded."
- disclosed, honestly and without prompting, a minor process slip: one
  non-financial file (`data-room/index_readme.md`) was opened one tool call
  before the brainstorm threshold/scope was formally posted — logged in
  `run-log.jsonl` rather than hidden, and confirmed by the reviewer to
  contain no dollar figures.

Verb chain used: **brainstorm → understand → clean → reconcile → analyze →
document** (transform folded into analyze — the revenue schedules needed
aggregation and a disclosed reclass, no coa/fx remapping). Deliverables:
`ar_gl_reconciliation.xlsx`, `revenue_bridge_fy2025.xlsx`, `workpaper.md`,
`deal_memo.md` in `output/`; tidy CSVs, a cleaning log, and `run-log.jsonl`
(a chronology log the preparer was asked to append to honestly, in real
time, so its ordering claims could be audited rather than taken on faith) in
`work/`.

### Independent review (run 2)

A second subagent, given only the review skill's text and pointed at the
run-2 `output/` folder plus the same sources, posted its claims checklist
before recomputing anything, then independently recomputed 36 line items
directly from source files (not from the preparer's own `work/` CSVs):
34 pass cleanly, 2 pass-with-caveat: row 8, the transposition (its arithmetic
and direction are confirmed; the subledger's $45,000.00 is believed correct,
with the GL carrying the transposed $54,000.00, but as the workpaper itself
says, this is not independently provable from sources in hand), and row 36, the
threshold-before-figures claim (the thresholds were stated at the point
claimed, but a non-financial source file was read for content one step
earlier — a minor, self-disclosed sequencing slip, not a fabrication). It
verified every cited
filename exists in `sources/` (no fabricated citations), reopened both xlsx
files fresh with `openpyxl` and confirmed they foot to the workpaper's own
figures, and explicitly confirmed all three planted AR items (duplicate,
timing, transposition) plus the revenue reclass and both data-room red flags.
It also independently re-ran a broader whole-population digit-swap scan (35
hits) and concluded that the preparer's decision to narrow to manually-keyed
rows first — rather than treat every mathematical hit as equally plausible —
was correct.

## Success-criterion verification (independent of both agents)

- **Folder shape**: `engagement/{sources,work,output}` present as expected.
- **Sources unchanged**: sha256 of all 22 files under `engagement/sources/`
  compared before vs. after the run 2 — identical.
- **Deliverables open cleanly and came from `write_workbook.py`**: both
  `ar_gl_reconciliation.xlsx` and `revenue_bridge_fy2025.xlsx` reopen with
  `openpyxl` with the exact cover-sheet shape `write_workbook.py._write_cover`
  produces (title/engagement/date/Sources/Assumptions blocks), and each has a
  matching `work/manifest_*.json` consumed by `write_workbook.py`'s `main()`.
- **Workpapers**: threshold stated in section 1, before any figure; every
  finding cites its source file and row/range; six assumptions listed;
  eight open items each with amount, suspected nature, and a named document
  that would close it; a verification section re-footing every schedule and
  confirming the reopened xlsx files.
- **Ground truth, independently recomputed by the task runner (not trusting
  either agent's arithmetic)**:
  - AR: raw subledger $2,764,449.50 vs. GL $2,619,949.50 → $144,500.00
    difference = duplicate batch `b-0621` ($118,500.00) + timing `inv-20241`
    ($35,000.00, provable via `je-7-0043`) − transposition `inv-19877`
    ($9,000.00). Confirmed exactly by direct computation against the
    fixtures.
  - Revenue: TB extracts' revenue accounts (4000+4100 across US/Canada/
    Holdco) sum to $49,200,000; income statement fy2025 revenue is
    $48,950,000; the $250,000 gap is exactly the freight reclass disclosed in
    `notes_fy2025.md`. Confirmed exactly.
  - Data-room red flags: Northern Foods MSA §11.2 change-of-control consent
    clause (customer ≈22% of revenue) and the $400,000–$600,000 probable,
    unaccrued Carter Mechanical litigation vs. `balance_sheet_fy2025.md`'s
    "no litigation or contingency reserves are recorded" — both confirmed
    present in the fixtures and both surfaced in the run-2 deliverables.
  - Trial balance's planted hazards (merged title `A1:E2`, subtotal/caption
    rows sharing column E with their own detail, duplicate Canada `5210`
    row, text-typed US `1400` cell `'77,614.00'`) — all four confirmed
    present in the fixture and all four named in the run-2 workpaper's
    understand section.
- **Reviewer's reperformance passes**: 34/36 independently recomputed line
  items pass cleanly; 2 pass with caveat — the transposition's unprovability
  of the *true* amount (row 8) and the source-read-before-threshold
  sequencing slip (row 36) — both of which the preparer and reviewer already
  flag honestly rather than overclaim.

## What was fixed

| Skill | What failed | What changed |
|---|---|---|
| `reconcile` | Step 2's transposition guidance named the divisibility-by-9 hint but not how to narrow a large candidate pool before testing it; a blind whole-population scan returned ~34 coincidental hits and the chase stopped there (confirmed independently by a separate reviewer subagent's own re-scan) | Added narrowing instruction (isolate pattern-breaking rows, eliminate already-explained candidates, then test what's left against the residual) plus a rationalization-table row quoting this run's actual workpaper/review text verbatim |

No other skill required a fix in this run. `transform` was exercised in a
lighter form (folded into `analyze`'s aggregation) rather than a distinct
coa/fx remap, since this engagement had no such remapping to do —
consistent with `transform`'s own scope ("the data is right; the shape is
wrong").

## Concerns / residual risk

- The transposition's *true* amount (the subledger's $45,000.00 for
  `inv-19877`, with the GL's $54,000.00 being the mis-keyed figure) is not
  independently provable from the fixtures in hand by the preparer/reviewer
  alone — both disclose this honestly rather than overclaim it, which is the
  correct posture, but a real engagement would still need the underlying
  sales document to close it.
- The reconcile fix was validated by one fresh end-to-end re-run, not by a
  dedicated RED/GREEN pair scoped to the reconcile skill in isolation (that
  isolated pair already exists from Task 12 and continues to pass — see
  `tests/scenarios/reconcile.md` / `tests/transcripts/reconcile-red.md`).
  This task's fix was validated in the harder, busier, multi-workstream
  context where it actually failed.
- **Undisclosed confound in the RED/GREEN pair above, caught on task review,
  not by me at the time**: `skills/reconcile/SKILL.md`'s rationalization
  table has named this exact fixture's answer — invoice `inv-19877`, recorded
  $45,000.00 vs. an implied $54,000.00 — since Task 12's commit `e412bf4`,
  well before this task's run 1. Both engagement agents in both runs were
  handed that skill text inline, meaning both were *given* the answer in
  their own instructions before they ever opened a source file. Run 1 still
  missed it despite that, which is mildly reassuring (the pre-existing text
  wasn't sufficient on its own), but run 2's pass is **not a clean test of
  whether the new narrowing heuristic generalizes** to an engagement that
  doesn't already contain its answer inside the skill text it was given. A
  real test of generalization would need either a fixture whose rationalization
  table doesn't already spell out the specific invoice/amounts, or a version
  of the skill text with that one rationalization row held back. This was not
  done here, and the fix should be read as "did not obviously help despite
  being handed the answer twice" rather than "proven to generalize."
