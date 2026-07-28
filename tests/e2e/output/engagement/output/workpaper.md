# Brightwater Distribution Co. — Initial Financial Diligence Workpaper

## 0. Scope (agreed, per brainstorm)

- **Produce:** (1) AR subledger-to-GL reconciliation, (2) FY2025 revenue bridge/explanation, (3) data-room findings memo — plus intermediate tidy tables and a data-room tie-point map.
- **From:** `trial-balance/tb_2026-06.xlsx`; `subledger-tie/ar_subledger_2026-06.csv`, `gl_summary_2026-06.csv`, `gl_je_detail_2026-07.csv`; `data-room/*` (18 files).
- **Thresholds (agreed before any figure computed):**
  - AR subledger-to-GL reconciliation: **$5,000**
  - Revenue bridge and data-room findings: **$250,000**
- **Verb chain:** understand → clean → transform → reconcile → analyze → document.

## 1. Threshold

Restated: $5,000 for the AR subledger-to-GL tie; $250,000 for the FY2025 revenue movement explanation and for data-room findings. Both agreed with the deal lead before any source file's values were read (see `engagement/work/run-log.jsonl`, seq 5).

---

## 2. Understand — inventory, grain, hazards, tie-point map

### 2a. Data room inventory — 18 files, none skipped

