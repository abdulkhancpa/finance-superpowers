# RED transcript: transform

Scenario: `tests/scenarios/transform.md`. Sandbox (`sbx-task11-red`) seeded
with `tests/fixtures/tb_tidy.csv` copied to `engagement/work/tb_tidy.csv`
(the scenario's own wording places the input in `work/`, not `sources/`,
since it is already the tidy output of a prior `clean` step). Dispatched to
a fresh `general-purpose` subagent with **no finance-superpowers skill
text** — only the protocol's work-directory line followed by the scenario
prompt verbatim.

Input snapshot before the run (`sha256sum work/tb_tidy.csv` →
`746a1fa9b09f6199a5ee485cf98e3e6214e6824026c834d31e375cf95475302b`) matched
exactly after the run — the agent never wrote into its own input file, only
into `work/` (a new csv) and a `deliverables/` folder it created itself.

Every finding below is grounded directly in the run's own JSONL transcript
(`agent-a344a27e6beaf3469.jsonl`, 15 tool calls, tool-call order and tool
inputs/outputs — not a self-report), plus independent re-execution against
the actual delivered files (`build_workbook.py`,
`work/summary_by_entity_class.csv`, `deliverables/TB_Summary_CFO.xlsx`).
The 15 tool calls, in order: `find` (listing), `Read` of `tb_tidy.csv`, a
Python one-off computing raw per-entity totals directly from the source
rows, a second Python one-off computing the by-class breakdown and
comparing it to those same entity totals, `ls`/`find` (dirs), `mkdir
deliverables`, one `Write` of `build_workbook.py` (the entire load →
classify → aggregate → write-csv → build-3-sheet-xlsx pipeline in one
script), a `Bash` run of that script, an `openpyxl` read-back of the
`Summary` sheet, three `Edit` calls (a display-only capitalization fix for
"US"), a second `Bash` run of the script to regenerate outputs, a second
`openpyxl` read-back, and a final `Read` of the summary csv. No source file
was ever opened for writing.

This agent, like the `clean` RED run, was more careful than the brief's
generic prediction of "unformatted xlsx" — the workbook it built has a
cover sheet, frozen panes, accounting number formats, conditional
formatting, and an auto-filter. The violations below are the specific,
narrower gaps a reviewer can still find with independent recomputation.

---

## Violation 1: the class-mapping rule is hardcoded and asserted as fact, never declared as an assumption a reviewer can challenge

**Quote**, `build_workbook.py` line 27:

> `CLASS_MAP = {1: "Assets", 2: "Liabilities", 3: "Equity", 4: "Revenue", 5: "Expenses"}`

**Quote**, the only place this rule is explained anywhere in the
deliverable — the workbook's `Cover` sheet:

> "Mechanical rule: account class = the thousands digit of the account number."
> "No judgment applied and no threshold used — every account in the source file is included."

There is no `output/workpaper.md`, no "Assumptions" section, and no
document anywhere that frames the thousands-digit rule as a choice a
reviewer could disagree with (a different chart of accounts could use a
different digit, or a different digit-to-class mapping entirely). It is
stated in the same declarative voice as a fact about the source file
itself ("No judgment applied") rather than as a rule the preparer supplied.
Confirmed by `find . -iname "*workpaper*" -o -iname "*assumption*"` against
the full delivered sandbox: no match.

**Iron law broken:** discipline law #4, "no hardcodes" — "any value not
traced to a source file... is marked as an assumption in the workpaper's
assumptions section — never buried in a formula or script." The class map
is buried in the script and only described, never declared as an
assumption, in a cover note that is not a workpaper.

---

## Violation 2: input total vs. output total was never independently re-verified as one equation against the delivered artifact

**Quote**, the tool result printed when `build_workbook.py` first ran:

> `Grand total (all entities, all classes) = -0.00`

**Quote**, the same number, restated in the workbook's `Cover` sheet:

> "The combined total across all three entities is -0.00."

