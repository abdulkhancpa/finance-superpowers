# finance-superpowers — Design

Date: 2026-07-27
Status: Approved. Ready for implementation planning.
Relationship to any personal system: none. Standalone product. Must never contain real personal or company data — only method and synthetic fixtures.

## 1. Product summary

A standalone skills library in Claude Code plugin format (portable — SKILL.md is an open standard, agentskills.io) for finance and accounting professionals, analyst through director, doing the work rather than overseeing it, with an M&A financial-diligence and integration angle.

The thesis, taken from obra/superpowers: the model already knows the accounting (GAAP, DCF math, consolidation mechanics). What it lacks is the working habits of a strong controller — tie everything out, never plug a difference, state materiality up front, cite every number, verify before releasing. finance-superpowers encodes those habits as nine verb skills plus a discipline layer, each individually pressure-tested before it ships.

**Name:** `finance-superpowers` — the repo name, the plugin name, and the skill prefix (`finance-superpowers:reconcile`).

## 2. Design principles (from superpowers research)

- **Methodology, not knowledge library.** Zero domain-knowledge skills. All value is process discipline; the model supplies the accounting facts.
- **Small and tested beats large and plausible.** Nine excellent skills, each pressure-tested, over dozens of plausible ones.
- **Descriptions state when to use a skill, never what it does.** A description that summarizes the process becomes a shortcut the agent takes instead of reading the body.
- **Discipline skills carry rationalization tables** — two-column "excuse → rebuttal" tables built from real failure transcripts — plus hard gates and one-line iron laws for rules that must never bend.
- **The meta-skill (skillify) makes the library compound.** Without it the library is static.
- **Design around the known critiques:** token cost, overkill on trivial tasks, rigidity in exploratory work. Skills stay short; the brainstorm gate scales down for small jobs.

## 3. The discipline layer (iron laws)

A thin bootstrap skill (`using-finance-superpowers`) loads on every session, carrying rules that apply to every verb:

1. **Every number ties to a source.** Every figure in a deliverable cites its file (and sheet/range or row). No ungrounded numbers.
2. **No unexplained plugs.** A difference gets chased to root cause or explicitly disclosed with its size and suspected nature — never silently absorbed.
3. **State the threshold before analyzing.** Materiality/explanation thresholds are agreed up front, not chosen after seeing the results.
4. **No hardcodes.** Any value not traced to a source file (an FX rate, tax rate, growth assumption, threshold) is clearly marked as an assumption or input — surfaced in the workpaper's assumptions section, never buried in a formula or script.
5. **Sources are read-only.** Skills never modify an input file. All output goes to a separate folder.
6. **Verify before "done."** Re-foot, re-tie control totals, confirm outputs open cleanly — evidence before claiming completion.
7. **Show the plan before the work.** A short summary of what's about to be produced, then produce it.

## 4. The nine verbs

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

Boundary notes keeping the set MECE:

- **clean** repairs (wrong structure, junk, duplicates) without changing meaning; **transform** reshapes correct data (mapping, pivoting, aggregating). One repairs, one reshapes.
- Anomaly investigation is not a verb; it is discipline inside **reconcile** and **analyze**: root cause or disclose, never plug.
- Schedule-building (rollforwards, bridges, amortization) is **transform** + **document**.
- Document-pile work (data rooms, contract stacks) is **understand** applied to many files — the M&A workhorse in v1.

Verbs chain naturally (brainstorm → understand → clean → transform → reconcile/analyze → document → review) but each stands alone.

### The brainstorm gate scales to the job

One brainstorm skill with a built-in sizing step. It always runs, but:

- **Small jobs** ("re-foot this schedule") collapse to a three-line confirmation — *what I'll produce, from which sources, at what threshold* — approved in one user reply.
- **The full scoping dialogue** triggers only when the work is multi-step or the threshold is genuinely unclear.
- The skill body carries a rationalization-table entry for "this task is too small even for the three-liner."

One skill, no mode-selection ambiguity.

## 5. The working contract

Every engagement is a folder with a standard shape:

```
engagement/
  sources/   # the exports the user pulled — read-only, never modified
  work/      # intermediates (tidy tables, matching files) — CSV, diffable
  output/    # deliverables: formatted xlsx + workpaper.md
```

- A skill that needs an export the user hasn't pulled says exactly what to request (system, report, period, format), then waits — it does not guess or fabricate.
- Reruns are safe and expected: drop next month's export in, run the same verb, get the same-shaped output.
- No live-system integration in scope. Users graduate proven workflows to live wiring themselves. The file contract is the product.

### Output contract

Every verb that produces a deliverable ends with:

