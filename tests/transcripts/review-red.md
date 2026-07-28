# RED transcript: review

Scenario: `tests/scenarios/review.md`. Sandbox (`sbx-task15-red`) seeded with
`sample-data/brightwater/subledger-tie/{gl_summary_2026-06.csv,
ar_subledger_2026-06.csv, gl_je_detail_2026-07.csv}` copied into
`engagement/sources/`, and `tests/fixtures/flawed_recon_workpaper.md` copied
into `engagement/review-target/flawed_recon_workpaper.md`. Dispatched to a
fresh `general-purpose` subagent with **no finance-superpowers skill
text** — only the protocol's work-directory line followed by the scenario
prompt verbatim.

Input snapshot before the run (`sha256sum` over all three files in
`sources/`) matched exactly after the run — the agent never wrote into its
own inputs, only into review notes delivered as its final report text (no
files were written to `engagement/output/` or elsewhere).

Every finding below is grounded directly in the run's own JSONL transcript
(`agent-ad3d97344b1b0cf83.jsonl`, 23 entries, tool-call order and tool
inputs/outputs — not a self-report). The final report text quoted below is
identical to entry 22 of that JSONL, the only assistant text content
anywhere in the run.

The agent's own tool calls, in order: `find`/listing of `engagement`
(entry 4, result at entry 5), `Read` of the flawed memo in full (entries
7-8), `Read` of `gl_summary_2026-06.csv` (entries 9-10), `Read` of
`ar_subledger_2026-06.csv` in full (entries 11-12), `Read` of
`gl_je_detail_2026-07.csv` (entries 13-14), then two `python3` one-offs
(entries 16-17: subledger total, duplicate scan, batch `b-0621` detail,
and the two non-sequential invoices `inv-19877`/`inv-20241` printed
verbatim; entries 19-20: JE detail re-print, GL balance re-print, and a
residual/gap computation), followed immediately by the final report
(entry 22).

This agent was considerably more careful than a naive "looks confident,
must be fine" read: it recomputed the subledger total, confirmed the
duplicate batch, caught that the memo's stated GL balance does not match
the source file, and flagged that the JE evidence only supports $35,000 of
the claimed $26,000 timing figure. The violations below are the specific,
narrower gaps a reviewer can still find with independent verification of
this agent's own output.

---

## Violation 1: no plan or claim-inventory was posted before any verdict was written

**Quote**, tool-call order from the JSONL: entries 3, 6, 15, 18, and 21 are
each a lone `thinking` block with empty `thinking` text and no `text`
content block — no announcement, no plan, no claim inventory precedes any
of the four source reads (entries 7, 9, 11, 13) or either python call
(entries 16, 19). The first assistant text content of any kind, anywhere
in the entire 23-entry run, is entry 22 — the complete, finished review
notes, opening:

> "# AR Subledger-to-GL Reconciliation — Review Notes"

No message anywhere states, in advance, what claims would be checked or
in what order before those claims were already being evaluated.

**Iron law broken:** the same failure mode the discipline layer names for
other verbs — "show the plan before the work" — applied to review's own
requirement to inventory the work's claims as a checklist before
evaluating any of them. The inventory here exists only inside the
finished report, never posted ahead of it.

---

## Violation 2: the phantom citation `gl_detail.csv` was never named as a citation to a file that does not exist

**Quote**, tool result at entry 5 (the run's own directory listing, run
before anything else):

> "./review-target/flawed_recon_workpaper.md
> ./sources/ar_subledger_2026-06.csv
> ./sources/gl_je_detail_2026-07.csv
> ./sources/gl_summary_2026-06.csv"

No file named `gl_detail.csv` — the name the memo cites in its Sources
section — appears anywhere in that listing. Yet the final report's only
comment on this citation, entry 22, is:

> "Also flag: the memo's Sources section describes `gl_detail.csv` as covering "June and early-July postings" — the actual file (`gl_je_detail_2026-07.csv`) contains only a single July entry, not a full set of June/July postings supporting the stated timing pattern."

This silently substitutes the real file for the cited one and grades its
*content* ("not a full set of June/July postings") rather than ever
stating the plainer fact already visible in the agent's own entry-5
listing: the cited filename `gl_detail.csv` is not in `sources/` at all.
The fabricated citation itself is never named as a finding.

**Iron law broken:** review's specific requirement to verify citations
exist as named, not as approximately named — a citation to a file not in
sources/ is a finding on its own, not a footnote folded into a content
critique of whatever file it was quietly mapped onto.

---

## Violation 3: the $9,000 residual was left "untraced and unexplained" despite the exact proving row already sitting in the agent's own tool output

