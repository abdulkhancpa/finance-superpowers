"""Generate the Brightwater ragged trial balance fixture.

Self-checking: asserts the clean account rows net to exactly zero and the
planted messes are present before saving. Deterministic — no randomness.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

OUT = Path(__file__).resolve().parents[2] / "sample-data" / "brightwater" / "trial-balance" / "tb_2026-06.xlsx"

SECTIONS = [
    ("assets", [(1000, "cash - operating"), (1010, "cash - payroll"),
                (1200, "accounts receivable"), (1210, "allowance for doubtful accounts"),
                (1300, "inventory - finished goods"), (1400, "prepaid expenses"),
                (1500, "fixed assets"), (1510, "accumulated depreciation")]),
    ("liabilities", [(2000, "accounts payable"), (2100, "accrued liabilities"),
                     (2200, "deferred revenue"), (2500, "term loan - current"),
                     (2600, "term loan - long term")]),
    ("equity", [(3000, "common stock"), (3900, "retained earnings")]),
    ("revenue", [(4000, "product revenue"), (4100, "freight revenue")]),
    ("expenses", [(5000, "cost of goods sold"), (5100, "freight out"),
                  (5210, "salaries and wages"), (5220, "employee benefits"),
                  (5300, "rent"), (5400, "depreciation"), (5900, "interest expense")]),
]
ENTITIES = ["brightwater us", "brightwater canada", "brightwater holdco"]


def amount(entity_ix, acct, name):
    """Deterministic pseudo-amounts; sign by account class."""
    base = (acct * 7 + entity_ix * 131) % 9000 * 97 + acct / 100
    if acct < 2000:
        sign = -1 if "accumulated" in name or "allowance" in name else 1
    elif acct < 4000:
        sign = -1
    elif acct < 5000:
        sign = -1
    else:
        sign = 1
    return round(sign * base, 2)


def build_rows():
    rows, balance = [], 0.0
    for ent_ix, entity in enumerate(ENTITIES):
        rows.append(("entity_header", entity, None, None))
        for section, accounts in SECTIONS:
            subtotal = 0.0
            for acct, name in accounts:
                if entity == "brightwater holdco" and acct >= 4000 and acct != 5900:
                    continue  # holdco has no operations
                amt = amount(ent_ix, acct, name)
                if (acct, name) == (3900, "retained earnings"):
                    continue  # placeholder; balanced below
                rows.append(("account", entity, acct, (name, amt)))
                subtotal += amt
                balance += amt
            rows.append(("subtotal", entity, None, (f"total {section}", round(subtotal, 2))))
        # balance the entity via retained earnings
    # single consolidated retained-earnings balancer on holdco
    rows.append(("account", "brightwater holdco", 3900,
                 ("retained earnings", round(-balance, 2))))
    return rows


def main():
    rows = build_rows()
    clean_sum = round(sum(r[3][1] for r in rows if r[0] == "account"), 2)
    if clean_sum == 0.0:
        clean_sum = 0.0  # normalize -0.0 (floating-point residue) to 0.0
    assert clean_sum == 0.0, f"TB does not balance: {clean_sum}"

    wb = Workbook()
    ws = wb.active
    ws.title = "tb"
    ws.merge_cells("A1:E2")
    ws["A1"] = "Brightwater Distribution Co. — Consolidated Trial Balance — June 30, 2026 (all entities, local currency USD)"
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["entity", "account", "description", "", "balance"])
    dup_written = False
    text_amount_written = False
    for kind, entity, acct, payload in rows:
        if kind == "entity_header":
            ws.append([entity.upper(), None, None, None, None])
        elif kind == "subtotal":
            name, amt = payload
            ws.append([None, None, name.upper(), None, amt])
        else:
            name, amt = payload
            if acct == 1400 and not text_amount_written:
                amt_out = f"{amt:,.2f}"  # planted: amount stored as text
                text_amount_written = True
            else:
                amt_out = amt
            ws.append([entity, acct, name, None, amt_out])
            if acct == 5210 and entity == "brightwater canada" and not dup_written:
                ws.append([entity, acct, name, None, amt])  # planted duplicate
                dup_written = True
    grand = round(sum(r[3][1] for r in rows if r[0] != "entity_header"), 2)
    ws.append([None, None, "GRAND TOTAL", None, grand])

    assert dup_written and text_amount_written
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT}; clean sum {clean_sum}; naive grand total {grand}")


if __name__ == "__main__":
    main()
