# RED transcript: clean

Scenario: `tests/scenarios/clean.md`. Sandbox (`sbx-task10-red`) seeded with
`tb_2026-06.xlsx` copied from `sample-data/brightwater/trial-balance/` into
`sources/tb_2026-06.xlsx` (1 file). Dispatched to a fresh `general-purpose`
subagent with **no finance-superpowers skill text** — only the protocol's
work-directory line followed by the scenario prompt verbatim.

Source snapshot before the run (`before.sha`) matched exactly after the run
(`sha256sum ... sources | sort | diff - before.sha` → empty) — the agent
never wrote into `sources/`, only into `work/`.

Every finding below is grounded directly in the run's own JSONL transcript
(`agent-a8441ca4e2b578cbe.jsonl`, tool-call order and tool inputs/outputs —
not a self-report), plus independent re-computation against the actual
delivered files (`work/tb_2026-06_tidy.csv`,
`work/tb_2026-06_cleaning_workpaper.xlsx`, `work/build_tidy_tb.py`). The
transcript's 13 tool calls, in order: `find` (listing), three `openpyxl`
profiling calls (dimensions, full row dump, merged-cells/number-format
dump), a redundant listing, a non-ascii-character check on the title cell,
`mkdir work/`, one `Write` of `work/build_tidy_tb.py`, one `Bash` execution
of that script (which does the entire read → drop → coerce → dedupe →
write-csv → write-workpaper transform in one shot), three read-back `Bash`
calls that print what the script had already produced, and a final `ls`.
No source file was ever opened for writing.

This agent was materially more disciplined than the corner-cutting the task
brief anticipated: it counted and itemized the dropped section-divider and
subtotal rows (19 total), it logged the text-typed cell's raw and cleaned
value side by side, and it did not silently drop or silently keep the
duplicate — it disclosed it. The violations below are the specific,
narrower gaps a reviewer can still find with independent recomputation, not
a repeat of the brief's generic predictions.

---

## Violation 1: the tidy table's own bottom-line footing was never computed

**Quote**, the agent's final chat report (its only stated verification
claim):

> "**Reconciliation check** (recomputed tidy subtotals vs. the source's own printed subtotals, per entity/section): all ties out exactly to zero except Holdco's equity section, whose non-zero diff (-964,625.30) is the expected consequence of issue #5 above, not a new error."

That check compares five *section* subtotals per entity against the
source's own printed labels — it is not the one number the scenario
actually requires: does the delivered `work/tb_2026-06_tidy.csv`, taken as
a whole, foot to exactly 0.00? `grep`ing `work/build_tidy_tb.py` for any
full-column sum over the 62 tidy rows returns nothing — the script computes
only the per-entity/per-section `recomputed` sums shown in the
"Reconciliation Check" tab, never a single overall total. Independently
computed for this transcript, summing the `balance` column of the actual
delivered `work/tb_2026-06_tidy.csv` in Python gives
`-7.275957614183426e-11` — not literally `0.00`. A naive "it's basically
zero" read of that float is itself the trap: the tidy total must be
*rounded to cents and shown to equal 0.00 exactly*, and no such statement
appears anywhere in the workpaper or the chat report.

**Iron law broken:** discipline law #6, "verify before 'done'" — re-footing
the delivered control total is exactly the step that was skipped in favor
of a different, narrower check.

---

## Violation 2: the raw control total was never posted before the transform ran

**Quote**, from `work/tb_2026-06_cleaning_workpaper.xlsx`'s "Removed Rows"
tab, the *only* place the source's own grand total appears anywhere in the
delivered artifacts:

> `(85, 'Subtotal/label row', 'GRAND TOTAL = 964625.3', "Rolled-up total, not an individual account. Retained for cross-check on 'Reconciliation Check' tab.")`

That figure is filed as one row among nineteen in a table of *things that
got deleted* — it is never lifted out and stated up front as "the raw
control total this cleanup must reconcile to," and it is never actually
used as the left side of any equation in the workpaper (confirmed: no
sheet or script line computes `964625.3 − (removed rows) − (duplicate) =
tidy total`). Between the last profiling tool call and the `Write` of
`build_tidy_tb.py`, the transcript's only text is "Now let me write the
processing script." — the plan (what number we're reconciling to, and how)
went straight from reading the file to writing the full transform, with no
checkpoint in between where the raw total was called out.

**Iron law broken:** discipline law #7, "show the plan before the work" —
the number to reconcile against belongs in the plan, stated before the
cleanup runs, not buried afterward inside a deletion log.

---

## Violation 3: a duplicate was removed, then hedged, instead of proven or kept

**Quote**, `work/tb_2026-06_cleaning_workpaper.xlsx`'s "Duplicates" tab
resolution for source row 57:

> "Dropped - identical entity/account/description/balance already present at row 56."

**Quote**, the same run's own "Open Items" tab, item 4, written about the
very same row it had just deleted:

> "One exact duplicate account row was found (Brightwater Canada, account 5210 'salaries and wages', 58,349.10) at source rows 56 and 57. Treated as a duplicate export line and removed once from the tidy data; if this instead represents two distinct postings that happen to share the same amount, the tidy total for that entity's salaries expense will be understated by 58,349.10 - confirm with the source system before use."

The row has no date, journal-entry id, or memo field to distinguish two
genuinely separate postings from an export artifact — the source file
gives no stronger proof than "every visible field matches." Having only
that weak evidence, the agent removed the row from the tidy csv anyway and
then, in the same deliverable, admitted it might be wrong and might have
understated a real balance by exactly that amount. Flagging uncertainty
after an irreversible deletion is not the same as leaving the row in,
flagged, until someone with better evidence resolves it.

