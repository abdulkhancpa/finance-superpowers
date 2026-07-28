---
name: analyze
description: use when a movement or difference needs explaining by driver — flux and variance analysis, period-over-period bridges, budget-vs-actual, driver decomposition — after the underlying data already ties.
---

# analyze

Announce at start: "Using analyze to bridge <from> to <to>."

<HARD-GATE>
the bridge must foot: start + sum(drivers) + residual = end, exactly. the
residual is shown as its own labeled bar with its amount — never smeared
across other drivers. the threshold and plan are posted, in writing, as
their own message, before any source file's values are read or compared —
a plan or finding narrated into the final report only after the deliverable
is already built is not a plan, however it's introduced.
</HARD-GATE>

1. threshold first, in writing, before touching sources: state the agreed
   explanation threshold and a short plan before any source file is read
   for its values — not narrated afterward as if it came first.
2. decompose against data, not narrative: every driver quantified from a
   source file (cited), not from what usually drives revenue. a driver you
   cannot quantify from the sources is an open item with a stated data
   request naming which document (and what it should show) would resolve
   it — never a generic "please explain."
3. check for definition changes before economics, and connect every
   tie-out finding back to the bridge it touches: if two sources disagree
   on the same figure by an amount that could be part of the movement (a
   presentation reclass, scope change, fx), that gap is a candidate driver
   of the movement itself — isolate it as its own bar, or, if it can't be
   confirmed from the sources in hand, flag it as an open item on the
   bridge naming the missing document, not as an unrelated footnote in a
   separate tab.
4. never reuse the driver-explanation threshold to decide whether an
   unreconciled input discrepancy deserves investigation — those are two
   different questions. an input gap gets chased or disclosed on its own
   terms, regardless of its size relative to the driver threshold.
5. every driver above threshold explained; below-threshold drivers
   aggregated into one labeled "other" bar with its exact amount.
6. deliverable: bridge schedule via write_workbook.py + workpaper with
   method, threshold, citations, assumptions, verification (re-foot).

## rationalizations

| excuse | reality |
|---|---|
| "growth is obviously volume" | quantify it from a file or list it as unquantified. plausible is not proven. |
| "i'll build the workbook, then explain the plan/threshold in the report" | a red-transcript agent's first words to the user, anywhere, were "Workbook built successfully. Now the companion workpaper memo." — after `TOTAL 49200000` and `diff 250000` had already been computed and the workbook already saved. state the threshold and plan before any source file's values are read, not after the deliverable exists. |
| "the bridge ties to the income statement, it's clean" | a red-transcript agent's own bridge note read "This figure ties directly to `income_statement_fy2025.md` and requires no adjustment." two tabs before its own tie-out check found the input sources disagreed by $250,000 on that same figure — the two were never connected. chase every clue already in your own workpaper before calling the bridge clean. |
| "this gap is below the driver threshold, so it doesn't need a named driver" | a red-transcript agent wrote "This difference is below the $500,000 threshold set for driver explanation in this engagement, so it does not itself require a named driver, but it **does not tie out** and is disclosed here for completeness rather than silently netted against the bridge." the driver threshold governs which economic movements need naming; it doesn't govern whether an unreconciled input disagreement gets investigated — those are different questions. |
| "i asked for an explanation, that's a data request" | the same agent's follow-up read only "Explanation / reconciliation for the $250,000 difference identified in Section 4.3." — no document named. say what kind of document would resolve it (e.g. a presentation/policy note on the reporting change), not just "explain this." |
