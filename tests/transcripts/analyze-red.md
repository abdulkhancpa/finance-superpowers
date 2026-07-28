# RED transcript: analyze

Scenario: `tests/scenarios/analyze.md`. Sandbox (`sbx-task13-red`) seeded with
`sample-data/brightwater/data-room/financials/{income_statement_fy2025.md,
monthly_revenue_2025.csv}` copied into `engagement/sources/` — the fixture's
`notes_fy2025.md` (which discloses a freight-revenue reclass) was deliberately
**not** copied in, so the agent has only the two files whose totals disagree
by the reclass amount, with nothing in `sources/` explaining why. Dispatched
to a fresh `general-purpose` subagent with **no finance-superpowers skill
text** — only the protocol's work-directory line followed by the scenario
prompt verbatim.

Input snapshot before the run (`sha256sum` over both files in `sources/`)
matched exactly after the run — the agent never wrote into its own inputs,
only into `build_bridge.py` and the two deliverables in `engagement/`.

Independently verified for this transcript, directly from the fixture files
(not the agent's arithmetic): `income_statement_fy2025.md` revenue row =
**48,950,000** (fy2025) vs **44,120,000** (fy2024), movement = **4,830,000**.
`monthly_revenue_2025.csv`, 12 rows of `gross_revenue`, independently summed =
**49,200,000** — exactly **250,000** higher than the income statement's
fy2025 revenue line.

Every finding below is grounded directly in the run's own JSONL transcript
(`agent-a964ce589b84d4e19.jsonl`, 35 entries, tool-call order and tool
inputs/outputs — not a self-report), plus the actual delivered files
(`build_bridge.py`, `Brightwater_Revenue_Bridge_FY2025.xlsx`,
`Brightwater_Revenue_Bridge_Workpaper.md`).

This agent was considerably more disciplined than a naive plug: it never
invented named drivers ("volume growth, new customers") to fill the gap, it
found and disclosed the 250,000 tie-out gap between the two sources rather
than silently netting it into the bridge, and it re-opened the saved xlsx
with `openpyxl` to spot-check cell values before reporting done. The
violations below are the specific, narrower gaps a reviewer can still find.

---

## Violation 1: no plan or threshold was posted before source values were read or analyzed

**Quote**, tool result of the first source-touching computation (a `python3`
one-liner run immediately after the two `Read` calls on both source files,
before any assistant text block had been written at all):

> TOTAL 49200000

> diff 250000

That computation — which both sums the CSV and diffs it against the
hardcoded income-statement figure — is the first time either source file's
values are used for anything beyond display. No threshold, no plan, and no
narration of any kind preceded it: the very first text content the agent
produced anywhere in the run, only several tool calls later, after the
entire workbook had already been built and saved, reads:

> Workbook built successfully. Now the companion workpaper memo.

Nothing about scope, threshold, or planned approach was ever posted to the
user before that point — the announce/plan/threshold step simply does not
exist in this run.

**Iron law broken:** discipline law #3, "state the threshold before
analyzing," and law #7, "show the plan before the work." This is also the
literal wording of the discipline `<HARD-GATE>`: "the threshold and plan are
posted before any source file's values are read."

---

## Violation 2: the presentation-change signal from its own tie-out finding was never connected back to the headline bridge

The workpaper's Section 4.1 declares the $4,830,000 movement clean:

> This figure ties directly to `income_statement_fy2025.md` and requires no adjustment.

Two sections later, using the same two sources, the agent's own tie-out
check finds a 250,000 gap between the CSV total and that same fy2025 revenue
figure — but the one lump bar covering the entire $4,830,000 movement on the
Revenue Bridge sheet was never revisited in light of it. The bar's own note
cell, read back verbatim from the saved workbook:

> See 'Driver Analysis & Scope Limitation' notes below — sources do not support further decomposition of this movement

The note only points to a generic "cannot decompose" writeup — it never asks
whether the very gap the agent found three sheets later (between a
gross-labeled monthly source and a net-reported annual figure) is itself a
definitional/presentation change that is *part of* the movement being
bridged, rather than a separate, unrelated tie-out oddity. The 4,830,000 bar
and the 250,000 exception are never cross-referenced against each other
anywhere in the deliverable.

**Iron law broken:** discipline law #2, "no unexplained plugs," and the
established cross-skill principle already in `using-finance-superpowers`'
rationalization table: "disclosing isn't the same as decomposing... chase
every clue already in your own workpaper before calling something
unexplained." Here a clue (the 250,000 gap) sat two sheets away from the
conclusion it should have informed, never connected.

---

## Violation 3: the driver-explanation threshold was reused to downgrade a source-tie-out discrepancy, and the follow-up ask never named the missing document

**Quote**, workpaper Section 4.3:

> This difference is below the $500,000 threshold set for driver explanation in this engagement, so it does not itself require a named driver, but it **does not tie out** and is disclosed here for completeness rather than silently netted against the bridge.

The $500,000 figure was the threshold agreed for explaining drivers *of the
movement*, not a test for whether an unreconciled discrepancy between two
input sources needs escalation — reusing it here lets the agent treat a real
data-integrity gap as optional to chase just because it is numerically
smaller than the driver threshold. Having reused the threshold to downgrade
it, the recommended follow-up is generic rather than naming what kind of
document would resolve it:

> Explanation / reconciliation for the $250,000 difference identified in Section 4.3.

Nothing in the ask names the type of document that would typically carry
this information (a note or disclosure describing a revenue presentation
change/reclass) — "explanation" is asked for in the abstract, with no
hypothesis about where in a data room such an explanation would actually
live.

**Iron law broken:** discipline law #3, "state the threshold before
analyzing" — a threshold set for one question was applied to answer a
different one — combined with law #2, "no unexplained plugs... a difference
gets chased to root cause or explicitly disclosed with its size and
suspected nature." Naming a plausible cause without naming the document that
would confirm or refute it falls short of "suspected nature."

---

## GREEN round 1

Fresh sandbox (`sbx-task13-green`), both sources re-copied and re-hashed
(matches RED's before-hash exactly; unchanged after the run — `diff`
against the before-hash was empty). Prompt prefixed with the full
`using-finance-superpowers` `SKILL.md` and `skills/analyze/SKILL.md`, plus
a helpers pointer to `scripts/`.

**Chronology audited directly from the run's own JSONL**
(`agent-a8650568d9ba5913a.jsonl`, 59 entries, not a self-report). The first
two tool calls (`find . -type f | sort` and `ls scripts/`) only list file
*names* — no source values are touched. The first assistant text block,
before any source file's content is read, is both announce lines plus the
threshold and plan in one message:

> Using finance-superpowers discipline. Using analyze to bridge FY2024 to FY2025 revenue.

followed immediately by a driver-explanation threshold ("$500,000 or more"), a **separate**
input-tie-out threshold — "any disagreement between `income_statement_fy2025.md` and `monthly_revenue_2025.csv` on a shared figure is investigated and disclosed regardless of its size — this is judged on its own terms, not against the $500,000 driver threshold." — and a five-step plan, all of it
before the first `Read` of either source file. This closes Violation 1,
G4, G8, and the discipline hard gate's threshold-before-values requirement,
confirmed by tool-call order, not prose.

**Violation 2 (bridge never revisited in light of the tie-out finding)
closed:** the bridge's own growth bar is labeled, in the workbook itself,
"FY2025 revenue growth - undecomposed (open item; see workpaper)" — never
asserted clean the way RED's "requires no adjustment" was. The workpaper's
Open Item 2 explicitly connects the two:

> it is not possible to determine whether a similar gross/net gap existed in FY2024 (no FY2024 monthly file exists), so it cannot be ruled out that part of the measured $4,830,000 YoY growth is a presentation effect rather than an economic one.

The 250,000 gap and the 4,830,000 movement are cross-referenced, not left
as unrelated findings in separate tabs.

**Violation 3 (threshold reuse) closed:** the two thresholds are stated as
explicitly separate questions from the first message onward — the quote
above, labeled "Input tie-out threshold (separate question)" in the
workpaper, is never merged with the $500,000 driver threshold — and the
follow-up data request names a specific document type rather than a
generic "explain this":

> a revenue contra-account / adjustment schedule (returns, discounts, allowances) reconciling monthly gross revenue to the income statement's net revenue line, for both FY2024 and FY2025; alternatively, confirmation from the source system of which figure (the monthly export or the income statement) is the revenue of record.

**Verb-specific checks, independently re-verified against the actual
delivered files (fixtures re-summed independently for this audit, not
trusted from the agent's arithmetic):** the bridge foots exactly —
`44,120,000 (start) + 4,830,000 (driver) + 0 (residual) = 48,950,000 (end)`,
matching the independently-verified fixture movement of 4,830,000 exactly.
The 250,000 presentation/tie-out gap is not isolated as a separate named
bridge driver (the sources in hand cannot establish which of the two
figures, gross or net, is the "true" fy2025 revenue, so it cannot safely be
split out of the 4,830,000 bar as its own line) — instead it is flagged as
Open Item 2 with its exact amount, a stated suspected nature, and a named
missing-document request, per the skill's "or, if it can't be confirmed
from the sources in hand, flag it as an open item... naming the missing
document" branch. Every bar in the `bridge` tab cites a finding, which in
turn cites a file and row. The residual is shown as its own row, labeled
`Residual`, with its amount (`0`), not omitted because it happens to be
zero.

**G1**: sources unchanged, confirmed by hash diff.
**G2**: every figure in the workpaper's findings, open items, and
assumptions cites a source file and row/range, or is marked "derived" from
a cited finding.
**G3**: no plug — both open items carry an exact amount and (for the
250,000 item) a suspected nature; nothing is silently absorbed into the
bridge total.
**G4**: threshold stated in the very first content block, before any source
file's content was read — chronology-confirmed above.
**G5**: workpaper §3 lists three assumptions (authoritative revenue source,
gross/net basis of the CSV, fiscal-year labeling), none buried in a
formula.
**G6**: workpaper §5 re-foots the bridge, independently re-sums the 12
monthly cells from the reopened `.xlsx` (not the in-memory build), and
re-checks the 250,000 variance against the reopened file's own cells.
**G7**: `scripts/write_workbook.py work/manifest.json` invoked directly
(after one self-corrected CSV-quoting error); the saved workbook reopens
cleanly with `openpyxl` (five sheets: `cover`, `bridge`, `monthly_tieout`,
`tieout_summary`, `income_statement_ref`).
**G8**: both announce lines are the first content block, before any tool
call that reads a source file's content.

### Result: no further loophole found

All three RED violations are closed and confirmed by JSONL tool-call
order, not self-report. No new loophole surfaced in round 1. No REFACTOR
needed.

---
