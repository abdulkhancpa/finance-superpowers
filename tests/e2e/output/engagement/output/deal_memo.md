# Brightwater Distribution Co. — Initial Financial Diligence Memo

**Prepared for:** Deal lead
**Prepared by:** Finance diligence workstream (finance-superpowers discipline)
**Date:** 2026-07-28
**Sources examined:** `trial-balance/tb_2026-06.xlsx`; `subledger-tie/ar_subledger_2026-06.csv`, `gl_summary_2026-06.csv`, `gl_je_detail_2026-07.csv`; all 18 files in `data-room/` (contracts, debt, financials, hr, legal, tax, index readme). Full citations and re-performable math are in `engagement/output/workpaper.md`.

## Headline findings

1. **The AR-to-GL tie is fully explained, with zero unexplained remainder** — the $26,000 raw gap between the AR subledger (`subledger-tie/ar_subledger_2026-06.csv`) and the GL control account (`subledger-tie/gl_summary_2026-06.csv`) is fully accounted for by a $35,000 June/July cutoff timing item (`subledger-tie/gl_je_detail_2026-07.csv`) and a probable $9,000 invoice transposition (`subledger-tie/ar_subledger_2026-06.csv`, inv-19877) — see `engagement/output/ar_gl_reconciliation.xlsx`.
2. **FY2025 revenue grew $4,830,000 (44,120,000 -> 48,950,000) year-over-year** (`data-room/financials/income_statement_fy2025.md`), of which $250,000 is a presentation reclass (freight moved from gross revenue into net-within-COGS, per `data-room/financials/notes_fy2025.md`) and roughly $2,937,000 is attributable to a new customer contract (Lakeside Grocers, per `data-room/contracts/lakeside_grocers_agreement.md`); the remaining ~$2,143,000 of growth is not attributable to a named driver from the sources in hand — see `engagement/output/revenue_bridge_fy2025.xlsx`.
3. **Two data-room items warrant deal-team attention before signing**: an unrecorded, counsel-assessed-probable litigation exposure of $400,000-$600,000 (`data-room/legal/pending_litigation.md`), and a change-of-control termination right held by Northern Foods Inc., a customer representing ~22% of consolidated revenue (`data-room/contracts/northern_foods_msa.md`).

## Basis and detail

### AR reconciliation (threshold: $5,000)

What the sources say: the AR subledger (`ar_subledger_2026-06.csv`) sums to $2,764,449.50 across 212 rows; the GL control account 1200 (`gl_summary_2026-06.csv`) shows $2,619,949.50 for the same period (2026-06).

What we computed: 5 of the 212 subledger rows are exact duplicates (same invoice number, customer, date, amount, and batch `b-0621`, posted twice) -- removing them brings the subledger to $2,645,949.50. The remaining $26,000 gap decomposes into (a) a $35,000 timing item -- invoice inv-20241 (Cedar Valley Co-op) is in the subledger's June population but was not posted to the GL until July 2 per JE-7-0043 (`gl_je_detail_2026-07.csv`) -- and (b) a $9,000 residual that, when narrowed to the population's own irregular/manually-keyed invoices and tested against the residual's exact size and direction, fits only one candidate: inv-19877 (Stonebridge Market), recorded at $45,000.00, where a digit transposition to $54,000.00 closes the tie exactly.

What we assume: that the 5 duplicate rows are one posting entered twice, not two genuine invoices (justified because every field matches, including the invoice number, which cannot legitimately repeat).

What we could not verify: the $9,000 Stonebridge transposition is the only candidate that fits the math, but it is **not independently confirmed** -- there is no original invoice or sales order for Stonebridge Market in the data room to prove the true amount is $54,000. This is flagged as an open item, not asserted as fact.

### FY2025 revenue movement (threshold: $250,000)

What the sources say: `income_statement_fy2025.md` reports FY2025 revenue of $48,950,000 vs. FY2024 of $44,120,000. Independently, `monthly_revenue_2025.csv` (12 months) and the three FY2025 entity TB extracts (`tb_extract_us/canada/holdco_fy2025.csv`) both sum to $49,200,000 gross -- they tie to each other exactly.

What we computed: the $250,000 gap between the $49,200,000 gross figure and the $48,950,000 reported figure is exactly explained by the freight-reclass policy change disclosed in `notes_fy2025.md` (freight moved from gross revenue into net-within-COGS beginning FY2025). Treating FY2024 as being on the same (pre-reclass) gross basis, the underlying like-for-like growth is $5,080,000. Of that, `lakeside_grocers_agreement.md` states the Lakeside Grocers contract began 2025-06-01 (did not exist in FY2024) and represents "approximately 6% of consolidated revenue" -- applying that to reported FY2025 revenue gives an approximate $2,937,000 new-customer driver.

What we assume: that FY2024's reported revenue was already presented gross (consistent with the notes' statement that "prior years presented it in revenue"), making the FY2024-to-FY2025-gross comparison like-for-like; and that the Lakeside dollar estimate, derived from the contract's own rounded "~6%" language, is an approximation rather than an exact source figure.

