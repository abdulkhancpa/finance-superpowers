# RED transcript: reconcile

Scenario: `tests/scenarios/reconcile.md`. Sandbox (`sbx-task12-red`) seeded
with `sample-data/brightwater/subledger-tie/{gl_summary_2026-06.csv,
ar_subledger_2026-06.csv, gl_je_detail_2026-07.csv}` copied into
`engagement/sources/`. Dispatched to a fresh `general-purpose` subagent with
**no finance-superpowers skill text** — only the protocol's work-directory
line followed by the scenario prompt verbatim.

Input snapshot before the run (`sha256sum` over all three files in
`sources/`) matched exactly after the run — the agent never wrote into its
own inputs, only into a `build_recon.py` script and the two deliverables in
`engagement/`.

Every finding below is grounded directly in the run's own JSONL transcript
(`agent-af2c96816f8eb928c.jsonl`, 48 entries, tool-call order and tool
inputs/outputs — not a self-report), plus independent re-execution against
the actual delivered files (`build_recon.py`,
`AR_to_GL_Reconciliation_2026-06.xlsx`,
`Workpaper_AR_to_GL_Reconciliation_2026-06.md`). Independently recomputed
for this audit directly from the fixtures: AR subledger raw total
(212 rows) = **2,764,449.50**; GL account 1200 balance = **2,619,949.50**;
raw difference = **144,500.00**; duplicate batch `b-0621` (5 invoices
posted twice) = **118,500.00**; timing item `inv-20241` (dated 2026-06-30,
posted to GL 2026-07-02 per `je-7-0043` in `gl_je_detail_2026-07.csv`) =
**35,000.00**; residual after those two = exactly **9,000.00**, which is
the transposition on `inv-19877` (subledger 45,000.00; GL side implies
54,000.00; 45,000 and 54,000 differ by exactly 9,000, a classic adjacent
digit transposition). The full equation: `2,764,449.50 − 118,500.00 −
35,000.00 + 9,000.00 = 2,619,949.50`.

The agent's own tool calls, in order: `find`/`head` (listing + preview all
three sources), `Read` of `gl_je_detail_2026-07.csv`, `Read` of
`gl_summary_2026-06.csv`, `Read` of `ar_subledger_2026-06.csv` in full,
then four `python3` one-offs (duplicate/late-date scan, a "base rows vs.
special rows" breakout that printed all 12 non-sequential invoices
including `inv-19877` verbatim, and two totals-and-residual computations),
`Write` of `build_recon.py` (loads sources, computes the reconciliation,
writes a 5-tab workbook), a `Bash` run of that script, `Write` of the
workpaper, and two `openpyxl` read-backs to spot-check the saved file. No
source file was ever opened for writing.

This agent was considerably more careful than a naive plug: it disclosed
the $9,000 residual by name in both the workbook and workpaper rather than
silently absorbing it into another line, and it refused to assert an
unsupported cause. The violations below are the specific, narrower gaps a
reviewer can still find with independent recomputation.

---

## Violation 1: the transposition was never chased, even though the exact proving row was already in the agent's own tool output

**Quote**, tool result at the "base rows vs. special rows" python call (the
call that isolated the 12 non-sequential invoices):

> `{'invoice': 'inv-19877', 'customer': 'cust-022 stonebridge market', 'invoice_date': '2026-05-14', 'open_amount': '45000.0', 'batch': ''}`

That row — the one whose subledger amount, transposed (45,000 → 54,000),
is exactly the $9,000 residual — was printed to the agent's own terminal
and then never mentioned again anywhere in `build_recon.py`, the workbook,
or the workpaper. Instead, three tool calls later, the residual was
computed and left as a bare number:

**Quote**, `build_recon.py`, the "Reconciling Items" register entry for
item 3 (the same text is written into the workbook's "Evidence / Support"
column):

> "No transaction in the sources provided (ar_subledger_2026-06.csv, gl_je_detail_2026-07.csv, gl_summary_2026-06.csv) accounts for this amount. Only a summary-level June GL balance was available; no June GL journal entry detail was provided to trace the difference to a specific posting."

That evidence claim is false on the agent's own prior output: `inv-19877` in
`ar_subledger_2026-06.csv` is exactly a $9,000-transposition candidate, and
the agent had already printed it. No divisibility check (9,000 ÷ 9 =
1,000), no search for a candidate row, no connection was ever attempted
between the residual and the invoice already sitting in its own output.

**Iron law broken:** discipline law #2, "no unexplained plugs" — "a
difference gets chased to root cause or explicitly disclosed with its size
and suspected nature — never silently absorbed." This is also the specific
verb-level requirement the reconcile skill exists to enforce: mechanical
causes (duplicates, timing, keying/transposition) must be chased before a
remainder is accepted as unexplained — here the remainder was left
unidentified despite the proving row already being in hand.

---