| # | Path | Type | Content ID |
|---|---|---|---|
| 1 | data-room/index_readme.md | md | Folder manifest (seller's banker note) |
| 2 | data-room/contracts/northern_foods_msa.md | md | Master supply agreement, Northern Foods Inc. |
| 3 | data-room/contracts/lakeside_grocers_agreement.md | md | Supply agreement, Lakeside Grocers LLC |
| 4 | data-room/debt/term_loan_agreement.md | md | Term loan agreement, First Cascade Bank |
| 5 | data-room/debt/amortization_schedule.csv | csv | Quarterly principal/interest schedule, 8 rows |
| 6 | data-room/financials/income_statement_fy2025.md | md | FY2025/FY2024 income statement (unaudited) |
| 7 | data-room/financials/balance_sheet_fy2025.md | md | Balance sheet as of 2025-12-31 (unaudited) |
| 8 | data-room/financials/notes_fy2025.md | md | Management notes to FY2025 financials |
| 9 | data-room/financials/monthly_revenue_2025.csv | csv | 12 months gross revenue, FY2025 |
| 10 | data-room/financials/ar_aging_2025-12.csv | csv | AR aging buckets as of 2025-12 |
| 11 | data-room/financials/tb_extract_us_fy2025.csv | csv | US entity TB extract, FY2025, 7 accounts |
| 12 | data-room/financials/tb_extract_canada_fy2025.csv | csv | Canada entity TB extract, FY2025, 7 accounts |
| 13 | data-room/financials/tb_extract_holdco_fy2025.csv | csv | Holdco entity TB extract, FY2025, 7 accounts |
| 14 | data-room/hr/headcount.csv | csv | FTE by department, FY2024 vs FY2025 |
| 15 | data-room/hr/bonus_plan.md | md | Management bonus plan terms |
| 16 | data-room/legal/cap_table.csv | csv | Cap table (3 holders) |
| 17 | data-room/legal/pending_litigation.md | md | Outside counsel litigation summary |
| 18 | data-room/tax/tax_summary.md | md | Tax position summary |

Plus, outside the data-room folder: `trial-balance/tb_2026-06.xlsx` (consolidated TB, 3 entities, 2026-06-30) and `subledger-tie/{ar_subledger_2026-06.csv, gl_summary_2026-06.csv, gl_je_detail_2026-07.csv}` (AR-to-GL tie file family).

### 2b. Grain and structural hazards (profiled with `profile_table.py`)

- **ar_subledger_2026-06.csv**: grain = one open AR invoice line. 212 rows. Hazard: 5 exact-duplicate rows (invoice+customer+date+amount+batch identical) — batch `b-0621` posted twice. `batch` column blank for 202/212 rows (only the 5 manually-keyed b-0621 lines and their dupes are populated) — not a hazard, just sparse.
- **gl_summary_2026-06.csv**: grain = one control-account balance line (account 1200, period 2026-06). 1 row. No hazards.
- **gl_je_detail_2026-07.csv**: grain = one JE line. 1 row (JE-7-0043, posts inv-20241 to account 1200). No hazards.
- **trial-balance/tb_2026-06.xlsx**: grain = one account balance per entity, 3 entity blocks (US/Canada/Holdco) in one sheet. Hazards: (1) merged title range A1:E2; (2) US row "prepaid expenses" (acct 1400) is **text**-typed `"77,614.00"`, not numeric — a naive sum of column E would silently skip or mis-sum it; (3) Canada "salaries and wages" (acct 5210) row is **duplicated verbatim** (58,349.10 appears twice); (4) `TOTAL ASSETS/LIABILITIES/EQUITY/REVENUE/EXPENSES` caption rows share column E with their own already-counted detail rows — naive `SUM(E:E)` over the whole sheet double-counts every subtotal (nonsense sum if attempted: summing all of column E gives a meaningless blended figure mixing details and their own subtotals, not shown here because no one should compute it this way). This file was profiled for context; it was **not** used as an input to either the AR reconciliation or the revenue bridge (see 2c).
- **data-room/financials/tb_extract_us/canada/holdco_fy2025.csv**: grain = one account balance per entity, FY2025. Hazard: the `account` column (4000, 4100, 5000, 5100, 5210, 5220, 5900) is numeric-typed and **sums to 34,530 in all three files** — a textbook trap sum (account codes, not dollars; meaningless if totaled). Separately, the five expense-account balances (5000, 5100, 5210, 5220, 5900) were **identical in dollar amount across all three entities** despite US/Canada/Holdco having very different revenue scale ($36.9M / $12.05M / $0.25M) — flagged as a data-quality red flag in the findings memo, not resolved here (no independent source to confirm which entity's figures, if any, are correct). *[v1.1 note: confirmed to be a generator bug (`gen_data_room.py`'s `EXPENSE_ROWS` list was shared across all three entities) — fixed; each entity now has its own expense rows, consolidating to the income statement's cogs/opex/interest.]*
- **data-room/financials/ar_aging_2025-12.csv**: grain = one aging bucket. 6 rows, no hazards. Buckets sum (2,690,000+1,180,000+540,000+260,000+120,000−180,000 allowance) = **4,610,000**.
- **data-room/financials/monthly_revenue_2025.csv**: grain = one month. 12 rows, no hazards. Sum = **49,200,000**.
- All other data-room files (contracts, debt, legal, tax, hr, index readme) are narrative/short tables with no structural hazards.

### 2c. Tie-point map (mapped, not yet judged — computation lives in sections 3–4)

| A | B | Status |
|---|---|---|
| `ar_aging_2025-12.csv` bucket total (4,610,000) | `balance_sheet_fy2025.md` "accounts receivable, net" (4,610,000) | **Ties exactly** — computed and confirmed in section 3 as a corroborating data-room check (not the AR-to-GL deliverable itself, which uses the subledger-tie family below). |
| `ar_subledger_2026-06.csv` control total (tidy) | `gl_summary_2026-06.csv` ending_balance | Mapped as the engagement's AR-to-GL tie; both sides cited, difference computed and explained in section 4 (reconcile). |
| `trial-balance/tb_2026-06.xlsx` acct 1200 (US 3,050,000 + Canada 780,000; Holdco carries no AR — no operations — = 3,830,000) | `gl_summary_2026-06.csv` ending_balance (2,619,949.50) | **Flagged, not chased.** Same stated period (2026-06) but different populations/amounts; neither the TB nor its per-entity split reconciles to the subledger-tie GL figure. **Open question** for the seller: is `gl_summary_2026-06.csv` a sub-population (e.g., one entity or one AR sub-account) of the consolidated TB AR, or a wholly separate ledger extract? Out of scope for the AR reconciliation as defined (that deliverable is explicitly the subledger-tie file family), but worth a follow-up data request before relying on the TB's AR figure. *[v1.1 note: the TB fixture was regenerated for economic plausibility after this run; the AR figures above reflect the current fixture. The open scope question is unchanged and is not a same-company question — the TB and the data room represent the same company.]* |
| `monthly_revenue_2025.csv` total (49,200,000) | `tb_extract_us/canada/holdco_fy2025.csv` combined accounts 4000+4100 (49,200,000) | **Ties exactly** — computed in section 5 (analyze). |
| `monthly_revenue_2025.csv` / TB-extract gross total (49,200,000) | `income_statement_fy2025.md` reported FY2025 revenue (48,950,000) | **Gap of exactly 250,000**, explained by the freight-reclass disclosure in `notes_fy2025.md` — computed in section 5. |
| `term_loan_agreement.md` balance at 2025-12-31 (4,800,000) | `balance_sheet_fy2025.md` "term loan" (4,800,000); `amortization_schedule.csv` first payment row (2026-03-31, balance after payment 4,650,000 = 4,800,000 − 150,000) | **Ties exactly** — corroborating check, not a deliverable in itself. |
| `bonus_plan.md` FY2025 accrual (44,800) | 8% × (EBITDA 3,560,000 − 3,000,000) per `income_statement_fy2025.md` = 8% × 560,000 = 44,800 | **Ties exactly** — corroborating check. |
| `data-room/financials/tb_extract_holdco_fy2025.csv` acct 4000 "product revenue" (250,000) | `trial-balance/tb_2026-06.xlsx` Holdco TOTAL REVENUE for 2026-06 (0) | **Flagged observation, not chased.** Holdco is shown as having zero revenue capacity in the later (2026-06) consolidated TB, yet its FY2025 TB extract records exactly $250,000 of "product revenue" — the same dollar amount as the freight-reclass disclosed in the notes. Possible coincidence or possible misclassification; not resolvable from sources in hand. Carried as an open item in section 6. |

## 3. Clean — ar_subledger_2026-06.csv

- **Raw control total** (naive sum of `open_amount`, all 212 rows, before any row touched): **2,764,449.50**.
- **Removed**: 5 exact-duplicate rows — invoice/customer/date/amount/batch identical to an earlier row in the same file, all under batch `b-0621`: inv-20310 (41,250.00), inv-20311 (18,775.00), inv-20312 (26,400.00), inv-20313 (22,075.00), inv-20314 (10,000.00). Each is judged a single posting entered twice (not two real invoices) because every field, including the invoice number itself, is identical — an invoice number cannot legitimately repeat for two distinct transactions. Removed sum: **118,500.00**.
- **Verification equation**: 2,764,449.50 − 118,500.00 = **2,645,949.50**, which equals the tidy table's own re-summed `open_amount` column exactly (residual 0.00). See `engagement/work/ar_subledger_2026-06_tidy.csv` (207 rows) and `engagement/output/ar_gl_reconciliation.xlsx` sheet `cleaning_log`.
- As a corroborating check (not part of the AR-to-GL deliverable): `ar_aging_2025-12.csv` bucket total ties exactly to `balance_sheet_fy2025.md` net AR (4,610,000) — different period (Dec-2025 vs the Jun-2026 subledger-tie population) so not combined with the June figures above.

## 4. Reconcile — AR subledger (tidy) to GL account 1200

**Threshold: $5,000** (agreed before any figure computed; see run-log seq 5).

- **First footing (isolated computation)**: Side A (tidy subledger) = **2,645,949.50**; Side B (`gl_summary_2026-06.csv` ending_balance) = **2,619,949.50**; raw difference = **26,000.00** (A over B).
- **Mechanics chased** (separate step, after footing):
  1. *Duplicates*: already removed in the clean step above.
  2. *Timing*: `gl_je_detail_2026-07.csv` JE-7-0043 (2026-07-02) posts **inv-20241, Cedar Valley Co-op, $35,000.00** ("post inv-20241 cedar valley co-op (june billing run)") to account 1200. The subledger includes this invoice in its June population (dated 2026-06-30); the GL does not recognize it until July. This narrows the residual to **−9,000.00** (2,645,949.50 − 35,000.00 = 2,610,949.50 vs GL 2,619,949.50).
  3. *Keying/transposition*: −9,000.00 is exactly divisible by 9 (a transposition hint, not proof). Per updated reconcile guidance, the search was **narrowed** to the 5 remaining irregular/manually-keyed invoices (outside the systematic inv-195xx–197xx sequence, already excluding the removed duplicates and the timing item) rather than scanned blindly across the population. Two digit-swap candidates matched the $9,000 magnitude: inv-19877 Stonebridge Market (subledger recorded 45,000.00; GL 1200 control balance is consistent with this invoice contributing 54,000.00 — a probable transposition **in the GL**, not the subledger) and inv-20314 (10,000.00 ↔ 1,000.00, the second Northern Foods invoice in the b-0621 batch — already counted once as a duplicate removal above, this is the surviving single occurrence). Both were tested against the **required direction**, not just magnitude: only the Stonebridge item (+9,000.00 needed on Side A to reach Side B) closes the equation; the Northern Foods candidate would widen the gap to 18,000.00 and was rejected.
- **Reconciliation statement** (see `engagement/output/ar_gl_reconciliation.xlsx`, sheet `reconciliation`):
  - Side A (tidy): 2,645,949.50
  - Less: timing — inv-20241 ($35,000.00, subledger higher)
  - Add: reconciling item — inv-19877 Stonebridge Market ($9,000.00) — added to Side A only to walk the subledger to the GL's control total; the probable error is **in the GL**, which appears to reflect this invoice at the transposed 54,000.00 rather than the subledger's recorded (and believed correct) 45,000.00
  - Adjusted Side A: 2,619,949.50
  - Side B (GL 1200): 2,619,949.50
  - **Unexplained remainder: 0.00**
- **Caveat on the transposition item**: the $9,000 item is the only candidate, **among the 5 manually-keyed/irregular invoices the search was deliberately narrowed to** (see mechanics above — those outside the systematic inv-195xx–197xx sequence, already excluding removed duplicates and the timing item), that fits the residual's exact size *and* direction. It is **not** the only $9,000 digit-swap match in the full 207-row tidy population: a broader, full-population digit-swap scan turns up dozens of additional mechanical matches within the systematic inv-195xx–197xx sequence, a byproduct of that sequence's formulaic amounts rather than evidence of real errors, which is exactly why the search was narrowed to the manually-keyed subset first. It is also not independently confirmed by a third source (no original Stonebridge Market invoice or sales order in the data room). Carried forward as an open item recommending the original invoice/sales order for inv-19877 be pulled to confirm which figure — the subledger's 45,000.00 or the GL-implied 54,000.00 — is the economically correct one.

## 5. Analyze — FY2025 revenue bridge (FY2024 → FY2025)

**Threshold: $250,000** (agreed before any figure computed; see run-log seq 5, restated at seq 25 before the bridge computation).

- **Gross-basis tie** (independently re-summed): `monthly_revenue_2025.csv` (12 months) = **49,200,000**; `tb_extract_us_fy2025.csv` (acct 4000+4100 = 35,950,000+950,000=36,900,000) + `tb_extract_canada_fy2025.csv` (12,050,000+0) + `tb_extract_holdco_fy2025.csv` (250,000+0) = **49,200,000**. Ties exactly (see `engagement/output/revenue_bridge_fy2025.xlsx`, sheet `gross_tie`).
- **Presentation reclass**: `notes_fy2025.md` note 1 discloses that, beginning FY2025, freight billed to customers ($250,000) is presented net within COGS rather than gross in revenue; prior years (including FY2024) presented it gross; the TB extracts retain the gross presentation. This exactly explains the gap between the 49,200,000 gross tie and the 48,950,000 revenue line reported in `income_statement_fy2025.md`.
- **Bridge** (foots exactly): FY2024 revenue (44,120,000, per `income_statement_fy2025.md`) **+** growth driver (5,080,000 = 49,200,000 − 44,120,000, gross-to-gross, since FY2024 was reported under the same gross convention per the notes) **−** presentation reclass (250,000) **=** FY2025 revenue as reported (48,950,000).
- **Growth driver decomposition**:
  - Lakeside Grocers new contract: `lakeside_grocers_agreement.md` states the contract began 2025-06-01 (did not exist in FY2024) and represents "approximately 6% of consolidated revenue" in FY2025. Applied to the reported 48,950,000, this is **~2,937,000** — an approximation from the source's own rounded language, not an exact figure (also flagged as an assumption).
  - **Open item**: the remaining **2,143,000** of growth (5,080,000 − 2,937,000) cannot be attributed to a named driver from sources in hand (no FY2024 monthly or customer-level revenue detail; Northern Foods' cost-plus-14%-reviewed-annually pricing is a plausible partial contributor but not quantifiable without the repricing schedule). This is **not** an unreconciled bridge remainder — the bridge itself foots to zero — it is a labeled bar carried as an explicit open item because, above the $250,000 threshold, it must be flagged rather than folded silently into "other." **Data request**: FY2024 monthly revenue detail (same format as `monthly_revenue_2025.csv`) or a FY2025 customer-level revenue schedule.

## 6. Assumptions

1. AR-to-GL reconciliation threshold $5,000; revenue-bridge/data-room threshold $250,000 — both stated by the deal lead in the engagement brief, before any source file was opened (run-log seq 5).
2. The 5 duplicate rows in `ar_subledger_2026-06.csv` are one posting entered twice (not two genuine invoices) — judged from all 5 fields matching exactly, including the invoice number.
3. The $9,000 AR reconciling item is treated as a probable digit-transposition **in the GL control balance** for inv-19877 (Stonebridge Market): the subledger records 45,000.00 and is believed correct; the GL 1200 balance is consistent with this invoice contributing 54,000.00 instead. Per updated reconcile guidance, the search for a candidate was deliberately **narrowed to the 5 manually-keyed/irregular invoices** outside the systematic inv-195xx–197xx sequence (see §4, mechanics chased) rather than scanned blindly across the full 207-row tidy population, because that systematic sequence's formulaic amounts produce dozens of coincidental ±9,000 digit-swap matches with no evidentiary weight. Within that narrowed subset, inv-19877 is the only candidate that closes the residual to the exact penny in the required direction. This is **not** a claim that inv-19877 is the only $9,000 digit-swap in the population as a whole, and it is **not** confirmed by an independent third source.
4. FY2024 revenue (44,120,000) is assumed to already be on the gross (pre-reclass) presentation basis, consistent with `notes_fy2025.md`'s statement that "prior years presented it in revenue."
5. The Lakeside Grocers dollar-value driver ($2,937,000) is derived by applying the contract document's own approximate language ("approximately 6% of consolidated revenue") to FY2025 reported revenue — an approximation, not a source-stated dollar figure.
6. `trial-balance/tb_2026-06.xlsx` was profiled for structural hazards and used only as corroborating/contextual information (see tie-point map); it was not required to tie to the subledger-tie AR population or the FY2025 data-room financials, since those are different periods/file families as defined by the engagement scope.

## 7. Open items

| # | Item | Amount | Suspected nature | What would close it |
|---|---|---|---|---|
| 1 | AR subledger vs GL — Stonebridge Market (inv-19877) transposition | $9,000.00 | Probable digit-transposition in the GL control balance (subledger recorded 45,000, GL consistent with 54,000) — the only candidate within the manually-keyed/irregular subset the search was narrowed to (not the full 207-row population, where a broader scan turns up dozens of coincidental matches) that fits the residual exactly in size and direction; unconfirmed by a third source | Original Stonebridge Market sales invoice/sales order for inv-19877 |
| 2 | Revenue bridge — unattributed organic growth | $2,143,000.00 | Existing-customer volume/price mix (e.g., Northern Foods annual cost-plus repricing); not decomposable from sources on hand | FY2024 monthly revenue detail (same format as `monthly_revenue_2025.csv`) or a FY2025 customer-level revenue schedule |
| 3 | TB (2026-06) AR vs subledger-tie GL summary | Gross difference $1,210,050.50 (consolidated TB acct 1200: US 3,050,000 + Canada 780,000, Holdco has no AR = 3,830,000 vs GL summary 2,619,949.50; *v1.1 note: TB regenerated after this run, figure updated*) | Population/scope mismatch — `gl_summary_2026-06.csv` appears to be a single control-account balance of unstated entity scope, not chased against the multi-entity consolidated TB (out of scope per engagement's file-family definition); this is a scope question, not a same-company question — the TB and the data room are the same company | Confirmation from seller of what population `gl_summary_2026-06.csv` represents relative to the consolidated TB |
| 4 | Holdco FY2025 TB extract "product revenue" = $250,000 for an entity shown with zero revenue capacity in the later (2026-06) consolidated TB; coincides exactly with the freight reclass amount | $250,000.00 | Possible misclassification of the freight reclass into Holdco's extract, or coincidence — not resolvable from sources in hand | Management's account-level mapping/support for the Holdco FY2025 revenue entry |
| 5 | Data-quality flag: identical COGS/opex dollar figures (accts 5000/5100/5210/5220/5900) across all three FY2025 TB entity extracts despite very different revenue scale | N/A (structural flag, not a dollar variance) | Confirmed to be a copy/paste error in the fixture generator (`gen_data_room.py`'s `EXPENSE_ROWS` list was shared across all three entities) — **fixed in v1.1**: each entity now has its own expense rows, consolidating to the income statement's cogs (36,210,000) / opex (9,180,000) / interest (1,140,000) | Resolved in v1.1 — no further action needed |
| 6 | Pending litigation (Carter Mechanical v. Brightwater US) — probable loss per outside counsel, no reserve recorded | $400,000–$600,000 | Unrecorded contingency; balance sheet states "no litigation or contingency reserves are recorded" despite counsel's "probable" assessment | Final expert report referenced in `pending_litigation.md`; updated counsel opinion |
| 7 | Northern Foods MSA change-of-control clause — ~22% of consolidated revenue, terminable by customer without consent upon change of control of supplier | ~22% of revenue at risk (not a dollar variance) | Deal-specific consent/waiver risk | Customer consent or waiver from Northern Foods Inc. in connection with the transaction |
| 8 | CEO change-of-control severance (18 months) — amount not quantified in the data room | Unquantified | Potential payout obligation triggered by the transaction | CEO compensation/salary detail (not in data room) |

## 8. Verification

- **AR cleaning**: raw total 2,764,449.50 − removed duplicates 118,500.00 = tidy total 2,645,949.50, re-footed from the tidy CSV itself (not carried from memory). Residual 0.00.
- **AR reconciliation**: reconciliation statement re-verified by summing its own itemized rows (Side A − timing + transposition correction = Adjusted Side A = Side B exactly); unexplained remainder 0.00.
- **Revenue bridge**: gross tie re-summed independently from `monthly_revenue_2025.csv` and the three `tb_extract_*_fy2025.csv` files (both = 49,200,000); bridge re-footed as 44,120,000 + 5,080,000 − 250,000 = 48,950,000, matching the reported income statement figure exactly.
- **Workbook integrity**: both `ar_gl_reconciliation.xlsx` and `revenue_bridge_fy2025.xlsx` were reopened after writing and every cell re-read via openpyxl to confirm no stray blank/formula cells. One defect was caught this way — a citation string beginning with "=" had been silently stored as an unevaluated formula (cached value `None`) — and was corrected (see run-log seq 27) before being accepted as verified.
- **Sources integrity**: `engagement/sources/` was never written to or modified; all outputs are in `engagement/work/` (intermediates) and `engagement/output/` (deliverables). A pre-existing hash manifest (`sources.sha256.pre.txt`) was left untouched.
- **Disclosed sequencing note**: one source file (`data-room/index_readme.md`, a one-paragraph folder manifest with no financial figures) was opened while orienting to the sandbox's folder structure, immediately before the formal brainstorm scope post — logged honestly in `engagement/work/run-log.jsonl` seq 3 rather than reconstructed to look compliant after the fact. No numeric/financial source content was read before the threshold (seq 5) and plan (seq 6) were posted.
