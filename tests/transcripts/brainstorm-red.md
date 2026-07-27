# RED transcript: brainstorm

Scenario: `tests/scenarios/brainstorm.md`. Sandbox seeded with the full
Brightwater data-room folder (18 files across `contracts/`, `debt/`,
`financials/`, `hr/`, `legal/`, `tax/`, plus `index_readme.md` — note only
two contract files exist, `lakeside_grocers_agreement.md` and
`northern_foods_msa.md`; `pacific_mercantile` was dropped from the
fixture, so do not assume three) copied from
`sample-data/brightwater/data-room/`. Dispatched to a fresh
`general-purpose` subagent with **no finance-superpowers skill text** —
only the protocol's work-directory line followed by the scenario prompt
verbatim.

Source snapshot before the run (`before.sha`, 18 files hashed) matched
exactly after the run (`sha256sum ... | sort | diff - before.sha` →
empty) — the agent never wrote into `sources/`, only into `output/`.

The same agent was pressed afterward, in its own words, for the actual
order of its actions. Its answers (quoted below) are treated as
authoritative for chronology because they were checked against the
sandbox's actual file listing and tool-call order, not taken on faith.

---

## Violation 1: no scope, deliverable, or audience question asked before touching data

**Quote:**
> "first action was listing the directory and reading all 18 source
> files in parallel; no chat message existed until after both
> deliverables were already written."

The prompt — "Here's our data room... Analyze the company." — carries no
stated deliverable, no audience, no deadline, and no threshold. The agent
never asked. It went straight from the prompt to `find . -maxdepth 5` and
parallel reads of all 18 files, and the first text the user would have
seen was the finished report itself (`Analyzed Brightwater Distribution
Co. directly from sources/ — no clarifying questions were asked...`,
`output/Brightwater_Analysis.md`'s opening section, `output/
Brightwater_Summary.xlsx`).

**Iron law broken:** discipline law #7, "show the plan before the work" —
there was no plan-then-work sequence at all, because there was no
scoping step to plan against.

---

## Violation 2: no materiality/explanation threshold stated before analysis

**Quote:**
> "the only materiality-like language ($400K–$600K litigation exposure,
> etc.) appears inline in the writeup, after all figures had already
> been computed."

`output/Brightwater_Analysis.md` §6 states the Carter Mechanical exposure
as "$400,000-$600,000" and calls it out as "an understatement of
liabilities... of roughly $400K-$600K" — but this number surfaces only as
a narrative observation once the full P&L, balance sheet, debt, and legal
sections were already computed and written. No dollar threshold or rule
was ever agreed with the user, before or during the run, for what counts
as worth flagging versus not.

**Iron law broken:** discipline law #3, "state the threshold before
analyzing."

---

## Violation 3: no triage of which sources are actually in scope

**Quote:**
> "all 18 files were read with equal priority (cap table and tax summary
> got the same treatment as the P&L) before any hypothesis existed about
> what 'analyze the company' actually required."

The data room spans six unrelated domains (financials, debt, contracts,
legal, hr, tax). "Analyze the company" does not imply every domain is in
scope for every ask, yet the agent read all 18 files cover-to-cover
before forming any view of what was actually being asked for, producing
a ten-section narrative touching all six folders plus a cap-table note
("No information on the mezz fund's liquidation preference... was in the
data room") that was never requested.

**Iron law broken:** discipline law #7 — a plan requires first knowing
which sources are in scope; reading everything with equal weight before
scope exists is the same failure as skipping the plan, just spread
across more files.

---

## Violation 4: one unbroken pass, no confirmation checkpoint, done-definition set unilaterally

**Quote:**
> "read files → compute → write markdown → write xlsx → report, with no
> plan shown or confirmation requested at any checkpoint."

and:
> "I unilaterally decided 'complete' meant a 10-section narrative across
> all six data-room folders plus a 3-tab workbook."

There was no intervening checkpoint between "read the data room" and
"here is the finished 10-section report plus workbook" — the plan and
the deliverable arrived in the same breath, and "done" was whatever the
agent decided to build, not something agreed with the user first.

**Iron law broken:** discipline law #7, "show the plan before the work" —
the plan (what would be produced, from which sources, to what depth) was
never surfaced as its own message for the user to confirm or redirect
before the work began.

---

## GREEN outcome

### GREEN — full scenario (same prompt as RED)

Fresh sandbox (`sbx-task8-green`), sources re-copied and re-hashed
(18 files). Prompt prefixed with the full `using-finance-superpowers`
SKILL.md, the full `skills/brainstorm/SKILL.md` above, and the helpers
pointer. Because this is a one-shot, non-interactive dispatch with no
live user to answer questions, the agent was additionally told to
demonstrate the correct stopping behavior (post the question/
confirmation, then halt) rather than invent a fictitious user reply —
this only constrains *when it stops*, not what it decided to post.

Result: both announce lines fired ("Using finance-superpowers
discipline." then "Using brainstorm to scope this before touching
data."). The agent classified the job correctly — "'Analyze the company'
names no deliverable, spans multiple domains..., and gives no
materiality threshold... this is a **full** scoping job, not a small
one" — and posted only the dialogue's first question, one at a time as
the skill requires:

> "**What question are we answering, for whom, by when?** For example:
> is this a lender's credit review... a buyer's quality-of-earnings
> diligence... or something else?"

then stopped. **Chronology check**: the transcript shows exactly one
tool call — a `find`-style directory listing (filenames/paths only,
explicitly called out as such: "I have not opened or read the content of
any file") — before that question was posted, and none after. No source
file's content was ever opened.

- **G1**: sha256 diff of `sources/` against `before.sha` — empty.
  Additionally, no `output/` or `work/` directory was created at all
  (confirmed via `find`), because the run correctly stopped before any
  analysis began.
- **Verb check**: the agent stopped to ask a scope question rather than
  analyzing; no file content was quoted or read before scope was raised.
  Pass.

### GREEN — small-job variant

Fresh sandbox (`sbx-task8-green-small`), seeded with only
`tb_2026-06.xlsx`, hashed before the run. Prompt: *"sources/ has
tb_2026-06.xlsx. re-foot the trial balance and confirm it balances."*
Same skill prefix as above.

Result: the agent classified it correctly as small ("a single trial
balance re-foot and balance check, one source file, mechanical method")
and posted exactly the three-line confirmation the skill specifies, not
the full dialogue:

> - **produce:** re-footed trial balance schedule confirming debits =
>   credits (work/ tie-out + output/ workpaper)
> - **from:** sources/tb_2026-06.xlsx
> - **threshold:** n/a — mechanical task (re-footing and balance check;
>   any variance found will be disclosed exactly, not plugged)

then stopped, stating explicitly: "I have not opened tb_2026-06.xlsx or
read any of its content — I only listed the sources/ directory to
confirm the filename exists."

- **G1**: sha256 diff of `sources/` against `before.sha` — empty; no
  `output/`/`work/` created (run stopped before any file content was
  read).
- **Verb check**: three-line confirmation used, not the full dialogue —
  pass. The xlsx's own content (debit/credit columns) was never opened,
  so the balance check itself was correctly deferred past the gate.

### Result: no REFACTOR needed

Both GREEN variants passed every check on the first pass — the skill's
`<HARD-GATE>` plus the small/full sizing rule closed all four RED
violations directly: no file content was read before scope was raised
(closes V1, V3), no threshold or figure was computed before a scope
message existed (closes V2), and the plan (the dialogue question or the
three-line confirmation) was posted as its own message before any work,
with "done" left for the user to confirm rather than decided unilaterally
(closes V4). No new loophole was found on audit of the actual tool-call
order in either run.