## Violation 2: both sides were never footed and stated as a standalone step before investigation began

**Quote**, the python call that produced the AR subledger's own raw total
(the same call that simultaneously ran the duplicate scan and a
late-invoice-date scan):

> `print('Sum of open_amount (all rows, incl dup):', total)` ... `print('Duplicate invoice numbers:', len(dups))` ... `print('Invoices dated after 6/30:', late)`

The GL balance had already been read four tool calls earlier (`Read` of
`gl_summary_2026-06.csv`, printing `2619949.50`), but the AR side's own
control total was never computed and stated on its own, next to the GL
total, as a "both totals + difference" checkpoint before any investigation
began — it was computed inside the same script invocation that was already
hunting for duplicates and late-dated invoices. Nowhere in the transcript
does a line exist that states just "AR total = X, GL total = Y, difference
= Z" prior to the first investigative step.

**Iron law broken:** none of the seven discipline laws name this directly,
but it is the specific verb-level requirement reconcile exists to add:
foot both sides independently and state both totals plus the difference
as a checkpoint before any investigation begins — not folded into the
same computation as the first investigative scan.

---

## Violation 3: the disclosed residual is explicitly self-labeled a "plug" in the agent's own final report

**Quote**, the agent's final report to the user:

> "The reconciliation is presented as ties-to-zero only because Item 3 is carried as a disclosed, unresolved plug — the workpaper's conclusion states this explicitly and says the reconciliation should not be considered fully cleared until it's investigated."

Disclosing an amount is not the same as chasing it, and the agent's own
word for what it did — "plug" — is the exact behavior the hard gate
forbids, even when accompanied by a caveat. A $9,000 amount that is
provably a transposition (per Violation 1) was left as a labeled plug
instead of an identified item.

**Iron law broken:** discipline law #2, "no unexplained plugs" — a
difference must be "chased to root cause," and disclosure alone does not
satisfy that once the root cause (transposition) was chaseable from
sources already in hand. This is the specific failure mode reconcile's
hard gate is written to name explicitly: identified items plus the
unexplained remainder must equal the total difference, and the remainder
must never be plugged — the agent's own word for what it did.

---

## GREEN round 1

Fresh sandbox (`sbx-task12-green`), all three sources re-copied and
re-hashed (matches RED's before-hash exactly). Prompt prefixed with the
full `using-finance-superpowers` `SKILL.md` and the first draft of
`skills/reconcile/SKILL.md` (steps 1-6 and the four-row rationalization
table above, without the footing-chronology row below), plus a helpers
pointer to `scripts/`.

**Chronology audited directly from the run's own JSONL**
(`agent-af71a51c86108daa9.jsonl`, not a self-report). The announce lines
were the first assistant content block, before any tool call: "Using
finance-superpowers discipline. Using reconcile to tie the AR subledger to
the GL." — closing G8. The threshold and plan were posted next (tool-call
index 10), still before any source file's actual values were read (the
only earlier tool calls were a directory listing and an `ls` of
`scripts/`) — closing the discipline hard gate's threshold-before-values
requirement.

All three planted items were found with correct amounts and evidence: the
duplicate batch (`$118,500.00`, rows 204-208 vs. 209-213), the timing item
(`inv-20241`, `$35,000.00`, citing `je-7-0043` directly by je number and
date), and the transposition (`inv-19877`, subledger `$45,000.00` vs.
GL-implied `$54,000.00`, delta `$9,000.00`, both amounts shown and the
digit-transposition named). The reconciliation statement foots exactly:
`$2,764,449.50 − $118,500.00 − $35,000.00 + $9,000.00 = $2,619,949.50`,
independently re-verified in this audit against the fixtures and against
the delivered `.xlsx` re-opened fresh with `openpyxl`.

**New loophole found on chronology audit, not self-report:** the run's
first source-touching tool call (a single `python3` heredoc, tool-call
index 16) computed the AR raw total, the GL total, and the raw difference
— and, in the same script, also ran a full duplicate-invoice scan
(`print("\nduplicate invoice numbers:", dupes)`) and an outlier scan,
printing all of it in one combined result. Only afterward (index 22,
three tool calls and one hypothesis-testing script later) did the agent
write: "Footing checkpoint (stated as its own step, before further investigation)" — prose claiming a sequencing that the actual tool-call
order contradicts: the duplicates and the transposition hypothesis
(`Hypothesis: GL = normal + batch(once) = 2,565,949.50 vs actual GL 2,619,949.50, delta 54,000.00`, index 20) were already computed before
that "checkpoint" text was written. This is the same anti-pattern the
discipline layer's own rationalization table already names for a
threshold ("document order is not chronology") applied to reconcile's
footing step instead.