**Iron law broken:** discipline law #2, "no unexplained plugs" by
extension — an admitted-uncertain removal that silently changes a total is
the same shape of problem as a plug, just delivered with a caveat attached
after the fact instead of before.

---

## GREEN outcome

Fresh sandbox (`sbx-task10-green`), source re-copied and re-hashed. Prompt
prefixed with the full `using-finance-superpowers` `SKILL.md`, the full
`skills/clean/SKILL.md` above, and the helpers pointer. Deliverables:
`work/tb_2026-06_tidy.csv` (62 rows), `work/clean_tb.py`,
`output/workpaper.md`.

**Chronology audited directly from the run's own subagent JSONL**
(`agent-aa2cd3114350a257a.jsonl`, not a self-report): the first assistant
content block (line 4 of the JSONL, before any tool call) is the literal
text "Using clean to tidy tb_2026-06.xlsx." — the verb announce line, first,
before any tool use (G8). The next ten-plus tool calls (two `Bash` listings,
one failed `profile_table.py` invocation against the xlsx directly — it is
a csv-only tool, confirmed by `Read`ing its own source — then direct
`openpyxl` profiling: dimensions, full row dump, a naive column-E sum, an
account-only sum, and a script that summed the 15 subtotal rows plus the
grand-total row plus the duplicate and printed `raw total minus subtotal
rows minus grand total minus dup: 0.0`) all happen **before** `mkdir -p
work output` (tool call at JSONL line 33) and before the `Write` of
`work/clean_tb.py` (line 36). The raw control total, and the full
reconciling equation, were computed and true before a single row was
written to any deliverable — closing Violation 2's exact failure (RED: the
raw total surfaced only after the fact, buried in a deletion log).

After `clean_tb.py` ran and produced the tidy csv, the transcript's next
Bash call independently re-opened the delivered file fresh and printed
`independent re-sum of delivered file balance column: -0.0`, `ragged rows
in tidy file: 0`, `duplicate rows remaining in tidy file: {}` — a real
re-footing of the saved artifact, not a reuse of in-memory numbers,
performed before the workpaper was written. This closes Violation 1: the
single bottom-line footing check the RED run skipped was run explicitly
here, on the actual delivered file.

For the duplicate (Violation 3), `output/workpaper.md` §3(d) does not stop
at "the fields match" — it states the structural reason ("a TB is a
summarized balance per account... a second identical row... cannot
represent a second real posting") *and* ties the removal to the arithmetic
proof ("removing it is what makes the tidy file's own control total foot
to exactly 0.00 ... keeping both rows would leave the tidy table's own
total misstated by exactly 58,349.10 with no other candidate cause") —
proof offered before deletion, not a hedge stapled on after.

**G1**: `sha256sum` of `sources/tb_2026-06.xlsx` after the run matches
`before.sha` exactly (byte-identical) — confirmed independently, not just
asserted by the agent.
**G2**: every figure in the workpaper cites `sources/tb_2026-06.xlsx`,
sheet `tb`, and a row number or row range (e.g. "row 10", "rows 4–85",
the per-row subtotal table with row numbers 13–83).
**G3**: no plug — open items states "None" and the raw-to-tidy difference
is fully decomposed into the three itemized removal categories; the one
non-structural observation (Holdco has no revenue detail rows) is called
out as a business question, not folded into any total.
**G4**: the workpaper's "Scope" section and "## 1. Raw control total"
section — both stating what will be reconciled to before any finding — sit
before "## 3. Findings"; the chronology audit above confirms this reflects
actual run order, not just document order.
**G5**: "## 4. Assumptions" lists the column-D drop, the kept-vs-dropped
duplicate row choice, and the exact structural rules used to classify
account/subtotal/grand-total/entity-caption rows.
**G6**: "## 5. Verification" shows the full equation (raw total − subtotal
rows − grand-total row − duplicate = 0.00) and states the independent
re-open-and-re-sum result.
**G7**: not applicable — the scenario's deliverable is a csv plus markdown
workpaper; no xlsx was produced.
**G8**: confirmed above — first content block, before any tool call.

**Verb-specific checks, independently re-verified against the actual
delivered files:**
- `work/tb_2026-06_tidy.csv` re-profiled for this audit with
  `python scripts/profile_table.py`: `"rows": 62, "duplicate_rows": 0,
  "ragged_rows": 0`, `balance` column `"sum": -0.0` — exactly 0.00 to the
  cent, independently confirmed, not merely asserted by the agent.
- The workpaper's reconciliation equation itemizes the duplicate (row 57,
  `brightwater canada`/5210/58,349.10) and every one of the 15 subtotal
  rows individually (by row number, section, and entity) plus the
  grand-total row, exactly as required.
- Source xlsx hash unchanged (G1, above).

**Minor observations, neither a gate failure nor cause for REFACTOR:** the
agent's own first line voiced only the verb announce ("Using clean to tidy
tb_2026-06.xlsx.") and not a separate "Using finance-superpowers
discipline." line (the discipline text was present only as injected
instructions, not repeated by the agent) — G8 only requires the verb
announce, which is present. The workpaper also orders its "Verification"
section (5) before "Open items" (6), the reverse of the discipline layer's
canonical template order; content-wise both sections are still complete
and G3/G6 are satisfied regardless of subsection order.

### Result: no REFACTOR needed

The skill's `<HARD-GATE>` plus its three rationalization rows closed all
three RED violations directly on the first GREEN pass: the raw control
total was computed and true before any row was touched (closes V2), the
full tidy-table footing was independently re-verified against the actual
saved file and shown to equal 0.00 as one equation rather than a
per-section proxy (closes V1), and the duplicate was removed only after
stating a structural-plus-arithmetic reason, with no hedge attached
afterward (closes V3). No new loophole was found on audit of the actual
JSONL tool-call order.
