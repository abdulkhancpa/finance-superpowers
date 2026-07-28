# finance-superpowers

Working discipline for finance and accounting professionals, as Claude Code skills.

## What this is

Claude already knows the accounting — GAAP, DCF math, consolidation mechanics, the debits and credits. What it doesn't reliably have, out of the box, is the working discipline of a strong controller: tie everything out, never plug a difference, state materiality before you look at the numbers, cite every figure back to its source, and verify before you say you're done. finance-superpowers is that discipline, encoded as ten Claude Code skills — nine verbs that cover the shape of financial work (understand, clean, transform, reconcile, analyze, document, review, brainstorm, skillify) plus a bootstrap skill that loads the iron laws on every session.

This is a methodology library, not a knowledge library — it teaches no accounting facts and adds no domain judgment. It is process discipline only: how to handle an export, how to prove a tie, how to disclose what you can't explain instead of quietly absorbing it. Every skill was pressure-tested before it shipped, using the same protocol throughout: run a realistic scenario without the skill, record verbatim how the agent cuts corners, write the minimal skill that closes exactly those failures, then confirm it holds. Nothing here talks to a live system — sources are exports the user already pulled, and the file contract (`sources/` → `work/` → `output/`) is the entire product. If you want live ERP or SharePoint wiring, that's a v2 conversation; this repo proves the workflow on files first.

## Install

