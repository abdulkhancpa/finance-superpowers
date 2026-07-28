---
name: skillify
description: use when a workflow just worked and will recur — end of a successful session, "we'll do this every month", or a process worth teaching to future sessions — to mint it as a named, tested skill.
---

# skillify

Announce at start: "Using skillify to mint <name> from this session."

<HARD-GATE>
the draft is grepped for every amount, date, entity name, invoice/batch/JE
number, and filename from the session that just ran, and each hit is
rewritten as a role or a check before the skill is shown as finished — and
the skill is not committed until tests/scenarios/<name>.md, a recorded
no-skill (RED) run, and a confirmed re-run (GREEN) all exist on disk, with
the GREEN confirmation checked against the run's actual tool-call order
(or a freshly reopened artifact) — never accepted from a narrative
document that merely asserts the order was correct.
</HARD-GATE>

1. extract the method, not the instance: generalize file names to roles
   ("the subledger export", not "ar_subledger_2026-06.csv") and this
   period's amounts to checks ("the statement must foot", not "must equal
   144,500"). anything period-specific that survives — an amount, a date,
   an entity name, an invoice/batch/JE number — is a bug; grep the draft
   for the session's actual figures and names before calling it done.
2. frontmatter is name + description only. the description states when
   to use the skill — triggering situations — never what it does or how
   (a process summary becomes a shortcut the agent takes instead of
   reading the body).
3. exactly one hard gate. find the single non-negotiable rule this verb
   exists to enforce and mark it, once, as `<HARD-GATE>` — not folded into
   ordinary numbered steps as advisory prose that reads no differently
   from the rest.
4. the body inherits the iron laws by reference; restate only the
   verb-specific gates. keep it short.
5. no skill ships untested: write tests/scenarios/<name>.md (the
   situation, the fixture files, the corners an agent would cut — a
   pattern to copy lives in tests/scenarios/ and sample-data/brightwater/),
   run it without the new skill and record the failures verbatim to
   tests/transcripts/<name>-red.md, then re-run with the skill and confirm
   each recorded failure closed. all three artifacts exist on disk before
   the skill is committed — a validation described only in a chat reply
   does not count. a narrative confirming closure is not itself evidence:
   re-open the run's own tool-call order (or the actual saved output) and
   check that the claimed sequence — threshold before values, footing
   before investigation, whatever the verb's gate requires — really
   happened in that order. a document that says "stated first" is not
   proof it was first.
6. name it lowercase-kebab, verb-first, specific enough to trigger.

## rationalizations

| excuse | reality |
|---|---|
| "keep this period's numbers/names in as an example" | a red-transcript agent's shipped skill kept a "Real-World Impact" section reading "First run (Brightwater, period 2026-06): subledger footed to $2,764,449.50 against a GL control balance of $2,619,949.50... Cedar Valley Co-op invoice... Stonebridge Market invoice keyed as $45,000.00, should be $54,000.00" — permanently frozen into general-purpose skill text. roles and checks, not instances. |
| "i tested it myself before shipping, that's enough" | the same agent's own closing report said "Stress-tested edge cases: a clean 3-line ledger... and a ledger with a genuinely unexplainable $123.45 variance..." — true, and yet a search over the whole sandbox for anything named like a test returned nothing. a validation that exists only as a sentence in a reply isn't reperformable; it has to be a file. |
| "the guidance already says not to plug / not to force a tie, that's gate enough" | the same skill's only guardrail — "do not force a tie... rather than plugging" — was ordinary numbered-step prose with zero `<HARD-GATE>` blocks anywhere in the file. a rule indistinguishable from the surrounding steps is one edit away from being softened out. mark the one non-negotiable rule, visibly, once. |
| "the description should explain the steps so the next agent knows what it does" | descriptions that summarize become shortcuts — the agent reads the description, thinks it knows the method, and never opens the body. state when, never how. |
| "my green transcript says the threshold was posted before any figures were read, so it was" | a green-run agent's own validation write-up read "This was written down... before any source file's values were computed for this run" — but its actual tool calls read all three source files and printed a raw total and a duplicate scan a dozen calls before the threshold text was ever written. document order is not chronology; check the tool-call sequence itself, not the write-up's claim about it. |