What we could not verify: the remaining ~$2,143,000 of growth cannot be attributed to a specific driver (e.g., Northern Foods' annual cost-plus repricing, or broader existing-customer volume) because the data room does not include FY2024 monthly or customer-level revenue detail. This is an open item, not folded into the Lakeside figure or silently dropped.

### Data-room red flags (threshold: $250,000, or qualitative where noted)

- **Unrecorded litigation contingency**: `legal/pending_litigation.md` -- outside counsel assesses the Carter Mechanical warranty claim as *probable*, with an estimated range of $400,000-$600,000, and states "no amount has been accrued." `financials/balance_sheet_fy2025.md` separately states "no litigation or contingency reserves are recorded." This is an inference, not a sourced fact: a probable-and-estimable loss is customarily accrued under most GAAP frameworks, so the absence of an accrual here is worth flagging to the deal team as a likely balance-sheet adjustment, not asserted as a definitive GAAP violation without further review.
- **Customer concentration / change-of-control risk**: `contracts/northern_foods_msa.md` -- Northern Foods represents "approximately 22% of consolidated revenue" and section 11.2 lets the customer terminate on any change of control of the supplier without its prior consent. This is a direct, quantifiable deal risk (potential loss of ~22% of revenue) that should be addressed via customer consent procurement pre-close. By contrast, `contracts/lakeside_grocers_agreement.md` (~6% of revenue) is freely assignable to an acquirer -- no flag there.
- **CEO change-of-control severance**: `hr/bonus_plan.md` discloses an 18-month severance obligation triggered by a change of control; the dollar amount is not quantifiable from the data room (no salary/compensation detail provided).
- **Data-quality flag in the FY2025 entity TB extracts**: the three files `tb_extract_us/canada/holdco_fy2025.csv` show *identical* dollar figures for COGS and all four operating-expense line items across US, Canada, and Holdco, despite the entities having very different revenue scale ($36.9M / $12.05M / $0.25M respectively). This looks like a possible copy/paste or placeholder error at the source and warrants a re-pull before these extracts are relied on for entity-level analysis.
- **Holdco recording $250,000 of "product revenue" in FY2025** (`tb_extract_holdco_fy2025.csv`) is an unexplained coincidence worth asking about: Holdco shows zero revenue capacity in the later (2026-06) consolidated TB (`trial-balance/tb_2026-06.xlsx`), yet its FY2025 extract shows exactly the same dollar amount as the freight reclass disclosed in the notes. We could not determine from the sources in hand whether this is a misclassification or unrelated.
- **Trial balance vs. AR-tie population mismatch**: the 2026-06 consolidated TB's AR (accounts 1200 across US/Canada/Holdco, summing to $2,482,557) does not tie to the AR-subledger-tie file family's GL figure ($2,619,949.50) for the same stated period. We have not chased this -- it appears to be a different population/scope, and it is out of the AR reconciliation's defined scope -- but the deal team should confirm with the seller what each file represents before relying on either in isolation.
- No findings above threshold in tax (`tax/tax_summary.md`: no open audits, FY2025 on extension -- routine) or debt (`debt/term_loan_agreement.md` and `amortization_schedule.csv` tie cleanly to the balance sheet).

## Limitations

This is an initial diligence pass on unaudited, management-prepared financials (per `financials/balance_sheet_fy2025.md` and `financials/notes_fy2025.md`) and seller-provided extracts. Findings are bounded by what these source files show; several open items below name the specific additional document needed to close them.

## Assumptions

- Explanation thresholds -- $5,000 for the AR reconciliation, $250,000 for the revenue bridge and data-room findings -- were set by the deal lead before any figure was computed.
- The 5 duplicate AR subledger rows are one posting entered twice, not two genuine invoices.
- FY2024 revenue is assumed reported on the same gross (pre-freight-reclass) basis as the FY2025 TB extracts, per the notes' own statement about prior-year presentation.
- The Lakeside Grocers ~$2,937,000 driver is an approximation derived from the contract's stated "~6%" language, not an exact source figure.

## Open items (see workpaper.md section 7 for full detail and exact amounts)

1. Stonebridge Market (inv-19877) $9,000 transposition -- needs the original invoice/sales order to confirm.
2. $2,143,000 of FY2025 revenue growth unattributed to a named driver -- needs FY2024 monthly or customer-level revenue detail.
3. $137,392.50 population mismatch between the 2026-06 consolidated TB's AR and the subledger-tie GL figure -- needs seller confirmation of scope.
4. Holdco's $250,000 FY2025 "product revenue" entry -- needs management's account-level mapping/support.
5. Identical COGS/opex figures across the three FY2025 entity TB extracts -- needs a re-pull from the source system.
6. Carter Mechanical litigation ($400,000-$600,000, probable, unaccrued) -- needs the final expert report.
7. Northern Foods change-of-control consent (~22% of revenue at risk) -- needs customer consent/waiver.
8. CEO change-of-control severance amount -- needs compensation detail (not in data room).

## Prepared-by / sources-examined

Prepared by the finance diligence workstream under the finance-superpowers discipline (brainstorm -> understand -> clean -> transform -> reconcile -> analyze -> document). Full source list, citations, computations, and verification steps are reperformable from `engagement/output/workpaper.md` and `engagement/work/run-log.jsonl`. Supporting workbooks: `engagement/output/ar_gl_reconciliation.xlsx`, `engagement/output/revenue_bridge_fy2025.xlsx`.
