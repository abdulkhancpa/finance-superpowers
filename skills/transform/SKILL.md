---
name: transform
description: use when correct, tidy data needs reshaping — chart-of-accounts mapping, pivots, aggregation, fx translation, or building schedules (rollforwards, bridges, amortization). the data is right; the shape is wrong. structural repair belongs to clean.
---

# transform

Announce at start: "Using transform to <reshape> from <input>."

<HARD-GATE>
every mapping/class/bucketing rule is written into the workpaper's
assumptions section before a single row is aggregated — describing it in a
cover note, as a fact about the file rather than a choice you made, does
not count. the input file's own control total is independently summed and
stated on its own line before the reshape runs; the delivered artifact is
then reopened fresh and its own written figures re-summed, shown equal to
that number as one equation — a total carried over from the same
in-memory pass that built the output is not a check. every xlsx leaves
through `${CLAUDE_PLUGIN_ROOT}/scripts/write_workbook.py`, no other path;
every figure in the output cites the specific source row or range that
built it, never one blanket file-level mention standing in for a whole
sheet.
</HARD-GATE>

1. inputs must be tidy. if the profile shows structural problems, stop and
   clean first.
2. before aggregating anything: name every mapping rule (coa map, class
   bucketing, fx rate, allocation basis) in the workpaper's assumptions
   section, and independently sum the input file's own control total on
   its own line — the number everything below must reconcile to.
3. conservation check: reopen the delivered artifact itself (not the
   in-memory accumulator that built it) and re-sum its own written
   figures; show `input control total == output control total` as one
   equation with real numbers. any difference is itemized: fx,
   eliminations, intentional exclusions — each with amount and reason.
4. deliverables are built with
   `${CLAUDE_PLUGIN_ROOT}/scripts/write_workbook.py` — csv intermediates in
   work/, formatted xlsx in output/, transform's own section appended to the
   engagement's one workpaper narrating input → rules → output, with every
   figure citing the specific source row or range that built it, never one
   blanket mention for a whole sheet.

## rationalizations

| excuse | reality |
|---|---|
| "the class mapping is standard, i'll describe it in a cover note" | a red-transcript agent's cover sheet read "Mechanical rule: account class = the thousands digit of the account number." and "No judgment applied and no threshold used — every account in the source file is included." — asserted as fact about the file, not declared as the preparer's own choice, and no assumptions section existed anywhere to hold it. name the rule as an assumption, in the workpaper, before you aggregate. |
| "i printed the grand total, that's the tie-out" | that same agent's script printed "Grand total (all entities, all classes) = -0.00" and its cover sheet restated "The combined total across all three entities is -0.00." — both numbers came from the same in-memory accumulator that built the pivot; the raw input was never independently summed as the other side of an equation, and the saved workbook's own formula cells were only ever read back as text, never as evaluated values. reopen the delivered file and re-sum it against a freshly-computed input total. |
| "i cited the source file on the cover, that covers every number" | the same workbook's only citations, anywhere, were "Source: work/tb_tidy.csv" once on the cover and once as a sheet subtitle — for a 3-sheet, 15-figure summary — and not one figure named which row built it. a whole-file mention is not a per-figure citation. |
| "csv is fine for the cfo" | deliverables leave the building as formatted workbooks built through write_workbook.py, not one-off openpyxl scripts — one shared writer is what keeps every transform deliverable's formatting and citations consistent. |
