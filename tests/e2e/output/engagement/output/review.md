# Independent Review — Brightwater Distribution Co. Initial Financial Diligence

**Reviewed:** `engagement/output/workpaper.md`, `engagement/output/deal_memo.md`, `engagement/output/ar_gl_reconciliation.xlsx`, `engagement/output/revenue_bridge_fy2025.xlsx`
**Reperformed against:** `engagement/sources/trial-balance/`, `engagement/sources/subledger-tie/`, `engagement/sources/data-room/` (read directly, independently of `engagement/work/`)
**Method:** every cited filename checked against the literal `sources/` listing; every numeric claim recomputed from source files with Python/openpyxl/csv/sha256sum; both xlsx deliverables reopened fresh and every cell read.

## Citation literalism

All file paths cited in the workpaper and memo (18 data-room files, 3 subledger-tie files, 1 trial-balance file) were checked against the actual `find engagement/sources -type f` listing. **Every citation matches an actual file.** No fabricated filenames found.

## Verdict table

| # | Claim | Work's number | My recomputation | Verdict |
|---|---|---|---|---|
| 1 | AR subledger raw control total, 212 rows | 2,764,449.50 | 2,764,449.50 | **PASS** |
| 2 | 5 exact-duplicate rows, batch b-0621, sum removed | inv-20310/11/12/13/14, $118,500.00 | Identical 5 rows identified independently (full-key duplicate scan), sum $118,500.00 | **PASS** |
| 3 | Tidy AR total | 2,645,949.50 | 2,645,949.50 (raw − dupes, re-footed from 207-row tidy population) | **PASS** |
| 4 | GL account 1200 ending balance, 2026-06 | 2,619,949.50 | 2,619,949.50 (`gl_summary_2026-06.csv`) | **PASS** |
| 5 | Raw AR-vs-GL gap | 26,000.00 | 2,645,949.50 − 2,619,949.50 = 26,000.00 | **PASS** |
| 6 | Timing item: JE-7-0043, inv-20241, Cedar Valley Co-op, $35,000, posted 2026-07-02 | as stated | Confirmed verbatim in `gl_je_detail_2026-07.csv` | **PASS** |
| 7 | Residual after timing | −9,000.00 | 2,645,949.50 − 35,000.00 = 2,610,949.50; 2,619,949.50 − 2,610,949.50 = 9,000.00 | **PASS** |
| 8 | Transposition: inv-19877 Stonebridge Market, 45,000.00 → 54,000.00, closes residual | claimed sole candidate among irregular invoices | Confirmed arithmetically: +9,000 closes the gap exactly, correct direction. **However**, a full-population digit-swap scan (not just the "irregular" subset) turns up **35** rows in the systematic inv-195xx–197xx sequence that also produce an exact ±9,000 swap — a mechanical artifact of that sequence's formulaic amounts, not evidence of real errors. The work's claim of "only candidate" is accurate **only within the manually-keyed subset it deliberately searched** (disclosed as a narrowing decision, not a blind scan) — it is not literally the only $9,000 digit-swap in the file. The work's own caveat ("not independently confirmed by a third source... open item") already carries the appropriate weight here. | **PASS**, with a precision note — see Q&A below |
| 9 | Rejected candidate: inv-20314 (10,000→1,000), wrong direction, would widen gap to 18,000 | as stated | Confirmed: 2,610,949.50 − 9,000.00 = 2,601,949.50; 2,619,949.50 − 2,601,949.50 = 18,000.00 | **PASS** |
| 10 | Reconciliation foots to zero | 2,645,949.50 − 35,000 + 9,000 = 2,619,949.50 = GL | Re-added independently, matches exactly | **PASS** |
| 11 | TB hazard: US "prepaid expenses" (1400) stored as text `"77,614.00"` | as stated | Confirmed — `type=str` on load | **PASS** |
| 12 | TB hazard: Canada "salaries and wages" (5210) duplicated verbatim, 58,349.10 twice | as stated | Confirmed, rows 56 & 57 both 58,349.10 | **PASS** |
| 13 | TB hazard: merged title range A1:E2 | as stated | Confirmed via `ws.merged_cells.ranges` | **PASS** |
| 14 | Consolidated TB acct 1200 by entity: US 814,812 + Canada 827,519 + Holdco 840,226 | 2,482,557 | 2,482,557 at time of this run; TB regenerated in v1.1 for economic plausibility — current fixture: US 3,050,000 + Canada 780,000, Holdco has no AR = 3,830,000 | **PASS** (as of this run; see v1.1 note) |
| 15 | TB-vs-subledger-tie AR population gap (flagged, not chased) | 137,392.50 | 2,619,949.50 − 2,482,557 = 137,392.50 at time of this run; current fixture: 3,830,000 − 2,619,949.50 = 1,210,050.50 | **PASS** (as of this run; see v1.1 note) |
| 16 | tb_extract account-code trap sum (all 3 entities) | 34,530 | 4000+4100+5000+5100+5210+5220+5900 = 34,530 in all three files | **PASS** |
| 17 | tb_extract expense accounts identical across entities | 5000/5100/5210/5220/5900 identical US/CA/Holdco | Confirmed identical in all 3 files at time of this run; confirmed to be a generator bug (`gen_data_room.py`'s `EXPENSE_ROWS` shared across entities) and **fixed in v1.1** — extracts are now entity-specific | **PASS** (as of this run; bug since fixed) |
| 18 | ar_aging bucket sum | 4,610,000 | 2,690,000+1,180,000+540,000+260,000+120,000−180,000 = 4,610,000 | **PASS** |
| 19 | ar_aging total ties to balance sheet net AR | 4,610,000 = 4,610,000 | Confirmed | **PASS** |
| 20 | monthly_revenue_2025 sum | 49,200,000 | Confirmed | **PASS** |
| 21 | tb_extract combined 4000+4100, 3 entities | 49,200,000 (US 36,900,000 + CA 12,050,000 + Holdco 250,000) | Confirmed exactly | **PASS** |
| 22 | Gap: gross tie vs reported revenue | 250,000 | 49,200,000 − 48,950,000 = 250,000; matches notes_fy2025.md freight-reclass amount exactly | **PASS** |
| 23 | Term loan balance ties to balance sheet & amortization | 4,800,000; first payment balance 4,650,000 = 4,800,000−150,000 | Confirmed in `term_loan_agreement.md`, `balance_sheet_fy2025.md`, `amortization_schedule.csv` | **PASS** |
| 24 | Bonus accrual = 8% × (EBITDA − 3,000,000) | 44,800 = 8%×560,000 | 8%×(3,560,000−3,000,000)=44,800, ties to `bonus_plan.md` | **PASS** |
| 25 | Holdco tb_extract product revenue vs later TB Holdco TOTAL REVENUE | 250,000 vs 0 | Confirmed both figures; coincidence flagged, correctly not resolved | **PASS** |
| 26 | Revenue bridge foots | 44,120,000+5,080,000−250,000=48,950,000 | Confirmed exactly | **PASS** |
| 27 | Lakeside driver ≈6% of FY2025 revenue | 2,937,000 | 0.06×48,950,000=2,937,000 exactly | **PASS** |
| 28 | Unattributed growth remainder | 2,143,000 | 5,080,000−2,937,000=2,143,000; correctly disclosed as open item, not silently dropped | **PASS** |
| 29 | Litigation: Carter Mechanical, probable, $400k–$600k, unaccrued | as stated | Confirmed verbatim in `pending_litigation.md` and `balance_sheet_fy2025.md` | **PASS** |
| 30 | Northern Foods ~22% revenue, change-of-control clause §11.2 | as stated | Confirmed verbatim, including section number | **PASS** |
| 31 | Lakeside freely assignable (contrast) | as stated | Confirmed verbatim | **PASS** |
| 32 | CEO 18-month change-of-control severance, unquantified | as stated | Confirmed in `bonus_plan.md` | **PASS** |
| 33 | Tax: no open audits, FY2025 on extension | as stated | Confirmed in `tax_summary.md` | **PASS** |
| 34 | Sources never modified | claimed | Recomputed SHA-256 of every file in `sources/`, matches pre-existing `sources.sha256.pre.txt` manifest exactly | **PASS** |
| 35 | Both xlsx deliverables open cleanly, cover sheet w/ sources+assumptions, figures foot to workpaper | claimed | Reopened both fresh with openpyxl; cover/cleaning_log/reconciliation and cover/gross_tie/revenue_bridge sheets all present; no stray formula/None cells found; every figure ties to workpaper exactly | **PASS** |
| 36 | Threshold stated before any figure computed | $5,000 / $250,000, run-log seq 5 | Confirmed thresholds stated at seq 5 — **but** see discipline finding below | **PASS (with caveat)** |

## Discipline checks (per skill step 5)

- **Threshold stated up front:** Yes — $5,000 (AR) and $250,000 (revenue/data-room) explicitly stated in workpaper §0/§1 and deal memo, both sections headers.
- **Assumptions declared:** Yes — 6 explicit assumptions in workpaper §6, a consistent subset of 4 repeated in the memo. All read as genuine judgment calls (duplicate interpretation, transposition hypothesis, FY2024 basis, Lakeside approximation), not numbers smuggled in as "assumptions."
- **Plugs disclosed as such:** Yes — the $2,143,000 revenue residual is explicitly labeled "not a bridge remainder, a labeled open item" rather than folded into "other" silently, exactly per the threshold-driven disclosure rule.
- **Open items disclosed with mechanism, not just size:** Yes, for all 8 open items — each carries a "suspected nature" and a "what would close it" column, not just a dollar amount.
- **Verification section present:** Yes, workpaper §8, and its claims (re-footing, reopening workbooks, sha256 check) were independently confirmed true by me, not merely asserted.

### Chronology / sequencing finding (run-log.jsonl)

Per the requested check: **a source file was read for content before the threshold was posted.** The run-log shows `seq 3` = `source_file_first_read` on `data-room/index_readme.md`, occurring before `seq 4` (brainstorm announce) and `seq 5` (threshold stated). The file read is a one-paragraph folder manifest with no dollar figures, but it does contain one substantive fact — "monthly tb extracts are per-entity, gross presentation" — that is directly relevant to the gross-vs-net presentation assumption later used in the revenue bridge (workpaper assumption #4, §6). This is **not concealed**: the preparer logged it honestly at the time (seq 3) and separately disclosed it in workpaper §8 ("Disclosed sequencing note"). It is a minor, self-reported, low-materiality deviation from strict "threshold before any source content" sequencing — reported here as instructed, not treated as invalidating any downstream figure (nothing dollar-denominated was read at that point).

## Overall conclusion

This is a high-fidelity piece of work. Every citation checked against the actual `sources/` file listing is genuine — no fabricated filenames. Every one of the ~35 numeric claims traced to source independently recomputes to the penny, including the two multi-entity gross-ties (revenue and AR), the AR-to-GL bridge, the litigation/customer-concentration/severance red flags, and both xlsx deliverables' internal footing. The AR reconciliation's residual was correctly and fully chased through duplicates → timing → transposition before being called closed, and the revenue bridge's unattributed remainder was correctly flagged as an open item rather than laundered into "other." Sources were verifiably left untouched (SHA-256 match). The one process finding — source content read one step before the formal threshold post — is minor, self-disclosed, and involves no dollar figures.

**Recommendation:** This work is reliable and can be relied on as delivered, subject to the open items it already lists (most materially: unconfirmed Stonebridge transposition, unattributed $2,143,000 revenue growth, unrecorded litigation contingency, and the Northern Foods change-of-control consent risk) — none of which are review failures, since all are correctly identified and flagged, not glossed over.

## Direct answers to reviewer's specific questions

- **Duplicate batch identified correctly?** Yes — 5 exact-duplicate rows (inv-20310, -20311, -20312, -20313, -20314), all batch `b-0621`, sum $118,500.00, independently confirmed via full-row-key duplicate scan.
- **Timing item identified correctly?** Yes — inv-20241, Cedar Valley Co-op, $35,000.00, JE-7-0043 dated 2026-07-02 (`gl_je_detail_2026-07.csv`), confirmed against the subledger's June-dated row for the same invoice.
- **Transposition error identified correctly, with invoice number/amounts?** The claimed transposition is inv-19877, Stonebridge Market: the subledger records (and believes correct) $45,000.00; the GL is consistent with this invoice contributing the transposed $54,000.00 (swap of the digits in the ten-thousands/thousands place).
- **Does independent recomputation confirm or refute this?** **Confirms the arithmetic**: the $9,000 residual (after duplicates and timing are removed) is closed exactly, in the required direction, by this swap. It does **not** independently confirm that the subledger's $45,000.00 is the *true* amount (and the GL's $54,000.00 the transposition error) — no third source (invoice, sales order) exists in the data room to prove it, exactly as the workpaper itself discloses. My own independent, full-population digit-swap test also found 35 other rows that mathematically produce an exact $9,000 swap — all of them in the synthetic, formulaic invoice sequence (inv-195xx–197xx) and thus implausible as real transposition candidates — which reinforces rather than undermines the work's decision to restrict its search to the manually-keyed/irregular invoices, and reinforces its own caveat that the divisibility-by-9 test is "a hint, not proof."
