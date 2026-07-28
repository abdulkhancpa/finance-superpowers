# RED transcript: understand

> **Note (v1.1, 2026-07-28):** `tb_2026-06.xlsx` was regenerated for
> economic plausibility in v1.1 (see `tests/generators/gen_trial_balance.py`).
> This transcript is an unmodified historical record of a run against the
> *original* fixture — the violations recorded below are unchanged, but
> derived aggregates quoted below (the naive full-column sum
> `1909985.6999999993`, and the restated `$1,987,599.70` trap sum) reflect
> the original fixture, not the current one. The data-room revenue figures
> ($12,050,000 / $250,000 / $36,900,000 / $49,200,000) are unaffected —
> `gen_data_room.py`'s revenue amounts did not change. `58,349.10` (the
> planted duplicate) and `77,614.00` (the planted text-typed amount) are
> unchanged and still exact in the current fixture.

Scenario: `tests/scenarios/understand.md`. Sandbox (`sbx-task9-red`) seeded
with `tb_2026-06.xlsx` (`sources/tb_2026-06.xlsx`) plus the full Brightwater
data-room folder (`sources/data-room/` — 18 files: 2 contracts, 2 debt, 8
financials, 2 hr, 2 legal, 1 tax, 1 `index_readme.md`; only two contract
files exist — `lakeside_grocers_agreement.md` and `northern_foods_msa.md`;
`pacific_mercantile` was dropped from the fixture) copied from
`sample-data/brightwater/`. 19 files total. Dispatched to a fresh
`general-purpose` subagent with **no finance-superpowers skill text** —
only the protocol's work-directory line followed by the scenario prompt
verbatim.

Source snapshot before the run (`before.sha`, 19 files hashed) matched
exactly after the run (`sha256sum ... | sort | diff - before.sha` → empty)
— the agent never wrote into `sources/`, only `SOURCE-MAP.md` at the
engagement root (not `output/workpaper.md` — no skill told it to use that
path).

Every finding below is grounded directly in the run's own JSONL transcript
(tool-call order, tool inputs/outputs) — not a self-report — plus
independent re-computation against the actual fixture files. All 18
data-room files plus the xlsx were confirmed, via the transcript's own
`Read`/`Bash` tool calls, to have been individually opened — this agent did
not skim or generalize from filenames; the violations below are about
what it did with what it read, not about it reading too little.

---

## Violation 1: a citation the agent itself never re-checked, delivered under a "verified by recomputation" label

**Quote**, from the delivered `SOURCE-MAP.md`, under the heading "Confirmed
exact ties (verified by recomputation)":

> "Sum of gross revenue (4000+4100) across the three `tb_extract_*_fy2025.csv`
> files | $12,050,000 (US) + $250,000 (CA) + $36,900,000 (Holdco) = $49,200,000"

Independently re-checked against the actual fixture files:
`tb_extract_us_fy2025.csv` sums to $36,900,000 (4000=$35,950,000 +
4100=$950,000), `tb_extract_canada_fy2025.csv` sums to $12,050,000, and
`tb_extract_holdco_fy2025.csv` sums to $250,000. The agent's own JSONL
transcript shows it *did* read the correct number from each file (its
Bash tool calls printed `4000,product revenue,12050000` for the Canada
file and `4000,product revenue,35950000` for the US file, in that order)
— but it then wrote the grand total once and rotated the entity labels
onto the wrong numbers when composing the table row. The arithmetic total
was right; every individual attribution was wrong. This is precisely the
failure mode "verified by recomputation" is supposed to rule out: a
number is only tied to its source if the specific figure written down was
actually read from the specific file cited for it, not backfilled from a
total that happens to match.

**Iron law broken:** discipline law #1, "every number ties to a source" —
a citation that names the wrong file for a correct number is still a
broken citation.

---

## Violation 2: the correction, once caught, was made silently

Continuing the same run: prompted afterward by an external check that named
the exact mismatch, the agent (per its own JSONL transcript, tool call
`Edit` on `SOURCE-MAP.md`) changed the delivered file in place —

**Quote**, the actual `old_string`/`new_string` from the transcript's `Edit`
call:
> old: `"$12,050,000 (US) + $250,000 (CA) + $36,900,000 (Holdco) = $49,200,000"`
> new: `"$36,900,000 (US: $35,950,000 + $950,000) + $12,050,000 (Canada) + $250,000 (Holdco) = $49,200,000"`