1. **A formatted xlsx workbook** in `output/` — professional, readable, audit-ready, for consumers who will never see Claude.
2. **A markdown workpaper** (`workpaper.md`) narrating method, tie-outs, judgment calls, assumptions, and citations back to `sources/`. The workpaper is what makes the work reviewable and re-performable.

**Excel mechanics:** all workbooks are produced through one shared helper, `scripts/write_workbook.py` (openpyxl), which owns the formatting bar:

- Cover sheet: title, date, engagement, sources cited, assumptions section.
- One sheet per schedule; frozen header rows.
- Proper number formats — accounting format for money, no floating-point garbage decimals.
- Sensible column widths; consistent header and total-row styling.

Skills never hand-roll xlsx formatting; they prepare tidy CSV intermediates in `work/` (diffable, rerun-verifiable) and call the helper to assemble the deliverable. Formatting bugs get fixed in one tested place, not nine skills.

## 6. Skill anatomy and conventions

- SKILL.md frontmatter: `name` + `description` only; the description states **when** to use the skill (triggering situations), never what it does or how.
- Bodies stay short; heavy reference material splits into supporting files the agent loads on demand. No `@file` force-loads.
- Discipline-critical skills carry rationalization tables built from real failure transcripts, a hard gate for the single most safety-critical rule, and an "announce at start" line ("Using reconcile to …") so skill use is visible to the human.
- Skills may ship small deterministic helper scripts; instructions are the default, code the exception. v1 ships two: `write_workbook.py` (xlsx assembly) and `profile_table.py` (tidy-table profiler used by understand/clean).
- Lowercase, tidy naming throughout.

## 7. Repository structure

```
finance-superpowers/
  .claude-plugin/plugin.json
  skills/
    using-finance-superpowers/   # discipline layer, loads every session
    brainstorm/
    understand/
    clean/
    transform/
    reconcile/
    analyze/
    document/
    review/
    skillify/
  scripts/
    write_workbook.py            # shared xlsx writer — the formatting bar
    profile_table.py             # tidy-table profiler
  sample-data/
    <company>/
      trial-balance/
      subledger-tie/
      data-room/
  tests/                         # RED/GREEN scenario scripts + recorded failure transcripts
  README.md
```

## 8. Sample data

Three scenarios built around **one fictional company** — a small multi-entity distributor being acquired, which naturally motivates all three — with a consistent story so the scenarios chain into an end-to-end mini-engagement:

1. **Ragged trial balance export** — merged headers, subtotal rows, format junk. Exercises understand / clean / transform.
2. **Subledger that doesn't tie to the GL** — planted differences: a duplicate batch, a timing item, a true error. Exercises reconcile / analyze.
3. **Small M&A data room** (~15–25 files: statements, contracts, TB extracts). Exercises understand-at-scale / document / review.

Rules:

- Every mess is planted deliberately to trigger the specific failure its verb's RED test must catch (a plug-sized difference, a duplicate batch, a merged-cell header).
- Small enough to hand-verify: hundreds of rows, not thousands.
- Entirely synthetic. Nothing derived from real personal or company data.
- The datasets double as demos and as the fixture set for skillify's own instructions.

## 9. Testing — TDD for skills

Each verb is validated before it ships:

- **RED:** run a realistic scenario on sample data *without* the skill; record verbatim how the agent cuts corners (plugs a difference, invents a number, modifies a source, skips verification).
- **GREEN:** write the minimal skill closing exactly those recorded failures; re-run; confirm compliance.
- **REFACTOR:** find new loopholes the agent invents; close them explicitly; re-test.

Recorded failure transcripts live in `tests/` and feed the rationalization tables.

## 10. Roadmap

- **v1:** nine verbs + discipline layer + sample datasets + the two helper scripts.
- **v2:** department playbooks as thin compositions of verbs. First: M&A financial diligence (understand the data room → clean → reconcile proof-of-cash → analyze quality of earnings → document findings). Then close-cycle and FP&A packs. Playbooks add domain judgment (what to look for) on top of verbs (how to work).
- **Out of scope indefinitely:** live-system connections (MCP to ERP/SharePoint/email), real company data in the repo, oversight/management-layer workflows.

## 11. Success criteria (v1 done when)

1. Each verb passes its RED/GREEN pressure test on the sample data.
2. A full mini-engagement runs brainstorm → review end-to-end on the sample company, producing a workpaper folder a reviewer who has never seen Claude could follow and re-perform.
3. Every deliverable produced in that engagement is a formatted xlsx meeting the `write_workbook.py` bar, with an accompanying workpaper whose every number cites a source.
4. Nothing in the repo contains real personal or company data.
5. skillify, run on a real workflow, produces a new skill that passes its own test.
