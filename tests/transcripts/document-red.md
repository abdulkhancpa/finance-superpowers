# RED transcript: document

Scenario: `tests/scenarios/document.md`. Sandbox (`sbx-task14-red`) seeded with
`sample-data/brightwater/data-room/legal/pending_litigation.md` and
`sample-data/brightwater/data-room/financials/balance_sheet_fy2025.md` copied
into `engagement/sources/`. Dispatched to a fresh `general-purpose` subagent
with **no finance-superpowers skill text** — only the protocol's work-directory
line followed by the scenario prompt verbatim.

Input snapshot before the run (`sha256sum` over both files in `sources/`)
matched exactly after the run — the agent never wrote into its own inputs,
only into `build_memo.py` and the deliverable in `engagement/`.

Every finding below is grounded directly in the run's own JSONL transcript
(`agent-a5301e97b53110416.jsonl`, 39 entries, tool-call order and tool
inputs/outputs — not a self-report), plus the actual delivered file
(`Brightwater_Litigation_Diligence_Memo.docx`, read back with `python-docx`
for this audit, not trusted from the agent's own report).

This agent produced a memo that leads with the headline finding (unlike the
brief's anticipated "buries the headline mid-memo" corner-cut, this run's
"Bottom Line" section is the very first body content and does state the
probable claim, the $400,000–$600,000 range, and the fact that nothing is
accrued, citing both files' substance in prose) and it chose a `.docx`
deliverable rather than the markdown memo the task calls for. The violations
below are the specific, narrower gaps a reviewer can still find.

---

## Violation 1: no plan or announcement was posted before source values were read

**Quote**, tool-call order from the JSONL (entries 3–10): the first tool call
of the run is a `find` listing filenames only, followed immediately — with no
assistant text block in between — by two back-to-back `Read` calls on both
source files. The tool result of the second `Read`, the first point either
source's actual content enters the run, is:

> 1	# brightwater distribution co. — balance sheet 2025-12-31 (unaudited)

No text of any kind — no announce line, no statement of what memo would be
produced, no plan — precedes that read. The first assistant text content
anywhere in the run appears only at the very end (entry 38), after the
`.docx` had already been built, run, and delivered via `SendUserFile`:

> ## What I produced
>
> Read both source documents in `sources/` and built a diligence finding memo for the acquirer's CFO/deal team:

**Iron law broken:** discipline law #7, "show the plan before the work" — a
short summary of what's about to be produced, then produce it. The plan here
is narrated only after the deliverable already exists, in the final report,
not posted as its own message beforehand.

---

## Violation 2: factual sentences carry no per-sentence source citation

**Quote**, memo body, extracted from the delivered `.docx` paragraphs:

> Brightwater's balance sheet as of 12/31/2025 carries no reserve for a litigation loss that the Company's own outside counsel has assessed as probable, with an estimated range of $400,000–$600,000.

This sentence blends a fact from `pending_litigation.md` (counsel's
probability assessment and range) with a fact from `balance_sheet_fy2025.md`
(no reserve carried) with no citation of either file. The only sourcing
anywhere in the memo is one generic header table row near the top:

> ['Sources:', 'Pending Litigation Summary (outside counsel); Unaudited Balance Sheet, 12/31/2025 (data room)']

Every other factual sentence in the memo — the accounting-analysis section,
the financial-statement-impact section, the deal-implications section —
relies on that single top-of-memo attribution and never again names which
file (or line/row) a given number or claim comes from. A reader who was not
in the room cannot tell, sentence by sentence, whether a given figure traces
to the litigation summary or the balance sheet.

**Iron law broken:** discipline law #1, "every number ties to a source. every
figure in a deliverable cites its file (and sheet/range or row). no
ungrounded numbers."

---

## Violation 3: an external accounting conclusion is asserted as established fact, never labeled as the preparer's own analysis

**Quote**, memo section 2 ("Accounting Analysis — This Is a GAAP Departure,
Not Just a Disclosure Gap"):

> Under ASC 450-20 (Loss Contingencies), a loss must be accrued by a charge to income when both of the following conditions are met: (a) it is probable that a liability has been incurred, and (b) the amount of loss can be reasonably estimated.

and, more starkly:

> Brightwater has recorded $0, which is not a GAAP-compliant outcome under any reading of the facts as presented.

Neither `pending_litigation.md` nor `balance_sheet_fy2025.md` mentions ASC
450-20, GAAP, or any accounting standard — this entire section is external
technical authority the agent introduced on its own, then stated as flat,
settled fact ("is not a GAAP-compliant outcome under any reading") rather
than as the diligence team's own interpretation subject to further legal or
accounting review. Nothing in the memo distinguishes "what the sources say"
(counsel's probability/range assessment; the balance sheet's zero accrual)
from "what we conclude by applying an outside framework to those facts" — the
two are asserted in the same declarative voice throughout the section.

**Iron law broken:** this is the same failure mode as
`using-finance-superpowers`' established rationalization "i know this number
is right... cite it anyway. every figure, every time" — extended to
conclusions, not just figures: an inference is presented with the same
certainty as a sourced fact, with no signal to the reader that it is an
inference at all.

---

## Violation 4: no dedicated assumptions/limitations section — hedges are buried inline instead

**Quote**, the only hedge in the entire memo, buried as a parenthetical inside
section 1's third bullet rather than surfaced anywhere as its own section:

> Counsel represents this is the only material litigation matter ("no other material matters"); we have not independently verified completeness of this representation (see §4).

The memo's closing line functions as a partial substitute —

> Prepared for internal deal team use based solely on the two data room documents identified above; not a legal opinion. Figures in USD.

— but this names no assumptions (e.g., that counsel's representation of
completeness is taken at face value, that the balance sheet's own "no
litigation or contingency reserves are recorded" line is itself accurate and
complete) and provides no "prepared by" / reperformability block. Section 5
("Open Items") lists follow-up requests, which is not the same thing as an
assumptions section: an open item is something still to be chased; an
assumption is a value or premise taken as given in the meantime. The memo
never separates the two.

**Iron law broken:** discipline law #4, "no hardcodes... any value not traced
to a source file... is marked as an assumption in the workpaper's assumptions
section — never buried in a formula or script" (here: never buried in a
parenthetical mid-paragraph).

---

## GREEN round 1

Fresh sandbox (`sbx-task14-green`), both sources re-copied and re-hashed
(matches RED's before-hash exactly; unchanged after the run — `diff` against
the before-hash was empty). Prompt prefixed with the full
`using-finance-superpowers` `SKILL.md` and `skills/document/SKILL.md`, plus a
helpers pointer to `scripts/`.

**Chronology audited directly from the run's own JSONL**
(`agent-af52f21ec6f0b8ce6.jsonl`, 22 entries, not a self-report). The first
tool call is a `find`/file-listing (no source content). The first assistant
text block, entry 7, is both announce lines plus the plan and threshold in
one message — posted **before** either source file is opened:

> Using finance-superpowers discipline. Using document to write a diligence finding memo on litigation exposure for the acquirer's CFO.
>
> **Plan:** I will read the two source files in `sources/` ... **Threshold (stated before opening any source file):** ...

Only after that message do entries 8 and 10 (`Read` on `pending_litigation.md`
then `balance_sheet_fy2025.md`) touch source content. This closes Violation 1
and G4/G8, confirmed by tool-call order, not prose.

**Violation 2 (no per-sentence citation) and Violation 4 (no assumptions
section) closed:** the delivered `output/litigation_finding_memo.md` cites a
source file and line for essentially every factual sentence (e.g. "no
litigation or contingency reserves are recorded" `sources/balance_sheet_fy2025.md`,
line 15"), carries a dedicated Assumptions section (four items, including the
threshold, the range-midpoint convenience, and the accrual-framework
reference explicitly labeled "reflects the reviewer's application of an
external accounting framework... this is an inference... not a statement
either source makes itself"), a separate Limitations section, and six Open
items each naming a closing document.

**Violation 3 (outside framework stated as flat fact) closed:** the memo's
only reference to an accrual framework is in the Assumptions section, labeled
explicitly as an inference — quote above — never stated in the declarative,
settled voice RED used ("is not a GAAP-compliant outcome under any reading of
the facts as presented").

**Loophole found:** the memo's Headline finding paragraph cited only
`sources/balance_sheet_fy2025.md` (for the "no reserve recorded" fact) and
never named `sources/pending_litigation.md` inline for the counsel
probable-loss/range claim in that same paragraph — the file name appeared
only in the header's "Sources examined" line and in the Basis section
immediately below. That is exactly the failure mode rule 2 and rationalization
row 1 warn against ("one sources line at the top of the memo is not a
citation for every sentence below it") — applied here to the memo's own most
important paragraph. Skill rule 1 was tightened to require the headline to
name every source file it draws from inline, not just in a header block
above it, and GREEN was re-run.

## GREEN round 2 (REFACTOR)

Fresh sandbox (`sbx-task14-green2`), sources re-copied and re-hashed;
unchanged after the run (`diff` against before-hash empty — **G1**).

**Chronology audited directly from the run's own JSONL**
(`agent-a6267036b4e967796.jsonl`, 36 entries). Entry 4, the first assistant
text, is the announce line only ("Using finance-superpowers discipline.
Using document to write a diligence finding memo for the acquirer's CFO.")
followed by a folder-listing `ls` (no source content) at entry 5, then entry
8 is the full plan and threshold — **G4**, **G8**:

> **Threshold (stated before reading source files)**
>
> For this litigation-exposure memo, I will apply the following materiality/explanation threshold: Any individual litigation matter with disclosed or estimated exposure ≥ $25,000, or ≥ 1% of Brightwater's total stockholders' equity (per the balance sheet), whichever is lower...

Only afterward, entries 9 and 11, are `Read` calls on `pending_litigation.md`
then `balance_sheet_fy2025.md` — the plan and threshold precede any source
value being read, tool-call order confirmed.

**Loophole closed:** the Headline finding paragraph in
`output/litigation_finding_memo.md` now names both files inline in the same
sentence:

> Outside counsel assesses a **probable** loss of **$400,000–$600,000** in *Carter Mechanical v. Brightwater US* (`pending_litigation.md`, rows 2–4), and Brightwater's unaudited FY2025 balance sheet confirms **no litigation or contingency reserve has been recorded** for this or any matter (`balance_sheet_fy2025.md`, row 15) — meaning reported equity of $6,530,000 (`balance_sheet_fy2025.md`, row 13) excludes a loss counsel itself calls probable and equal to 6.1%–9.2% of that equity balance.

**Verb-specific checks, independently re-verified against the delivered
`output/litigation_finding_memo.md`:** the first paragraph states the finding
— probable, $400,000–$600,000, nothing accrued — citing both files, as
quoted above. Every factual sentence in Basis/Detail cites a file and row
(cash/AR/inventory/fixed-asset sub-totals used in one "What we computed"
re-footing sentence are the one place a component figure isn't individually
re-cited inline, though the same values were already cited by row two
sentences earlier and the full computation is pointed to
`work/litigation_exposure_calc.csv`). A dedicated Limitations section and a
six-item Open items section are both present, each open item naming a
specific closing document.

**G1**: sources unchanged, confirmed by hash diff (empty).
**G2**: every figure in the memo and workpaper cites a source file and row.
**G3**: no plug — the Verification section states plainly "Confirmed no plug
or netting was introduced," and all six open items carry exact amounts (or
"unquantifiable with sources on hand" where genuinely unquantifiable) with
suspected nature.
**G4**: threshold and plan posted as their own message before either source
file was read — chronology-confirmed above via JSONL tool-call order.
**G5**: a five-item Assumptions section, none buried in a formula — including
the accrual-framework mapping and the range-midpoint/low-end conventions,
each explicitly labeled as the reviewer's own convention, not a sourced
number.
**G6**: the memo's Verification section independently recomputes the balance
sheet re-footing and the exposure ratios by Python (matching the memo's own
figures), and confirms both delivered files re-open cleanly.
**G7**: n/a — the deliverable is a markdown memo; no xlsx was produced, which
is the correct call for a two-document qualitative finding (the agent said so
explicitly rather than manufacturing an unnecessary workbook).
**G8**: the announce line is the first assistant text content, before any
tool call that reads a source file's content (the one preceding tool call is
a bare `ls` folder listing).

### Result: no further loophole found after round 2

All four RED violations are closed, the round-1 loophole (headline missing
one file's inline citation) is closed and confirmed by re-run, and no new
loophole surfaced in round 2. No further REFACTOR needed.

---
