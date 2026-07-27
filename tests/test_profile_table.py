import csv

from scripts.profile_table import profile_table


def make_csv(tmp_path):
    p = tmp_path / "t.csv"
    rows = [
        ["account", "amount"],
        ["A1000", "100.50"],
        ["A1200", "1,000.00"],
        ["A1200", "1,000.00"],   # exact duplicate
        ["A1300", ""],           # blank amount
        ["A1400", "50", "junk"],  # ragged row
    ]
    with open(p, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    return p


def test_profile_counts(tmp_path):
    prof = profile_table(make_csv(tmp_path))
    assert prof["rows"] == 5
    assert prof["duplicate_rows"] == 1
    assert prof["ragged_rows"] == 1


def test_profile_columns(tmp_path):
    prof = profile_table(make_csv(tmp_path))
    amount = next(c for c in prof["columns"] if c["name"] == "amount")
    assert amount["type"] == "numeric"
    assert amount["sum"] == 2150.5
    assert amount["blank"] == 1
    account = next(c for c in prof["columns"] if c["name"] == "account")
    assert account["type"] == "text" and account["distinct"] == 4
