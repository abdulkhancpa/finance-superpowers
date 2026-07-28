---
name: review
description: use when checking whether finished work holds up — a human analyst's schedule or memo, or claude's own prior output — before it is relied on or released.
---

# review

Announce at start: "Using review to reperform <work> against <sources>."

<HARD-GATE>
never assess a number you have not recomputed from the sources. agreement
reached by reading is not review. the claims checklist itself — not a
sentence promising one — is posted, in writing, as its own message,
before the first recomputation of any source figure; a line like "here is
the plan" followed immediately by recomputation, with the actual
checklist appearing only afterward, is the same violation one layer down.
</HARD-GATE>

1. announce, then inventory the work's claims as a checklist — every
   number, every citation, every conclusion — before evaluating any of
   them. the checklist's own text must describe claims not yet tested, not
   recap tests already run — a checklist written in the past tense
   ("I reperformed each...") is a summary, not a plan.
2. reperform independently: recompute each figure from the cited source.
   your number vs their number, side by side. foot every table in the
   work — a table that does not foot fails regardless of its story, even
   if no single cell looks wrong on its own; add the sides yourself.
3. verify citations exist, literally: list the actual files in sources/
   and check every cited filename against that list before opening
   anything. a cited name that isn't in the listing is a fabricated
   citation and is reported as exactly that — do not silently map it onto
   a similarly-named file that does exist and grade the content instead;
   the wrong name is its own finding, separate from whatever the file it
   probably meant to name does or doesn't say.
4. an unexplained remainder is not reviewed until its mechanism is
   checked, not just its size: before writing "unexplained" or "no
   support," test the residual against every candidate already sitting in
   the sources you've already opened (duplicate, timing, transposition,
   population) — a residual whose exact amount matches a candidate you
   already printed and set aside is not unexplained, it's unchased.
5. check the work's own discipline as its own step, separate from the
   number-checks: does it state a threshold anywhere? assumptions
   declared? plugs disclosed as such? report the presence or absence of
   each explicitly — a memo can get every number right and still fail
   this step.
6. verdict per claim: pass / fail (with your recomputed number) /
   cannot-verify (with the missing evidence named). overall conclusion
   only after the per-claim table.
7. output: `output/review.md`, a standalone file — never a section
   appended into the workpaper being reviewed. the claims checklist,
   verdict table, discipline checks, and overall conclusion all live here,
   citing both the reviewed deliverables and the sources reperformed
   against.
8. tone: findings are about the work, not the worker. every fail carries
   the evidence that proves it.

## rationalizations

| excuse | reality |
|---|---|
| "the cited file is close enough to a real one, I'll just note what the real file covers" | a red-transcript agent's own file listing already returned only three names — `./sources/ar_subledger_2026-06.csv`, `./sources/gl_je_detail_2026-07.csv`, `./sources/gl_summary_2026-06.csv` — with no `gl_detail.csv` among them, yet its report's only comment was that the file it silently substituted "contains only a single July entry, not a full set of June/July postings" — a coverage complaint, never the plainer finding that the cited name does not exist in sources/ at all. |
| "I found the residual and sized it, no source explains it" | a red-transcript agent had already printed `{'invoice': 'inv-19877', ... 'open_amount': '45000.0', ...}` and separately printed the residual itself as `9000.0`, then wrote "No other reconciling item, invoice, or JE in the provided sources accounts for the $9,000 difference. It is untraced and unexplained" — two sections later filing that same row away as an unrelated aging note instead of testing 45,000 against an implied 54,000. |
| "the review only checks whether the numbers are right" | a red-transcript agent's every verdict was a numeric recomputation; it never once reported whether the memo it reviewed stated a threshold anywhere in its own text — an omission real enough that the memo's total silence on the point went unmentioned in five pages of otherwise careful review notes. |
| "I'll write up what I found, then explain the plan in the report" | a red-transcript agent's first text content of any kind, in the entire run, was the completed review-notes document itself — no inventory of claims, no announcement, posted before any source file was opened. |
| "I said 'before evaluating anything, here is the plan' right before I evaluated, so the plan came first" | (caught in the GREEN round-1 audit, not the RED run) a green-run agent posted exactly that line, then immediately ran the duplicate-key scan and residual arithmetic in the next two tool calls — and only after those ran did it post the actual claims checklist, whose own text described the work in the past tense: "I reperformed each against the source CSVs (full duplicate-key scan, independent sum, JE detail lookup). Now writing up findings." A sentence announcing a plan is not the plan; the checklist itself has to precede the computation, not follow it wearing a preceding sentence as a disguise. |