This repo is a Claude Code plugin — `.claude-plugin/plugin.json` defines it, `.claude-plugin/marketplace.json` catalogs it as a single-plugin marketplace, and `skills/` holds the ten SKILL.md files, each following the open [agentskills.io](https://agentskills.io) standard.

To install locally:

1. Clone this repo.
2. Install the Python dependencies the two helper scripts need: `pip install -r requirements.txt` (this pulls in `openpyxl`, used by `scripts/write_workbook.py` to build deliverables, plus `pytest` for the test suite). Any Python that can run these scripts works — Claude Code invokes them via `${CLAUDE_PLUGIN_ROOT}`, not a bundled interpreter, so this install has to be on the machine running Claude Code.
3. In Claude Code, add it as a plugin marketplace source and install from it:
   ```
   /plugin marketplace add /path/to/finance-superpowers
   /plugin install finance-superpowers@finance-superpowers
   ```
   (or point `/plugin marketplace add` at this repo's git URL instead of a local path).
4. Start a session (or run `/reload-plugins` in one already open). The `using-finance-superpowers` skill loads automatically and announces itself; the other nine verbs trigger from their descriptions as your request matches — you don't invoke them by name.

This exact flow was verified end to end in this repo, not just checked against docs: `claude plugin marketplace add ./` (local scope) succeeded, `claude plugin install finance-superpowers@finance-superpowers` succeeded, and `claude plugin details finance-superpowers@finance-superpowers` confirmed version `1.0.0`, status enabled, and all ten skills (`analyze, brainstorm, clean, document, reconcile, review, skillify, transform, understand, using-finance-superpowers`) loaded — then both were removed again to leave the environment clean.

Because SKILL.md is a portable format, the `skills/` directory also works as a plain skills folder in any harness that supports the standard — the plugin manifest is a convenience, not a requirement.

## The working contract

Every engagement is a folder with a standard shape:

```
engagement/
  sources/   # the exports you pulled — read-only, never modified
  work/      # intermediates: tidy tables, matching files — CSV, diffable
  output/    # deliverables: formatted xlsx + workpaper.md
```

- If a skill needs an export you haven't pulled, it says exactly what to request (system, report, period, format) and waits — it never guesses or fabricates.
- Reruns are safe and expected: drop next month's export into `sources/`, run the same verb, get the same-shaped output.
- Sources are never edited in place. Anything that needs fixing gets copied into `work/` first.

**Output contract.** Every verb that produces a deliverable ends with two things:

1. A formatted xlsx workbook in `output/`, assembled through the one shared helper, `scripts/write_workbook.py` — a cover sheet (title, date, engagement, sources cited, assumptions), one sheet per schedule with frozen headers, accounting number formats (no floating-point garbage decimals), sensible column widths, and consistent header/total-row styling. Skills never hand-roll xlsx formatting.
2. A markdown workpaper (`workpaper.md`) narrating method, tie-outs, judgment calls, assumptions, and citations back to `sources/` — what makes the work reviewable and re-performable by someone who wasn't in the room.

Skills prepare tidy CSV intermediates in `work/` (diffable, rerun-verifiable) and call `write_workbook.py` to assemble the final deliverable — formatting bugs get fixed in one tested place, not in nine skills separately.

## The nine verbs

| Verb | The question it answers | Typical uses |
|---|---|---|
| brainstorm | What are we trying to find out, and what does done look like? | Scope, approach, thresholds — hard gate before data work |
| understand | What am I looking at? | Profile an export, map a data room, work out grain and what should tie to what |
| clean | Fix what's wrong without changing meaning | Merged cells, subtotal rows, duplicates, format junk → tidy tables |
| transform | Reshape what's right | CoA mapping, pivots, aggregation, FX translation, schedules |
| reconcile | Do these two things agree, and why not? | Bank recs, subledger-to-GL, intercompany, proof-of-cash |
| analyze | What drives this difference? | Flux/variance, bridges, driver decomposition — everything above threshold explained |
| document | Write it up audit-ready | Memos, position papers, workpaper narratives |
| review | Does someone else's work hold up? | Reperform, tie, challenge — a human's work or Claude's own |
| skillify | This worked — make it repeatable | Turn a successful session into a named, tested skill |

They chain naturally — brainstorm → understand → clean → transform → reconcile/analyze → document → review — but each stands alone. A tenth skill, `using-finance-superpowers`, isn't a verb: it's the discipline layer that loads on every session and carries the iron laws below.

## The iron laws

Loaded by `using-finance-superpowers` on every session, applying to every verb:

1. **Every number ties to a source.** Every figure in a deliverable cites its file (and sheet/range or row). No ungrounded numbers.
2. **No unexplained plugs.** A difference gets chased to root cause or explicitly disclosed with its size and suspected nature — never silently absorbed.
3. **State the threshold before analyzing.** Materiality/explanation thresholds are agreed up front, not chosen after seeing the results.
4. **No hardcodes.** Any value not traced to a source file (an FX rate, tax rate, growth assumption, threshold) is clearly marked as an assumption or input — surfaced in the workpaper's assumptions section, never buried in a formula or script.
5. **Sources are read-only.** Skills never modify an input file. All output goes to a separate folder.
6. **Verify before "done."** Re-foot, re-tie control totals, confirm outputs open cleanly — evidence before claiming completion.
7. **Show the plan before the work.** A short summary of what's about to be produced, then produce it.

## Sample data

Three scenarios, one fictional company — **Brightwater Distribution Co.**, a small multi-entity US/Canada distributor being acquired — chained into a single consistent story, under `sample-data/brightwater/`:

- **`trial-balance/`** — a ragged consolidated TB export (merged title row, section headers mixed into the data, double-counting subtotal rows, a duplicate account row, a text-typed amount, a grand-total row). Exercises understand / clean / transform.
- **`subledger-tie/`** — an AR subledger and GL that differ by exactly **$144,500.00**: the GL control balance is $2,619,949.50, the subledger foots to $2,764,449.50. The planted causes are a duplicate batch ($118,500.00), a June invoice posted to the GL in July ($35,000.00), and a $9,000.00 keying transposition in the GL — one of which (the transposition) is deliberately hard to isolate from the data alone, so the reconcile/analyze skills have to disclose it as a genuine open item rather than force a clean explanation. Exercises reconcile / analyze.
- **`data-room/`** — a small diligence data room, 18 files across financials, contracts (2 files), debt, HR, legal, and tax, with planted findings (a revenue reclass footnoted in the FY2025 notes, a change-of-control clause in a customer contract, an unaccrued litigation contingency). Exercises understand-at-scale / document / review.

Every mess is planted deliberately to trigger the specific failure its verb's RED test has to catch. All of it is small enough to hand-verify (hundreds of rows, not thousands) and entirely synthetic — see the "no real data" statement below.

Regenerate any of it with the scripts in `tests/generators/` (`gen_trial_balance.py`, `gen_subledger.py`, `gen_data_room.py`); `sample-data/brightwater/README.md` documents the planted story in one place.

## How the skills were tested

Each skill went through the same RED/GREEN/REFACTOR loop before it shipped:

- **RED** — run a realistic scenario on the Brightwater fixtures *without* the skill; record verbatim how the agent cuts corners (plugs a difference, invents a number, edits a source file, skips verification, states a threshold after already having seen the numbers).
- **GREEN** — write the minimal skill that closes exactly those recorded failures; re-run; confirm the failures are gone.
- **REFACTOR** — look for the next loophole the agent finds; close it explicitly; re-test.

The recorded RED transcripts live in `tests/transcripts/` (one per skill, e.g. `reconcile-red.md`), and the scenarios that produced them are in `tests/scenarios/`. These transcripts are also the source material for each skill's rationalization table — every "excuse → reality" row quotes an agent's own recorded words back at it, not a hypothetical.

On top of the per-skill tests, `tests/e2e/` holds a full mini-engagement on Brightwater that chains **brainstorm → understand → clean → reconcile → analyze → document**, then an independent **review** pass over the result — a deal-lead prompt covering data-room review, an AR tie, a revenue bridge, and a findings memo — checked against the ground truth planted in the fixtures. `transform` was exercised in a lighter form folded into `analyze`'s aggregation step rather than as its own pass, since this engagement had no CoA/FX remapping to do; `skillify` isn't part of an engagement run at all — it mints new skills from a session afterward, so it has no place in this one. The committed reference output is under `tests/e2e/output/engagement/`: a real `sources/` → `work/` → `output/` folder a reviewer who has never seen Claude could open and re-perform, with `output/workpaper.md` and `output/review.md` as the audit trail. `tests/e2e/mini-engagement.md` narrates the run, including what the RED (no-skills) pass missed.

Two shared helper scripts back the skills and are themselves unit-tested (`tests/test_write_workbook.py`, `tests/test_profile_table.py`): `scripts/write_workbook.py` (the xlsx formatting bar every deliverable goes through) and `scripts/profile_table.py` (the tidy-table profiler used by understand and clean).

## Roadmap

- **v1 (this release):** nine verb skills + the discipline layer + the Brightwater sample datasets + the two helper scripts, each pressure-tested individually and together.
- **v2:** department playbooks as thin compositions of verbs — no new domain knowledge, just sequencing and judgment about what to look for. First: M&A financial diligence (understand the data room → clean → reconcile proof-of-cash → analyze quality of earnings → document findings). Then close-cycle and FP&A packs.
- **Out of scope indefinitely:** live-system connections (MCP to an ERP, SharePoint, or email), real company data anywhere in this repo, and oversight/management-layer workflows — this library is for the person doing the work, not the person reviewing it from above.

## No real data

This repo contains no real personal or company data, anywhere, at any point in its history that ships. `sample-data/brightwater/` is entirely synthetic — a fictional company, generated figures, invented names — built specifically to exercise these skills' failure modes without touching anything real. If you use finance-superpowers on your own engagements, your `sources/`, `work/`, and `output/` folders stay on your machine; nothing here transmits or retains what you feed it.