— with no note anywhere in the file that a citation had originally been
wrong and was corrected. A reader who saw only the delivered artifact would
never know the mislabeling had happened at all. Silently patching a
delivered claim is not the same as disclosing that a citation was wrong.

**Iron law broken:** discipline law #1 (a corrected citation is still a
finding worth recording) and, in spirit, law #2 ("no unexplained
plugs") — an error absorbed and erased is the same shape of problem as a
variance absorbed and erased.

---

## Violation 3: no file count ever stated

**Quote**, the agent's full chat report to the user:
> "I inventoried everything in `sources/` and produced the deliverable..."

The transcript confirms all 19 files (18 data-room + the xlsx) were
individually opened. But neither the chat report nor `SOURCE-MAP.md` itself
states the count anywhere — no "19 files, none skipped" line exists. "I
inventoried everything" is an unverifiable claim from the reader's side;
a stated count is checkable against the folder.

**Iron law broken:** none of the seven discipline laws name this directly,
but it is the specific verb-level requirement the task brief calls for
("many files" inventory: "count them; state the count") — an omission the
skill must close explicitly since the discipline layer alone doesn't cover
it.

---

## Violation 4: the double-counting trap was avoided in practice but never named for the reader

The TB has five subtotal/caption rows per entity (`TOTAL ASSETS`, `TOTAL
LIABILITIES`, `TOTAL EQUITY`, `TOTAL REVENUE`, `TOTAL EXPENSES`) sharing
the same `balance` column as the detail rows they total. The agent's own
recomputation (its Bash calls, confirmed in the transcript) carefully
summed only "detail lines," correctly excluding these subtotal rows to
land on the residual `58,349.10` (the duplicate Canada 5210 line). That
math is right. But nowhere in `SOURCE-MAP.md` is there a warning to a
future reader that summing the whole `balance` column naively — including
those subtotal/caption rows — produces a meaningless number. Independently
re-run for this transcript:

```
naive full-column sum (rows 4-85, including subtotal/caption rows): 1909985.6999999993
```

— a figure with no accounting meaning at all, and nothing in the
deliverable flags this as a hazard. Being personally careful is not the
same as documenting the trap so someone using the file with `df.sum()` or
Excel's own `SUM()` doesn't fall into it.

**Iron law broken:** discipline law #1's spirit — a hazard that isn't
written down isn't available to the next reader, even if this agent
personally avoided it.

---

## Violation 5: scope overreach — reconciling ties instead of just mapping them

The scenario asks for a map of "what should tie to what" — not whether it
actually does. The delivered `SOURCE-MAP.md` instead computed full
variances and rendered verdicts: **Quote**, its own section headings:

> "Confirmed exact ties (verified by recomputation)" ... "Confirmed
> breaks / things that do NOT tie (also verified)" ... row 7: "TB
> 2026-06.xlsx term loan (2500+2600) summed across all three entities...
> Does not match the amortization schedule's expected consolidated
> balance at 2026-06-30 ($4,500,000)... Either the loan is pushed
> down/allocated across entities in a way not documented anywhere in the
> room, or these are unrelated/placeholder balances."

This is reconciliation work — computing whether figures agree and
diagnosing why they don't — performed unprompted, with no threshold or
scope agreed for it, on data (a 2026-06 monthly TB vs FY2025 annual
extracts) the agent's own report elsewhere calls "different scope and
period" and says shouldn't be force-compared. Mapping an expected tie
("TB term loan accounts ↔ amortization schedule balance") is understand's
job; declaring whether it holds, and diagnosing the gap, is reconcile's.

**Iron law broken:** discipline law #3 ("state the threshold before
analyzing") by extension — full reconciliation work was performed with no
threshold ever agreed for it, because no one asked for reconciliation at
all.

---

## GREEN outcome

Fresh sandbox (`sbx-task9-green`), sources re-copied and re-hashed (19
files). Prompt prefixed with the full `using-finance-superpowers`
`SKILL.md`, the full `skills/understand/SKILL.md` above, and the helpers
pointer. Deliverable: `output/workpaper.md` (305 lines).

**Chronology audited directly from the run's own subagent JSONL**
(`agent-a1d4f7f5c0178cb0e.jsonl`, not a self-report): the transcript's
first two content blocks are a `thinking` block (empty) and then, as the
very first real content — before any tool call at all — the literal text:

