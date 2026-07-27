"""Generate the Brightwater diligence data room (18 files, all synthetic)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "sample-data" / "brightwater" / "data-room"

REV_IS = 48_950_000          # income statement revenue
REV_RECLASS = 250_000        # freight revenue netted into cogs per notes
TB_REVENUE = {"us": 36_900_000, "canada": 12_050_000, "holdco": REV_RECLASS}
assert sum(TB_REVENUE.values()) == REV_IS + REV_RECLASS

MD_FILES = {
    "financials/income_statement_fy2025.md": f"""# brightwater distribution co. — income statement fy2025 (unaudited)
| line | fy2025 | fy2024 |
|---|---|---|
| revenue | {REV_IS:,} | 44,120,000 |
| cost of goods sold | (36,210,000) | (32,780,000) |
| gross profit | 12,740,000 | 11,340,000 |
| operating expenses | (9,180,000) | (8,420,000) |
| ebitda | 3,560,000 | 2,920,000 |
| depreciation & interest | (1,140,000) | (1,050,000) |
| pre-tax income | 2,420,000 | 1,870,000 |
""",
    "financials/balance_sheet_fy2025.md": """# brightwater distribution co. — balance sheet 2025-12-31 (unaudited)
| line | 2025-12-31 |
|---|---|
| cash | 2,140,000 |
| accounts receivable, net | 4,610,000 |
| inventory | 5,890,000 |
| fixed assets, net | 3,220,000 |
| total assets | 15,860,000 |
| accounts payable | 3,410,000 |
| accrued liabilities | 1,120,000 |
| term loan | 4,800,000 |
| total liabilities | 9,330,000 |
| equity | 6,530,000 |

no litigation or contingency reserves are recorded.
""",
    "financials/notes_fy2025.md": """# notes to fy2025 financials (management-prepared)
1. revenue: beginning fy2025, freight billed to customers (250,000) is
   presented net within cost of goods sold; prior years presented it in
   revenue. trial balance extracts retain the gross presentation.
2. inventory is fifo, lower of cost or nrv.
3. these statements are unaudited and management-prepared.
""",
    "contracts/northern_foods_msa.md": """# master supply agreement — northern foods inc.
- term: 2024-01-01 through 2027-12-31, auto-renewing annually thereafter.
- fy2025 volume: approximately 22% of brightwater consolidated revenue.
- pricing: cost-plus 14%, reviewed annually.
- section 11.2 (assignment): this agreement may not be assigned, and shall
  be terminable by customer, upon any change of control of supplier
  without customer's prior written consent.
""",
    "contracts/lakeside_grocers_agreement.md": """# supply agreement — lakeside grocers llc
- term: 2025-06-01 through 2026-05-31, month-to-month thereafter.
- fy2025 volume: approximately 6% of consolidated revenue.
- standard assignment clause; assignable to an acquirer of substantially
  all assets without consent.
""",
    "debt/term_loan_agreement.md": """# term loan agreement — first cascade bank
- original principal 6,000,000; balance 4,800,000 at 2025-12-31.
- rate: sofr + 275bps. maturity 2029-06-30.
- covenants: minimum fixed charge coverage 1.25x, tested quarterly;
  maximum total leverage 3.0x.
- prepayment: 1% penalty if repaid before 2027-06-30.
""",
    "tax/tax_summary.md": """# tax position summary (management-prepared)
- us federal and state returns filed through fy2024; fy2025 on extension.
- canada (bc) returns filed through fy2024.
- no open audits. r&d credits: none claimed.
""",
    "hr/bonus_plan.md": """# management bonus plan
- pool: 8% of ebitda above 3,000,000, paid in march following year-end.
- fy2025 accrual: 44,800 (included in accrued liabilities).
- ceo employment agreement includes 18-month severance on termination
  following a change of control.
""",
    "legal/pending_litigation.md": """# pending litigation summary (prepared by outside counsel)
- carter mechanical v. brightwater us: warranty claim on 2024 product
  batch. counsel assesses loss as probable; estimated range 400,000 to
  600,000. no amount has been accrued pending final expert report.
- no other material matters.
""",
    "index_readme.md": """# brightwater data room