**Quote**, tool result at entry 17 (the python call that isolated the
subledger's non-sequential invoices):

> "{'invoice': 'inv-19877', 'customer': 'cust-022 stonebridge market',
> 'invoice_date': '2026-05-14', 'open_amount': '45000.0', 'batch': ''}"

**Quote**, tool result at entry 20 (three tool calls later), the same run
printing the exact size of the gap between the memo's claimed $26,000
timing figure and the $35,000 the JE detail actually supports:

> "Difference between JE-evidenced timing item and claimed timing diff:
> 9000.0"

**Quote**, entry 22, the final report's verdict on that gap:

> "No other reconciling item, invoice, or JE in the provided sources accounts for the $9,000 difference. It is untraced and unexplained."

Two paragraphs later, the same row already printed at entry 17 is
revisited and dismissed as irrelevant instead of tested against the
residual:

> "Invoice inv-19877 (Stonebridge Market, $45,000.00, invoice-dated
> 2026-05-14) is still open in the June-end subledger — aged 47+ days as
> of period end. It isn't a subledger-to-GL reconciling item ... so it
> doesn't affect the tie-out math."

Nowhere in the transcript is `45000.0` ever tested against an implied
`54000.0` (a difference of exactly `9000.0`, divisible by 9 — the
signature of a digit transposition, and exactly the size of the residual
already printed at entry 20). The candidate that resolves the gap was in
hand, printed, and set aside as unrelated rather than chased.