Both numbers come from the same in-process Python accumulator
(`grand_total`) that was built while aggregating rows into the pivot — the
same pass that produced the by-class summary. The source file's own
control total was never separately summed and stated as the left side of
an equation (`raw tb_tidy.csv total = X`); nor was the delivered workbook
ever reopened and its own written/computed cells re-summed to prove they
tie to that raw number. Confirmed independently for this transcript:
`python3 -c "..."` summing `work/tb_tidy.csv` directly gives `raw sum
-0.0` — a number that never appears anywhere in the deliverable as an
explicit, separately-labeled "input total." The two `openpyxl` read-backs
in the transcript (tool calls 9 and 14) print the `Entity Total` row's
formula text (`'=SUM(B5:B9)'`) — not Excel's evaluated result — so no
verification ever touched the actual value a spreadsheet application would
show; the only number ever inspected was the Python variable that built the
file.

**Iron law broken:** discipline law #6, "verify before 'done'" — "re-foot,
re-tie control totals, confirm outputs open cleanly — evidence before
claiming completion." A single number restated in two places, both derived
from the same in-memory computation, is not a conservation check; nothing
here reopens the delivered file and independently re-sums it against a
freshly-computed raw total.

---

## Violation 3: no output figure cites which source rows built it, and the workbook was hand-rolled with no standard writer

The only citation of the input anywhere across all three sheets (`Cover`,
`Summary`, `TB Detail`) is one blanket, whole-file mention, appearing
exactly twice:

**Quote**, `Cover` sheet: "Prepared 2026-07-27  |  Source: work/tb_tidy.csv"

**Quote**, `Summary` sheet subtitle: "Balances as provided in tb_tidy.csv;
account class = thousands digit of account number"

None of the 15 class/entity figures on the `Summary` sheet, and none of the
62 detail rows or their derived `Account Class` column on `TB Detail`, cite
which specific source row(s) rolled up into them — a reader cannot trace
any single cell back to a row range without re-deriving the classification
themselves. Separately, the workbook itself was built by 137 lines of
one-off `openpyxl` calls inside `build_workbook.py` (fonts, fills, borders,
column widths, freeze panes, autofilter all defined locally) rather than
through any single, shared writer — nothing here would keep a second
transform deliverable's formatting, cover structure, or citation
conventions consistent with this one.

**Iron law broken:** discipline law #1, "every number ties to a source" —
"every figure in a deliverable cites its file (and sheet/range or row). no
ungrounded numbers." A single file-level mention twice in a 3-sheet
workbook is not a per-figure citation.

---

## GREEN outcome

Fresh sandbox (`sbx-task11-green`), `work/tb_tidy.csv` re-copied and
re-hashed (`746a1fa9b0...` — matches RED's snapshot). Prompt prefixed with
the full `using-finance-superpowers` `SKILL.md`, the full
`skills/transform/SKILL.md` above, and a helpers pointer to
`scripts/`. Deliverables: `work/summary_by_entity_class.csv` (17 rows: 14
class-level + 3 entity-total, each with a `source_citation` column),
`manifest.json`, `output/tb_summary_by_entity_class.xlsx`,
`output/workpaper.md`.

**Chronology audited directly from the run's own subagent JSONL**
(`agent-a516cd486abec3c9e.jsonl`, not a self-report). The very first
assistant content block (index 4, before any tool call) reads, in full:

> "Using finance-superpowers discipline. Using transform to reshape
> summary by entity/account-class from work/tb_tidy.csv."
> "**Plan before work:**"
> "Threshold: This is a mechanical reshape (no judgment/estimation
> involved) — scope says "no threshold — mechanical." The only check
> that matters is conservation: independently-summed input control total
> must equal the re-summed output control total, with any difference
> itemized (not plugged)."
> "Assumption to record before aggregating: account class = the
> thousands digit of the account number (e.g., 1000s = assets, 2000s =
> liabilities, 3000s = equity, 4000s = revenue, 5000s = expenses) — this
> is the mapping rule agreed in scope, stated here before any row is
> touched."

This is both announce lines (G8) and the class-mapping assumption (closing
Violation 1) stated in writing before the first tool call of the run — the
next tool calls (index 5 `find`, index 6 `Read` of
`scripts/write_workbook.py`, index 10 `Read` of `tb_tidy.csv`) all come
after. The independent input control total was computed next (index 13-14,
`python3` printing "input control total (sum of balance column, all rows,
work/tb_tidy.csv): -0.0") — before the by-class aggregation script ran
(index 16), before `mkdir -p output` (index 22), before the manifest was
written (index 25), and before `scripts/write_workbook.py` was ever
invoked (index 27, the actual command:
`python3 "C:/.../scripts/write_workbook.py" manifest.json` →
`wrote output\tb_summary_by_entity_class.xlsx`) — closing Violation 3's
requirement that every xlsx go through the shared writer, with the call
itself visible in the tool-call record, not merely claimed.