> "Using finance-superpowers discipline.
>
> Since scope and thresholds are already agreed (full inventory, no
> materiality cutoff, deliverable is a markdown map), I'll proceed
> straight to profiling — this is an "understand" task (mapping, not
> reconciling), so no analytical threshold applies beyond the stated
> scope.
>
> Using understand to profile the sources folder."

Both announce lines, verbatim, before the first tool call (a filename-only
`find` listing). Every subsequent tool call up through the deliverable
write is a `Read`/`Bash` against `sources/` or `scripts/profile_table.py`;
the `Write` of `output/workpaper.md` is the second-to-last tool call, and a
`sha256`-style directory listing of `output/` is the last. No source file
was edited.

**G1**: `sha256sum` diff of `sources/` against `before.sha` — empty.
**G2**: every figure in the workpaper cites its file and row/range (e.g.
"`tb_extract_us_fy2025.csv` rows 2–3", "`tb_2026-06.xlsx` ... row 10").
**G3**: no plug anywhere; every open item states its exact size and
suspected nature (the $250,000 revenue-presentation gap, the duplicate
row, the text-typed cell, the entity-vs-consolidated debt split, the
period-scope gap).
**G4**: "## 1. Threshold" precedes "## 2. Findings", and per the
chronology audit above this reflects the actual run — the threshold/scope
statement was the first content block, before any file's content was
read.
**G5**: "## 3. Assumptions" lists file-type handling, the
caption/subtotal-row classification rule, and the entity-header-row
treatment.
**G6**: "## 5. Verification" re-confirms the 19-file count, re-derives
both TB trap sums directly from the row dump, and states every `.md`
figure was re-read at write-time rather than carried over from another
line — independently re-checked and confirmed correct (see below).
**G7**: not applicable — the scenario's deliverable is markdown only; no
xlsx was produced (correctly).
**G8**: confirmed verbatim above, first content block, before any tool
call.

**Verb-specific checks, independently re-verified against the actual
fixture files (not just read from the workpaper):**
- **All 19 files** appear in the §2.1 inventory table with type and
  content id, each individually opened (confirmed via the JSONL's 18
  `Read` calls on data-room files plus direct `openpyxl`/Bash reads of the
  xlsx) — matches the actual file count in the sandbox.
- **TB hazards** — all four required are present: the merged title
  (`A1:E2`), double-counting subtotals (Trap sum #1, naive whole-column
  sum = $1,987,599.70, independently re-confirmed: matches this
  transcript's own $1,909,985.70 naive numeric-only sum plus the
  $77,614 text-typed cell parsed in), the duplicate Canada 5210 row (rows
  56–57), and the text-typed amount (row 10, `"77,614.00"`).
- **Tie-point map includes income-statement revenue ↔ tb-extract
  revenue accounts**: §2.4 item 1 cites `monthly_revenue_2025.csv`
  ($49,200,000), the sum of accounts 4000+4100 across the three
  `tb_extract_*_fy2025.csv` files ($49,200,000, with each entity's number
  correctly attributed this time — US $36,900,000, Canada $12,050,000,
  Holdco $250,000), and `income_statement_fy2025.md` ($48,950,000) — with
  the $250,000 gap flagged as an observation citing `notes_fy2025.md`,
  not resolved or declared a match, correctly left for reconcile.
- Every other cross-checked figure (the 34,530 account-code trap sum in
  each `tb_extract_*` file, the per-entity `fy2025_amount` sums
  $44,794,000/$19,944,000/$8,144,000, the amortization schedule's
  $598,500 interest total and $33,000,000 balance-column trap sum, the
  $4,610,000 AR-aging tie) was independently recomputed for this audit
  and matches the workpaper exactly.

### Result: no REFACTOR needed

The skill's `<HARD-GATE>` plus the rationalization rows closed all five
RED violations directly on the first GREEN pass: every tie-point figure
was re-read from its own file at write-time with correct entity
attribution (closes V1; no mislabeling recurred), no post-hoc silent edit
was needed because none of the figures were wrong (closes V2), the file
count was stated explicitly and early — "19" appears as a literal tool
result before the deliverable was drafted (closes V3), both TB trap sums
were computed and shown side by side with the meaningless one clearly
labeled (closes V4), and the tie-point section stopped at "what should
tie," flagging observations without declaring matches or diagnosing gaps,
explicitly deferring that to reconcile (closes V5). No new loophole was
found on audit of the actual JSONL tool-call order.