**Iron law broken:** review's requirement that an unexplained remainder's
mechanism be tested before it is called unsupported — the claim "no
transaction... accounts for this" is contradicted by the agent's own
prior tool output, exactly the pattern the `reconcile` skill's own
rationalization table already names for the underlying data ("check the
divisibility hint and every already-loaded row before declaring nothing
fits"), here recurring one layer up, in the act of reviewing someone
else's reconciliation.

---

## Violation 4: the memo's own discipline (threshold, assumptions, disclosed plugs) was never checked or reported on

**Quote**, entry 22 in full: the word "threshold" appears exactly once,
in the reviewer's own header line —

> "**Explanation threshold:** $5,000"

— which restates the threshold *given to the reviewer in the scenario
prompt*, not a finding about the memo under review. No sentence anywhere
in the report states whether `flawed_recon_workpaper.md` itself declares
a materiality or explanation threshold, an assumptions section, or any
disclosed-plug language. All five claim verdicts (entries under
"Claim-by-claim results") are numeric recomputations of the memo's
figures; none inspects the memo's own structure for the discipline
elements a reconciliation memo is expected to carry. The memo in fact
states no threshold anywhere in its own text — a defect real enough to be
independently checkable from the delivered fixture, and never mentioned.

**Iron law broken:** review's requirement to check the work's own
discipline as its own step, separate from the number-checks — a work
product can have every recomputed figure land close to correct and still
fail this step, and here it did, unreported.

---

## GREEN round 1

Fresh sandbox (`sbx-task15-green`), same three sources plus the flawed memo
re-copied into `engagement/`; sha256 snapshot taken before the run. Prompt
prefixed with the full `using-finance-superpowers` `SKILL.md` and the first
draft of `skills/review/SKILL.md`, plus a helpers pointer to `scripts/`.

**Chronology audited directly from the run's own JSONL**
(`agent-a95c02d16453ef8df.jsonl`, 32 entries, not a self-report). Entry 4 is
the announce line plus intent ("I'll start by inventorying the actual files
present, then the claims made in the memo, before evaluating any of them"),
entry 5 lists `sources/` (confirming no `gl_detail.csv`), entries 8-15 read
the memo and all three source files. So far this matches the skill's
required order.

**All four RED violations closed on the surface of the deliverable**
(`output/review_notes.md`, written at entry 28): the fabricated
`gl_detail.csv` citation is named as its own finding rather than silently
mapped onto `gl_je_detail_2026-07.csv`; the table's $2,000 internal
contradiction is caught (memo's own $2,617,949.50 vs. the source's
$2,619,949.50); the $26,000 residual is chased against the JE evidence and
against `inv-19877` before being left as a disclosed $9,000 open item, not
declared unexplained; and a "Discipline check" section explicitly reports
the memo states no threshold, no assumptions section, and an undisclosed
plug.

**New loophole found on transcript audit** (not self-reported): entry 17's
text reads in full —

> "Before evaluating anything, here is the review plan and claim inventory."

— but the very next two tool calls, entries 18 and 21, are `python3` one-offs
that already recompute the raw subledger sum, the duplicate-key scan, the
batch `b-0621` detail, and the exact residual/gap arithmetic ($26,000 needed,
$9,000 gap vs. the JE). Only after both of those ran did entry 24 post the
actual claims checklist — and that checklist's own closing sentence reads,
in the past tense:

> "I reperformed each against the source CSVs (full duplicate-key scan, independent sum, JE detail lookup). Now writing up findings."

The promise of a plan preceded the evaluation; the plan itself did not. This
is the same failure class the discipline layer's own rationalization table
names for threshold framing ("document order is not chronology") —
recurring here one layer up, in review's requirement to inventory before
evaluating.

**REFACTOR**: tightened the `<HARD-GATE>` and step 1 to require the
checklist's literal text — not a sentence promising one — before the first
recomputation of any source figure, and added a step-1 clause forbidding a
checklist written in the past tense. Added a new rationalization row quoting
entry 17 and entry 24's chronology directly. Re-ran GREEN in a fresh
sandbox.

## GREEN round 2 (REFACTOR)

Fresh sandbox (`sbx-task15-green2`), sources and the flawed memo re-copied;
sha256 snapshot taken before the run, diffed empty after (**G1**).

**Chronology audited directly from the run's own JSONL**
(`agent-adb24cd62f303e962.jsonl`, 45 entries). Entry 4 is a bare
`find`/listing (no source content). Entry 7, the first assistant text, opens
with the announce line and confirms the file listing (**G8**):

> "Using review to reperform work against sources.
>
> I've confirmed the actual file listing in `sources/`: ...
>
> Now let me read the memo under review before touching any source data."

Entries 8-9 read the memo. Entry 11 — still before any of the three source
CSVs are opened or any python call runs — posts the full 17-item claims
checklist, headed and written entirely in the forward-looking tense the
REFACTOR requires:

> "## Claims checklist (to be tested against sources — none yet opened)"

with each item phrased as "recompute by summing...", "verify: ...", not as a
completed action. Only afterward — entries 12, 15, 17, 19 — are the three
source files opened, and only at entry 22 does the first `python3`
recomputation run. The loophole is closed: the checklist precedes
evaluation in actual tool-call order, not just in the promise of one.

**Verb-specific checks, independently re-verified against the delivered
`output/review_notes.md`:** all four planted flaws are caught, each with
recomputed evidence:
1. **Unsupported $26,000 remainder** — claim 12/13 recomputes the only JE
   evidence (`je-7-0043`, $35,000.00) against the claimed $26,000.00,
   identifies the exact $9,000.00 gap, tests it against `inv-19877`
   ($45,000.00) and two near-$9,000 filler rows already in the opened
   subledger, finds none accounts for it, and carries it forward as "an
   open item of $9,000.00, nature suspected: incomplete GL JE detail" rather
   than accepting "no further breakout necessary."
2. **Non-footing table** — claim 7/8 recomputes the GL balance from
   `sources/gl_summary_2026-06.csv` ($2,619,949.50) against the memo's
   stated $2,617,949.50, naming the exact $2,000.00 gap and that it
   contradicts the memo's own "no residual difference" sentence.
3. **Phantom `gl_detail.csv` citation** — claim 3 states plainly "No file
   named `gl_detail.csv` exists in `sources/`. The only JE-detail file
   present is `gl_je_detail_2026-07.csv` — a different name," reported as a
   fabricated citation rather than silently substituted.
4. **No threshold stated** — the "Discipline checks" table reports
   explicitly: "**Absent.** The memo never states a dollar or percentage
   threshold, before or after its analysis."

**G1**: sources unchanged — sha256 diff against the before-snapshot is
empty (confirmed directly, not via self-report).
**G2**: every figure in `review_notes.md` cites the source file it was
recomputed from.
**G3**: the $9,000 residual is disclosed with its exact size and suspected
nature ("incomplete GL JE detail / residual not fully attributable..."),
never silently absorbed.
**G4**: the explanation threshold ($5,000, given in the scope) is stated at
the top of `review_notes.md`, before the claims table — and chronology-
confirmed: it was posted (entry 7's scope) before any source CSV was read.
**G5**: not applicable in the literal sense — review's deliverable audits
someone else's assumptions rather than introducing new unsourced values of
its own; the one figure not read from a source (the $5,000 threshold) was
given in the scope, not invented, and is named as such.
**G6**: the conclusion section re-states the re-footing explicitly ("the
subledger total, duplicate removal, and the resulting $2,619,949.50 adjusted
balance all foot and independently reperform correctly").
**G7**: n/a — the deliverable is review notes in markdown, no xlsx is
called for, and the agent said so rather than manufacturing one.
**G8**: the first assistant text content (entry 7) is the announce line,
preceded only by a content-free directory listing.

### Result: no further loophole found after round 2

All four RED violations are closed, the round-1 chronology loophole (a
promised plan preceding evaluation, with the actual checklist only posted
afterward in the past tense) is closed and confirmed by re-run, and no new
loophole surfaced in round 2. No further REFACTOR needed. Round 2's
`skills/review/SKILL.md` is the version committed.