After the workbook was written, the transcript's own text (index 29)
reads: "Now the required verification: reopen the delivered xlsx (not the
in-memory data) and re-sum its own written cells against the
independently-computed input control total." — followed (index 30) by a
fresh `openpyxl.load_workbook` and re-sum, before `output/workpaper.md`
was written (index 33). This closes Violation 2: the conservation check
runs against the saved artifact, not the accumulator that built it.

**Independently re-verified for this audit** (not taking the agent's
numbers on faith): re-opened `output/tb_summary_by_entity_class.xlsx`
fresh with `openpyxl` — `raw input total (independent, summed directly
from work/tb_tidy.csv) = -0.0`, `independent re-sum of the 14 class-level
rows in the delivered xlsx = -0.0`, `grand total cell as saved in the
delivered xlsx = 0`, `tb_detail sheet independent re-sum (62 rows) =
-0.0`. All four figures agree exactly with each other and with the
workpaper's own stated equation. The cover sheet, read back independently,
lists both `Sources` (one entry: `work/tb_tidy.csv`, with row range and
entity count) and `Assumptions` (three entries, including the class-mapping
rule, verbatim-consistent with `manifest.json`'s `cover.assumptions`).

**G1**: `sha256sum work/tb_tidy.csv` after the run matches the before-run
hash exactly — confirmed independently.
**G2**: every figure in `work/summary_by_entity_class.csv` and
`output/workpaper.md` §2 carries its own `work/tb_tidy.csv` row or
row-range citation, including a non-contiguous case (`rows 61,63`) called
out by name rather than mis-stated as a range — closes Violation 3.
**G3**: `output/workpaper.md` §4 "Open items: None," fully tied out by
§5's four-way equation; no plug anywhere.
**G4**: threshold stated in the first assistant message, before any tool
call — chronology-confirmed above, not just document order.
**G5**: `output/workpaper.md` §3 and the workbook cover both list the
class-mapping rule, the no-threshold decision, and the holdco
no-Revenue-row structural fact as assumptions.
**G6**: `output/workpaper.md` §5 shows the full equation (input control
total == class-level re-sum == entity-total re-sum == grand-total cell ==
detail-sheet re-sum) and states the reopen-and-re-sum was performed on the
saved file, not in-memory data.
**G7**: `output/tb_summary_by_entity_class.xlsx` was produced by the
actual `scripts/write_workbook.py manifest.json` invocation visible in the
tool-call record (index 27) and reopened cleanly for this audit with
`openpyxl.load_workbook(..., data_only=True)`.
**G8**: confirmed above — both announce lines are the first content
block, before any tool call.

**Verb-specific checks, independently re-verified against the actual
delivered files:**
- Workpaper §5.4 states the equation "input control total (-0.00) ==
  class-level re-sum from the delivered file (-0.00) == entity-total
  re-sum (0.00) == grand total cell (0.00) == detail-sheet re-sum (-0.00)"
  — independently reproduced above, exact match.
- Class mapping appears in the assumptions section of both
  `output/workpaper.md` §3(1) and the workbook cover sheet's Assumptions
  block — not merely described in a note.
- `output/tb_summary_by_entity_class.xlsx` exists, was produced via
  `scripts/write_workbook.py` (JSONL tool call, index 27), the cover sheet
  lists sources, and the file reopens cleanly with `openpyxl`.

### Result: no REFACTOR needed

All three RED violations closed on the first GREEN pass, confirmed by
JSONL chronology (not self-report) and by this audit's independent
re-computation against the actual delivered files: the class mapping was
declared as an assumption in writing before a single row was read
(closes V1); the conservation check re-opened the saved workbook and
re-summed its own written cells against an independently-computed input
total, rather than trusting the in-memory accumulator (closes V2); every
figure carries its own source row/range citation and the workbook was
built exclusively through `scripts/write_workbook.py` (closes V3). No new
loophole was found.
