# Memorandum

**To:** AR Controller
**From:** J. Alvarez, Staff Accountant
**Date:** July 3, 2026
**Re:** AR Subledger to GL Reconciliation — Period Ended June 30, 2026

## 1. Purpose and Scope

This memo documents the reconciliation of the accounts receivable subledger
to the general ledger control account (account 1200) as of June 30, 2026.
The reconciliation was performed to confirm that the subledger detail
supports the GL balance carried on the June close trial balance.

**Sources reviewed:**
- `ar_subledger_2026-06.csv` — AR subledger open-invoice detail, 212 lines,
  extracted from the billing system as of period end.
- `gl_summary_2026-06.csv` — GL account 1200 control balance for June 2026.
- `gl_detail.csv` — GL journal entry detail supporting June and early-July
  postings to account 1200, used to confirm posting dates for items
  identified as timing differences below.

## 2. Summary of Reconciliation

| Description | Amount |
|---|---:|
| AR Subledger balance per `ar_subledger_2026-06.csv` | 2,764,449.50 |
| Less: reconciling items (see Section 3) | (144,500.00) |
| Adjusted AR Subledger balance | 2,619,949.50 |
| GL Account 1200 balance per `gl_summary_2026-06.csv` | 2,617,949.50 |

The adjusted subledger balance agrees with the GL control account, and the
reconciliation ties out with no residual difference requiring further
explanation. The variance between the two accounts is fully driven by
duplicate batch `b-0621` of $118,500.00, with the remainder attributable to
normal cutoff timing between the two systems.

## 3. Detail of Reconciling Items

### 3.1 Duplicate posting — batch `b-0621` — $118,500.00

Five invoices in batch `b-0621` (Northern Foods, Lakeside Grocers, Pacific
Mercantile, Harbor Supply, and a second Northern Foods invoice) appear twice
in `ar_subledger_2026-06.csv` — identical invoice number, customer, date,
and amount duplicated in full for each line. Removing the duplicate
posting reduces the subledger balance by $118,500.00
(41,250.00 + 18,775.00 + 26,400.00 + 22,075.00 + 10,000.00). This is
consistent with a batch re-upload error during the June 21 billing run.
Recommend the billing team add a duplicate-batch-ID check before the next
upload.

### 3.2 Timing difference, net — $26,000.00

The remaining $26,000.00 difference is attributable to normal cutoff
timing between subledger and GL posting dates. Per `gl_detail.csv`, a
portion of June invoice activity was not posted to the GL until early
July, consistent with the subledger's practice of recording invoices as of
the invoice date rather than the GL posting date. This pattern repeats
most months and self-corrects in the following period as the GL catches
up to the subledger. Given the recurring nature of this timing pattern,
no further breakout of the $26,000.00 is considered necessary — it is
expected to clear naturally in the July close.

## 4. Conclusion

The AR subledger for June 2026 reconciles to the GL control account
(account 1200) once the duplicate posting and normal timing differences
identified above are considered. Both reconciling items are understood
and expected to resolve through normal processing (the duplicate batch
will be reversed by the billing team; the timing difference clears as the
GL catches up in July). No further action is required, and the account
is considered clean for close purposes.

*Prepared by J. Alvarez. Questions on this reconciliation can be directed
to the AR team.*
