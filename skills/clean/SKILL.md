---
name: clean
description: use when a source file has structural problems — merged cells, header/subtotal rows mixed into data, duplicates, text-typed numbers, ragged rows — and you need a tidy table before any mapping or analysis; reshaping already-correct data instead of fixing broken structure is transform's job, not this one.
---

# clean

Announce at start: "Using clean to tidy <file>."

<HARD-GATE>
the raw control total is written down, on its own line, before any row is
dropped, coerced, or deduped — never reconstructed afterward from what got
deleted. the tidy table's own full column is then re-summed, rounded to
cents, and shown equal to the raw total minus every itemized removal — an
equation with real numbers, not a per-section proxy for it. a row is
dropped as a duplicate only when you can say why it is one posting, not
two; anything you can't prove stays in, flagged, never deleted with a
hedge stapled on afterward.
</HARD-GATE>

1. profile first (understand, or `python scripts/profile_table.py`). before
   touching a single row, write down the raw control total (the file's own
   naive/grand total) as the number this cleanup must reconcile to.
2. work on a copy in work/ — the source stays untouched.
3. every removal or coercion is logged with a count and location: n
   header/subtotal rows removed (listed), n duplicates removed (both rows
   shown, with the reason you know they are one posting and not two real
   ones), n text-typed values coerced (before/after).
4. a duplicate you cannot prove is a duplicate stays in the tidy table,
   flagged — dropping it and noting your doubt afterward is not the same
   as keeping it.
5. verify: re-sum the tidy table's own balance column, rounded to cents.
   show it as one equation: raw control total − removed subtotal rows −
   removed duplicates = tidy total. the tidy total equals exactly 0.00, or
   the residual is itemized as an open item with its exact size.
6. output: tidy csv in work/, cleaning log in output/workpaper.md.

## rationalizations

| excuse | reality |
|---|---|
| "the section-by-section reconciliation ties, that's the check" | a red-transcript agent's own report claimed "all ties out exactly to zero except Holdco's equity section, whose non-zero diff (-964,625.30) is the expected consequence of issue #5 above, not a new error" — five section checks, never the one required. independently re-summing that same agent's own delivered csv gives -7.275957614183426e-11, not 0.00. round it, state it, every time. |
| "i'll capture the grand total while i'm logging what got deleted" | a red-transcript agent's only mention of the source's own total anywhere was one row inside a nineteen-row deletion log — "GRAND TOTAL = 964625.3" filed under things dropped, never posted up front and never used as one side of an equation. the raw total is step 1, written down before anything is touched, not archaeology afterward. |
| "looks identical, i'll drop it and note my doubt" | a red-transcript agent dropped a row as a duplicate ("Dropped - identical entity/account/description/balance already present at row 56.") then admitted in the same deliverable "if this instead represents two distinct postings that happen to share the same amount, the tidy total for that entity's salaries expense will be understated by 58,349.10" — an admitted-uncertain deletion is a plug with a caveat stapled on. prove it or leave it in, flagged. |