uploaded by seller's banker. folders: financials, contracts, debt, tax,
hr, legal. monthly tb extracts are per-entity, gross presentation.
""",
}

CSV_FILES = {
    "financials/tb_extract_us_fy2025.csv": TB_REVENUE["us"],
    "financials/tb_extract_canada_fy2025.csv": TB_REVENUE["canada"],
    "financials/tb_extract_holdco_fy2025.csv": TB_REVENUE["holdco"],
}

# fixed, deterministic expense rows per entity (account, description, base amount)
EXPENSE_ROWS = [
    (5000, "cost of goods sold", 5_400_000),
    (5100, "freight out", 210_000),
    (5210, "salaries and wages", 1_860_000),
    (5220, "employee benefits", 340_000),
    (5900, "interest expense", 84_000),
]


def write_md_files():
    for rel, content in MD_FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def write_tb_extracts():
    """Per-entity TB extract CSVs: revenue rows (4000+4100) tie to TB_REVENUE."""
    for rel, value in CSV_FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        is_us = "_us_" in rel
        product_rev = value - 950_000 if is_us else value
        freight_rev = 950_000 if is_us else 0
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["account", "description", "fy2025_amount"])
            writer.writerow([4000, "product revenue", product_rev])
            writer.writerow([4100, "freight revenue", freight_rev])
            for acct, desc, amt in EXPENSE_ROWS:
                writer.writerow([acct, desc, amt])


def write_ar_aging():
    """5 aging buckets summing to gross 4,790,000, plus allowance -180,000 -> net 4,610,000."""
    path = ROOT / "financials/ar_aging_2025-12.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    buckets = [
        ("current", 2_690_000),
        ("1-30 days", 1_180_000),
        ("31-60 days", 540_000),
        ("61-90 days", 260_000),
        ("over 90 days", 120_000),
    ]
    gross = sum(amt for _, amt in buckets)
    assert gross == 4_790_000, f"ar aging gross mismatch: {gross}"
    allowance = -180_000
    net = gross + allowance
    assert net == 4_610_000, f"ar aging net mismatch: {net}"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["bucket", "amount"])
        for bucket, amt in buckets:
            writer.writerow([bucket, amt])
        writer.writerow(["allowance for doubtful accounts", allowance])


def write_amortization_schedule():
    """8 quarterly rows from 2026-03-31, principal 150,000 each, interest = prior balance x 0.0175."""
    path = ROOT / "debt/amortization_schedule.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    dates = [
        "2026-03-31", "2026-06-30", "2026-09-30", "2026-12-31",
        "2027-03-31", "2027-06-30", "2027-09-30", "2027-12-31",
    ]
    balance = 4_800_000
    principal = 150_000
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["payment_date", "principal", "interest", "balance"])
        for date in dates:
            interest = round(balance * 0.0175, 2)
            balance = balance - principal
            writer.writerow([date, principal, interest, balance])


def write_headcount():
    """6 departments, fte totals 118 (2024) and 127 (2025)."""
    path = ROOT / "hr/headcount.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ("warehouse & logistics", 42, 46),
        ("sales", 28, 31),
        ("finance & accounting", 9, 10),
        ("customer service", 14, 16),
        ("it & operations support", 8, 9),
        ("executive & admin", 17, 15),
    ]
    total_2024 = sum(r[1] for r in rows)
    total_2025 = sum(r[2] for r in rows)
    assert total_2024 == 118, f"fte 2024 mismatch: {total_2024}"
    assert total_2025 == 127, f"fte 2025 mismatch: {total_2025}"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["department", "fte_2024", "fte_2025"])
        for dept, fte24, fte25 in rows:
            writer.writerow([dept, fte24, fte25])


def write_cap_table():
    """founders 62%, mezz fund 28%, option pool 10%."""
    path = ROOT / "legal/cap_table.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ("founders", 6_200_000, 62),
        ("mezz fund", 2_800_000, 28),
        ("option pool", 1_000_000, 10),
    ]
    assert sum(r[2] for r in rows) == 100
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["holder", "shares", "percent"])
        for holder, shares, pct in rows:
            writer.writerow([holder, shares, pct])


def write_monthly_revenue():
    """12 rows summing to exactly 49,200,000 (gross)."""
    path = ROOT / "financials/monthly_revenue_2025.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    months = [
        ("2025-01", 3_820_000), ("2025-02", 3_760_000), ("2025-03", 4_050_000),
        ("2025-04", 4_010_000), ("2025-05", 4_130_000), ("2025-06", 4_220_000),
        ("2025-07", 4_180_000), ("2025-08", 4_090_000), ("2025-09", 4_160_000),
        ("2025-10", 4_240_000), ("2025-11", 4_280_000), ("2025-12", 4_260_000),
    ]
    total = sum(amt for _, amt in months)
    assert total == 49_200_000, f"monthly revenue total mismatch: {total}"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "gross_revenue"])
        for month, amt in months:
            writer.writerow([month, amt])


def main():
    write_md_files()
    write_tb_extracts()
    write_ar_aging()
    write_amortization_schedule()
    write_headcount()
    write_cap_table()
    write_monthly_revenue()

    files = sorted(p for p in ROOT.rglob("*") if p.is_file())
    file_count = len(files)
    assert file_count == 18, f"expected 18 files, found {file_count}: {files}"

    # revenue tie-out identity: three TB extracts' revenue accounts (4000+4100)
    # sum to exactly 49,200,000 = income statement 48,950,000 + reclass 250,000
    tb_revenue_total = 0
    for rel in CSV_FILES:
        path = ROOT / rel
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["account"]) in (4000, 4100):
                    tb_revenue_total += int(row["fy2025_amount"])
    assert tb_revenue_total == REV_IS + REV_RECLASS == 49_200_000, (
        f"revenue identity failed: tb={tb_revenue_total}, "
        f"is+reclass={REV_IS + REV_RECLASS}"
    )

    print("18 files written")
    print(
        f"revenue identity: tb extracts {tb_revenue_total:,} == "
        f"income statement {REV_IS:,} + reclass {REV_RECLASS:,}"
    )


if __name__ == "__main__":
    main()
