---
name: reconcile
description: use when two things should agree and you must prove whether they do — bank recs, subledger-to-gl, intercompany, proof-of-cash, statement-to-extract ties — or when a difference between two totals needs explaining.
---

# reconcile

Announce at start: "Using reconcile to tie <a> to <b>."

<HARD-GATE>
identified items + unexplained remainder = total difference, exactly, to
the penny. the unexplained remainder is disclosed with its amount — never
plugged, never rounded away, never absorbed into another item. disclosing
a remainder is not the same as chasing it: a mechanism that could still be
chased from sources already in hand is not yet an open item.
</HARD-GATE>

1. foot both sides independently first, as their own step: the very first
   computation that touches either source file's values must do nothing but
   sum side a, sum side b, and print the difference. duplicate scans, date
   scans, and hypothesis checks belong in a later, separate call — running
   them in the same script as the footing, then narrating a "checkpoint"
   afterward as if it came first, does not satisfy this; chronology is the
   tool-call order, not the prose.
2. chase mechanics before judgment: duplicates (same key posted twice),
   timing (items in one period's population but the other side's next
   period — prove with the other period's detail, not assertion),
   keying/transposition errors (difference divisible by 9 is a hint, not
   proof — find the actual entry, don't stop at "no source explains this"
   without checking every row already in hand against that hint),
   population mismatches (scope: dates, entities, accounts).
   a divisibility hint is not itself a search: scanning an entire large
   population for any digit-swap divisible by 9 returns many coincidental
   hits and, left there, is a longer list, not an answer. narrow first —
   isolate the rows that break the population's own pattern (an irregular
   key or name, a round amount where the rest carry cents, an entry
   outside an otherwise systematic sequence) — then eliminate the ones
   already explained by other reconciling items already found. what's left
   is the actual candidate set; test each one against the residual's exact
   amount before writing "no candidate fits."
3. every reconciling item carries: amount, direction (which side is
   higher), root cause, and evidence citation (file + row/je number).
   "probably timing" without the proving entry is an open item, not an
   explained one. "no transaction explains this" is a claim, not a search —
   before writing it, check every already-loaded row for a candidate that
   fits the residual's size and pattern.
4. proof: a reconciliation statement in the workbook — side a total,
   each item signed, side b total — that foots. re-verify by recomputing
   it from the itemized rows, not by asserting it.
5. items under the agreed threshold are still listed individually.
6. a remaining amount only becomes an open item once you can say, in
   writing, which mechanics you checked and ruled out for it (duplicate?
   timing? transposition? population?) — an item that's merely disclosed
   without that check is a plug wearing a disclosure as a caption.

## rationalizations

| excuse | reality |
|---|---|
| "found the big item, the rest is noise" | the identity must hold to the penny. keep going or disclose the remainder — and disclosing still requires checking the mechanics first. |
| "no transaction in the sources explains this residual" | a red-transcript agent wrote exactly that — "No transaction in the sources provided (ar_subledger_2026-06.csv, gl_je_detail_2026-07.csv, gl_summary_2026-06.csv) accounts for this amount" — after it had already printed the one row that does: `inv-19877`, open_amount `45000.0`, a $9,000 transposition candidate (45,000 vs. an implied 54,000). check the divisibility hint and every already-loaded row before declaring nothing fits. |
| "i'll total the subledger while i'm scanning for duplicates" | foot both sides and state the difference as its own step, before investigation starts. a red-transcript agent's raw-total sum, duplicate scan, and late-invoice-date scan all ran inside one python call — no line anywhere stated "AR total = X, GL total = Y, difference = Z" before the first investigative step. |
| "i disclosed it as an open item, so it's not a plug" | disclosure with a caveat is still a plug if the mechanism was chaseable from sources already in hand. a red-transcript agent's own final report called it exactly that: "Item 3 is carried as a disclosed, unresolved plug" |
| "it'll reverse next month" | show the entry that proves it. the sample's timing item is provable from the july je detail (`je-7-0043`) — cite the je number, not the assumption that it reverses. |
| "i'll state the footing checkpoint before further investigation" | (caught in the GREEN round-1 audit, not the RED run) a green-run agent's first source-touching python call already ran `print("\nduplicate invoice numbers:", dupes)` in the same script as the AR/GL footing and an outlier scan — then, three tool calls later, wrote "Footing checkpoint (stated as its own step, before further investigation)" as though the totals hadn't already been produced alongside the duplicate/outlier scan. tool-call order is chronology; a restated checkpoint after the fact isn't one. |
| "i scanned for every digit-swap divisible by nine and none of the candidates were corroborated by a second source, so it can't be isolated" | inside a larger multi-workstream engagement (not the isolated reconcile-only scenario), an agent's own workpaper read: "a full scan of all 207 tidy rows for a two-adjacent-digit swap that would produce exactly a $9,000 difference returns 34 candidate rows... with no corroborating second source... to identify which — if any — is the actual erroneous entry" — and a second, independent reviewer re-ran the identical blind scan, got 35 hits, and signed off on "not identified, and this is the correct outcome, not a miss." both missed that the population is overwhelmingly one systematic, sequential naming pattern with a handful of irregular, named, round-dollar entries breaking it — narrowing to that handful first, then eliminating the ones already explained by other found items, leaves exactly one untested row whose transposition matches the residual to the penny. a scan across the whole population is not the same as narrowing the population first. |