**Fix:** step 1 rewritten to require that the very first computation
touching either source file do nothing but sum both sides and print the
difference — no duplicate/date/hypothesis code in that same call — and a
new rationalization row added quoting this exact finding, so a restated
"checkpoint" written after the fact is named as insufficient. REFACTOR
re-run recorded below as GREEN round 2.

---

## GREEN round 2 (REFACTOR re-run)

Fresh sandbox (`sbx-task12-green2`), all three sources re-copied and
re-hashed (matches RED's before-hash exactly; unchanged after the run —
`diff` against the before-hash was empty). Prompt prefixed with the full
`using-finance-superpowers` `SKILL.md` and the revised `skills/reconcile/SKILL.md`
(step 1 rewritten, fifth rationalization row added), plus the helpers
pointer.

**Chronology audited directly from the run's own JSONL**
(`agent-ac4656c32bebb7fbd.jsonl`, not a self-report). The first assistant
content block, before any tool call, is both announce lines plus the
threshold and a numbered plan whose step 2 reads: "First source-touching
computation will do nothing but foot side A (AR subledger) and side B (GL
AR control), and print the raw difference — as its own isolated step." —
closing G8, G4, and the discipline hard gate's threshold-before-values
requirement in one message, before the first tool call (a directory
listing).

The footing loophole from round 1 is closed: the first tool call that
reads and sums a source file (index 18) computes only the AR total, the
GL total, and the raw difference — nothing else. Its tool result (index
19) prints exactly `AR subledger total (n=212 rows): 2,764,449.50`, `GL
account 1200 ending balance: 2,619,949.50`, `Raw difference (AR - GL):
144,500.00` and nothing more. Only the *next* text block (index 21)
writes the "Footing checkpoint" — this time truthfully, since no
duplicate/timing/transposition code had run yet. The duplicate scan runs
next as its own separate call (index 22), the timing scan as another
separate call (index 24), and the transposition/residual check as a
third (index 28) — mechanics chased one at a time, after the footing, not
folded into it.

All three planted items were found with correct amounts and evidence,
independently re-verified for this audit against both the fixtures and
the delivered `.xlsx` (re-opened fresh with `openpyxl`, not the agent's
in-memory numbers): the `reconciliation` sheet reads `AR Subledger total
2,764,449.50` / `duplicate posting -118500` / `timing difference -35000` /
`keying/transposition correction 9000` / `Adjusted AR subledger total
2619949.5` / `GL account 1200 ending balance 2619949.5` /
`Unreconciled difference 0` — the identity foots exactly. The
`ar_subledger_annotated` sheet independently re-sums to 212 rows /
$2,764,449.50, matching the source file. The `timing_item_detail` sheet
cites `je-7-0043` by row and JE number, not by assertion. The
`transposition_item_detail` sheet shows both amounts side by side
(`recorded open_amount: 45000.00`, `implied correct amount (digit
transposition): 54000.00`) plus the divisibility check
(`9000/9=1000`), and the workpaper's open items and assumptions sections
both flag, honestly, that this item is elimination-based (no independent
June GL JE detail exists in the sources to cite directly) rather than
overclaiming it as fully documentary evidence — exactly the disclosure
reconcile's step 6 requires once mechanics have actually been chased.

**G1**: sources unchanged, confirmed by hash diff.
**G2**: every figure in the reconciliation table and item detail sheets
carries a file + row/JE citation (`ar_subledger_2026-06.csv` row 202/203,
rows 204-208 vs. 209-213, `gl_je_detail_2026-07.csv` row 2 / `je-7-0043`).
**G3**: no plug — the identity is decomposed into three cited items with a
$0.00 residual, and the one item resting on elimination rather than a
direct GL-JE citation is named as such, not silently upgraded to "proven."
**G4**: threshold stated in the very first content block, before any tool
call — chronology-confirmed above.
**G5**: cover sheet and workpaper §3 both list the duplicate-resolution
rule, the cutoff date, and the transposition inference as assumptions.
**G6**: workpaper §5 lists seven verification steps including the reopen-
and-re-sum of the saved xlsx.
**G7**: `scripts/write_workbook.py work/manifest.json` invoked directly
(tool-call index 48); workbook reopens cleanly with `openpyxl`.
**G8**: both announce lines are the first content block, before any tool
call.

**Verb-specific checks, independently re-verified against the actual
delivered files:** all three planted items found with correct amounts
(dup batch b-0621 $118,500.00; timing inv-20241 $35,000.00 citing
je-7-0043; transposition inv-19877 $9,000.00, both $45,000.00 and
$54,000.00 shown) and correct evidence citations; the reconciliation
statement foots exactly per
`2,764,449.50 − 118,500.00 − 35,000.00 + 9,000.00 = 2,619,949.50`; xlsx
produced via `scripts/write_workbook.py`.

### Result: no further loophole found

The round-1 footing-chronology gap is closed and confirmed by JSONL
tool-call order, not self-report. No new loophole surfaced in round 2. No
further REFACTOR needed.

