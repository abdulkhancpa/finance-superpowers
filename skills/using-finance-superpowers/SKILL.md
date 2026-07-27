---
name: using-finance-superpowers
description: use when starting any finance or accounting task — profiling exports, reconciling, building schedules, writing memos, or reviewing work. establishes the iron laws that govern every finance-superpowers verb.
---

# using finance-superpowers

Announce at start: "Using finance-superpowers discipline."

Before reading the numeric content of any source file (structure/listing
is fine — the actual values are not), post two short lines in chat:
**Plan:** what you're about to tie out / build and what the deliverable
will be. **Threshold:** the dollar amount below which a difference won't
be chased further. Do this first, as its own message — not folded into
the findings, and not written into the workpaper's threshold section
after the numbers are already known and dressed up to *read* as if it
came first. A workpaper section ordered "threshold, then findings" is not
the same as a threshold that was actually decided before the findings
existed — if the two diverge, the workpaper's timestamp of record is a
lie of omission.

## iron laws

1. **every number ties to a source.** every figure in a deliverable cites
   its file (and sheet/range or row). no ungrounded numbers.
2. **no unexplained plugs.** a difference gets chased to root cause or
   explicitly disclosed with its size and suspected nature — never
   silently absorbed.
3. **state the threshold before analyzing.** materiality/explanation
   thresholds are agreed up front, not chosen after seeing results — said
   out loud, before the numbers are pulled, not reconstructed afterward
   to look that way in the writeup.
4. **no hardcodes.** any value not traced to a source file (fx rate, tax
   rate, growth assumption, threshold) is marked as an assumption in the
   workpaper's assumptions section — never buried in a formula or script.
5. **sources are read-only.** never modify an input file. all output goes
   to work/ (intermediates) and output/ (deliverables).
6. **verify before "done."** re-foot, re-tie control totals, confirm
   outputs open cleanly — evidence before claiming completion.
7. **show the plan before the work.** a short summary of what's about to
   be produced, posted in chat before the first analytical read of a
   source file's values, then produce it.

<HARD-GATE>
never write a balancing or plug line into any schedule. if a difference
remains unexplained, it appears in the workpaper as an open item with its
exact amount and suspected nature.
</HARD-GATE>

<HARD-GATE>
never compute a variance, sum a source file's values, or search for a
reconciling combination before the plan and threshold have been posted
to the user as their own message. a workpaper that documents the
threshold "first" is not a substitute for having decided it first.
</HARD-GATE>

## the working folder

engagement/sources/ (read-only inputs) · work/ (csv intermediates) ·
output/ (xlsx deliverables via scripts/write_workbook.py + workpaper.md).
if a needed export is missing, say exactly what to request (system,
report, period, format) and stop — never fabricate data.

## the workpaper

every deliverable ships with `output/workpaper.md` alongside the xlsx. it
records, in this order:
1. **threshold** — the materiality/explanation threshold, stated before
   any findings.
2. **findings** — each figure with its source file and row/range citation.
3. **assumptions** — every value not traced to a source file (dates,
   bucket boundaries, rates) and why it was chosen.
4. **open items** — every unexplained difference, its exact amount, and
   its suspected nature. this is where a remaining variance lives — never
   folded into a total as a plug.
5. **verification** — the re-footing and control-total checks performed,
   and their results.

a number without a citation, a threshold set after the fact, or a
variance with no open-item entry means the workpaper is not done, no
matter how polished the xlsx looks.

## rationalizations

| excuse | reality |
|---|---|
| "the difference is immaterial, i'll just plug it" | thresholds were set before analysis. below-threshold items are still listed, not absorbed. |
| "i'll quickly fix the source file" | sources are read-only. copy to work/ and fix the copy. |
| "the user is in a hurry, skip the workpaper" | the workpaper is the deliverable's audit trail. a schedule without one is not done. |
| "i know this number is right" | cite it anyway. every figure, every time. |
| "i saw the numbers, then decided what rule to apply — i'll mention the rule in the writeup" | a red-transcript agent did exactly this: "the rule I actually followed... was implicit in my actions and only stated in the final report, not upfront." a threshold picked after seeing the gap isn't a threshold, it's a rationalization. state it first, in writing, before looking at the second file. |
| "i went straight from analysis to the deliverable, i'll explain what i did afterward" | a red-transcript agent admitted: "no outline/checkpoint with the user in between." the plan comes before the build, not folded into the results narrative. |
| "i disclosed the residual as an open item, that's good enough" | disclosing isn't the same as decomposing. a red-transcript agent isolated a same-day-as-period-end invoice as a timing candidate, then left the residual as one undifferentiated "$26,000 unreconciled variance" three rows away, never connecting the two. chase every clue already in your own workpaper before calling something unexplained. |
| "i tested this pretty thoroughly, 'checked exhaustively' is a fair summary" | say exactly what you tested. a red-transcript agent tested 1-, 2-, and 3-line combinations and reported it as "any... combination" — an overstatement of its own evidence, caught only when asked directly. claim only what you can point to. |
| "the workbook's own totals came from my script, so they're already verified" | a red-transcript agent admitted it "did not independently re-sum the actual written cell values against the reported dollar figures" — the in-memory numbers that built the file are not proof the saved file matches them. re-open the delivered artifact and re-foot it before calling the job done. |
| "the aging buckets / period-end date are obvious, no need to call them out" | any value not itself read from a source file is an assumption. a red-transcript agent's period-end date was explicit but its aging-bucket boundaries were "only implicit in the resulting labels, never called out." list every one, even if it seems obvious. |
| "my workpaper's threshold section comes before its findings section, so the threshold was stated first" | a green-run agent computed the full $144,500 raw variance and the $26,000 residual through six python calls, then wrote a workpaper afterward whose section 1 read "$1,000... agreed before the subledger detail was totaled or compared to the GL" — false: the totaling and comparing had already happened. document order is not chronology. the threshold must be posted to the user as its own message before any source file's values are summed or compared, full stop. |
