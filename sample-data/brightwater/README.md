# brightwater distribution co. — sample data

Entirely synthetic. Brightwater is a fictional small multi-entity US/Canada
distributor being acquired. Three scenarios chain into one mini-engagement:

- `trial-balance/` — a ragged consolidated TB export (merged title, section
  headers, double-counting subtotal rows, a duplicate account row, a
  text-typed amount, a grand-total row).
- `subledger-tie/` — AR subledger vs GL that differ by exactly $144,500.00
  (duplicate batch b-0621 $118,500.00 + June invoice posted to GL in July
  $35,000.00 − a $9,000.00 keying transposition in the GL).
- `data-room/` — a small diligence data room (~18 files) with planted
  findings (a revenue reclass, a change-of-control clause, an off-balance-
  sheet litigation contingency).

Regenerate with the scripts in `tests/generators/`. Treat everything here
as read-only fixture data — engagements copy it into their own `sources/`.
