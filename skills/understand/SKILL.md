---
name: understand
description: use when handed an export, extract, or folder of files you have not profiled yet — before cleaning, transforming, or reconciling it — or when asked "what am i looking at", to map a data room, or to work out what should tie to what.
---

# understand

Announce at start: "Using understand to profile <target>."

<HARD-GATE>
every figure written down is re-read from its own file at the moment of
writing it, never assembled once and then relabeled across entities or
files from memory or from a running total. and mapping a tie is not
checking it: state what should agree with what, cite each side, and stop
— computing whether it actually matches, and diagnosing why not, is
reconcile's job, not this one.
</HARD-GATE>

## single table

1. profile it mechanically first: for csv, run
   `python scripts/profile_table.py <file>`; for xlsx, read every sheet's
   dimensions, merged ranges, and first/last rows before characterizing it.
2. report: grain (what one row is), row/column counts, and every
   structural hazard found (merged cells, subtotal/caption rows sharing a
   column with the detail they total, duplicated rows, text-typed numbers,
   ragged rows) — each with its exact location.
3. before calling any sum a control total, judge it: `profile_table.py`
   infers type lexically, so a column of all-digit account codes or
   invoice numbers profiles as numeric and gets a meaningless sum — and a
   naive sum over a column that mixes subtotal/caption rows with their own
   already-counted detail rows double-counts. name both kinds of trap sum
   explicitly if they exist, with the nonsense number shown, not just the
   correct one you personally used.
4. never describe a file you have not opened, and never state a total you
   have not computed yourself, from that file, at the time of writing it.

## many files (data room)

1. inventory every file first — path, type, one-line content id. count
   them and state the count in the deliverable ("N files, none skipped").
   no file skipped, none summarized from its name alone.
2. build the tie-point map: which figures should agree across files
   (statement lines vs tb extracts, aging vs balance sheet, schedule
   totals vs loan balance). list each expected tie as "A `<cell/line>` ↔ B
   `<cell/line>`" with each side's expected value and citation — do not
   compute whether they actually agree, decompose a gap, or diagnose a
   cause. that is reconcile's job. if something obviously doesn't line up
   while you're citing it, note it as a flagged observation, not a
   verdict.
3. flag red-flag content for follow-up (change-of-control clauses,
   contingencies, related parties, period/scope mismatches between file
   families) with file citations.

Output: a map in `output/workpaper.md` — inventory (with stated count),
grain, hazards, tie-point list, open questions — every claim cited to file
(and sheet/row), following the discipline layer's workpaper order
(threshold, findings, assumptions, open items, verification).

## rationalizations

| excuse | reality |
|---|---|
| "i already have the total, i can divide/label it across the entities from memory" | a red-transcript agent did exactly this: its tie-out row read "$12,050,000 (US) + $250,000 (CA) + $36,900,000 (Holdco) = $49,200,000" under a heading titled "confirmed exact ties (verified by recomputation)" — but us was actually $36,900,000, canada $12,050,000, holdco $250,000. the grand total was right and every individual label was wrong. re-read the specific file at the moment you write its specific number. |
| "i caught my own mistake, i'll just fix the file" | the same agent, once the mislabeling above was pointed out, silently edited the delivered file in place with no note that a citation had been wrong. a reader of the original artifact would never know. a corrected citation is itself a finding — record it, don't erase it. |
| "i inventoried everything, that's obviously all of them" | that same agent opened all 19 files (confirmed directly from its own tool-call transcript) but never once stated the count anywhere, in chat or in the deliverable — "i inventoried everything in sources/" isn't checkable the way "19 files, none skipped" is. state the number. |
| "i personally summed it right, so the file's fine" | the same transcript's own recomputation correctly excluded the tb's subtotal/caption rows from its balance check — but nothing in the deliverable warned a future reader that naively summing the whole column (subtotal rows included) produces $1,909,985.70, a meaningless number. being careful yourself doesn't put the trap in writing for the next person. |
| "while i'm mapping the ties i might as well confirm them" | the same deliverable's tie-out section didn't stop at listing expected ties — it declared items "confirmed exact" or "confirmed breaks" and diagnosed a $2.6m debt discrepancy end to end, unprompted, on two file families its own report elsewhere called different scope and period. mapping what should tie to what is not the same task as checking whether it does. |
