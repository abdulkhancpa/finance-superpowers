"""Tidy-table profiler: structure, control totals, and mess signals for a CSV.

Note: type inference is purely lexical — a column of all-digit identifiers
(account codes, invoice numbers) profiles as numeric and receives a sum.
Consumers must judge whether a numeric column's sum is a meaningful control total.
"""
import csv
import json
import sys
from collections import Counter


def _as_number(s):
    """Parse a value as a number, tolerant of accounting formatting:
    thousands separators (1,234.00), a leading currency symbol
    ($5,000.00), and parenthesized negatives ((1,234.00) -> -1234.00).
    """
    text = str(s).strip()
    negative = text.startswith("(") and text.endswith(")")
    if negative:
        text = text[1:-1].strip()
    text = text.replace(",", "").replace("$", "").strip()
    try:
        num = float(text)
    except ValueError:
        return None
    return -num if negative else num


def profile_table(csv_path):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if not rows:
        return {"file": str(csv_path), "rows": 0, "duplicate_rows": 0,
                "ragged_rows": 0, "columns": []}
    header, data = rows[0], rows[1:]
    dupes = sum(n - 1 for n in Counter(map(tuple, data)).values() if n > 1)
    ragged = sum(1 for r in data if len(r) != len(header))
    columns = []
    for i, name in enumerate(header):
        vals = [r[i] for r in data if len(r) > i]
        nonblank = [v for v in vals if v.strip()]
        numbers = [n for n in (_as_number(v) for v in nonblank) if n is not None]
        col = {
            "name": name,
            "blank": len(vals) - len(nonblank),
            "distinct": len(set(nonblank)),
            "type": "numeric" if nonblank and len(numbers) == len(nonblank) else "text",
        }
        if col["type"] == "numeric":
            col["sum"] = round(sum(numbers), 2)
        columns.append(col)
    return {"file": str(csv_path), "rows": len(data), "duplicate_rows": dupes,
            "ragged_rows": ragged, "columns": columns}


def main():
    print(json.dumps(profile_table(sys.argv[1]), indent=2))


if __name__ == "__main__":
    main()
