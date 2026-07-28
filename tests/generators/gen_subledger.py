"""Generate the Brightwater AR subledger-vs-GL fixture.

Self-checking: asserts the reconciliation identity
  subledger_total - gl_balance == dup_batch + timing - transposition
before writing anything. Deterministic — no randomness.
"""
import csv
from pathlib import Path

OUTDIR = Path(__file__).resolve().parents[2] / "sample-data" / "brightwater" / "subledger-tie"

GL_BALANCE = 2_619_949.50
DUP_BATCH_TOTAL = 118_500.00
TIMING = 35_000.00
TRANSPOSITION = 9_000.00  # inv-19877: GL keyed 54,000.00, correct 45,000.00

DUP_BATCH = [  # batch b-0621, sums to DUP_BATCH_TOTAL
    ("inv-20310", "cust-014 northern foods", "2026-06-21", 41_250.00),
    ("inv-20311", "cust-032 lakeside grocers", "2026-06-21", 18_775.00),
    ("inv-20312", "cust-007 pacific mercantile", "2026-06-21", 26_400.00),
    ("inv-20313", "cust-051 harbor supply", "2026-06-21", 22_075.00),
    ("inv-20314", "cust-014 northern foods", "2026-06-21", 10_000.00),
]


def base_invoices():
    """~200 deterministic open invoices, excluding the special ones."""
    invoices, total = [], 0.0
    customers = [f"cust-{i:03d} account {i}" for i in range(1, 41)]
    n = 0
    i = 0
    while n < 200:
        i += 1
        num = f"inv-{19500 + i}"
        if num in ("inv-19877", "inv-20241"):
            continue
        amt = round(((i * 137) % 400) * 61 + 250 + (i % 7) * 0.25, 2)
        invoices.append((num, customers[i % 40], f"2026-{4 + (i % 3):02d}-{1 + (i % 28):02d}", amt))
        total += amt
        n += 1
    return invoices, round(total, 2)


def main():
    invoices, base_total = base_invoices()
    correct_19877 = 45_000.00
    sub_rows = (invoices
                + [("inv-19877", "cust-022 stonebridge market", "2026-05-14", correct_19877)]
                + [("inv-20241", "cust-009 cedar valley co-op", "2026-06-30", TIMING)]
                + [r + ("b-0621",) for r in DUP_BATCH]
                + [r + ("b-0621",) for r in DUP_BATCH])  # planted duplicate posting
    sub_total = round(sum(r[3] for r in sub_rows), 2)

    # GL = everything once, 19877 at the transposed amount, no timing invoice
    gl_implied = round(base_total + (correct_19877 + TRANSPOSITION) + DUP_BATCH_TOTAL, 2)
    assert gl_implied == GL_BALANCE, f"adjust GL_BALANCE to {gl_implied}"
    assert round(sub_total - GL_BALANCE, 2) == round(
        DUP_BATCH_TOTAL + TIMING - TRANSPOSITION, 2), "identity broken"

    OUTDIR.mkdir(parents=True, exist_ok=True)
    with open(OUTDIR / "ar_subledger_2026-06.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["invoice", "customer", "invoice_date", "open_amount", "batch"])
        for r in sub_rows:
            row = list(r)
            if len(row) == 4:
                row.append("")  # blank batch when absent
            w.writerow(row)
    with open(OUTDIR / "gl_summary_2026-06.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["account", "description", "period", "ending_balance"])
        w.writerow(["1200", "accounts receivable - trade", "2026-06", f"{GL_BALANCE:.2f}"])
    with open(OUTDIR / "gl_je_detail_2026-07.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["je", "date", "account", "memo", "amount"])
        w.writerow(["je-7-0043", "2026-07-02", "1200",
                    "post inv-20241 cedar valley co-op (june billing run)", f"{TIMING:.2f}"])
    print(f"subledger {sub_total:,.2f} vs GL {GL_BALANCE:,.2f} "
          f"diff {sub_total - GL_BALANCE:,.2f}")


if __name__ == "__main__":
    main()
