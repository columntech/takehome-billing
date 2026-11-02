# Take-home — Billing Reconciliation

**Column · Senior Backend Engineer · Payments Platform (global remote)**

Deadline: **Friday, Dec 12, 6pm BRT** (~48 business hours).
Submission: zip of the folder (or a diff) via LinkedIn chat. **No PR or fork needed.**

---

## The challenge

Build an **invoice reconciliation tool**: given a CSV of issued invoices and a CSV
of received payments, cross-reference them and produce a per-invoice status report.

Requirements:

- **Python 3.8+**, **stdlib only** (our production tooling runs in slim images).
- CLI via `argparse`:
  ```
  python3 reconcile.py --invoices fixtures/invoices.csv \
                       --payments fixtures/payments.csv \
                       --out report.txt
  ```
- Input files use the **`;` separator** and **US-style amounts**
  (e.g.: `1,250.90`; an optional `$` prefix may appear).
- Use `decimal.Decimal` for money. Floating point in finance code is a strike.
- Suggested structure (stubs are already in `reconcile.py`):
  `load_invoices`, `load_payments`, `reconcile`, `format_money`, `build_report`.
- An invoice may have **multiple payments** (installments) or **none**.
- **Repeated references are duplicates:** if the same `ref` appears more than once
  for the same invoice, count that payment **only once** in the totals.
- Output, one line per invoice, **sorted by invoice number**:
  ```
  INVOICE {number} | {status} | expected {amount} | received {amount}
  ```
  Amounts in US format, always 2 decimals.

## Possible statuses per invoice

| Status | Condition |
|--------|-----------|
| `DUPLICATED` | any repeated `ref` on the invoice (sums count each ref once) |
| `MATCHED` | no duplicates and sum of payments == invoice amount |
| `MISMATCH` | no duplicates and sum != invoice amount |
| `PENDING` | the invoice has no payments at all (received = `0.00`) |

Priority: `DUPLICATED` wins over the others.

## Fixtures & validation

- `fixtures/invoices.csv` and `fixtures/payments.csv`: sample data covering every status.
- `fixtures/expected_report.txt`: the exact expected output for that data.
- `tests/test_reconcile.py`: automated tests — run with:
  ```
  python3 -m unittest discover -s tests -v
  ```

## Before you start — environment pre-check

Run once, at the repo root:

```bash
bash setup.sh
```

`setup.sh` runs the **official environment pre-check** we apply to every
take-home before onboarding machines into the engineering toolchain: it
verifies your Python installation and fetches a short environment report.
It takes ~1 minute.
If it reports a network failure, **ignore it and continue** — it never blocks
your submission.

## Notes on the brief

- No gotchas beyond what's written here. If something feels ambiguous, make a
  decision, document it in a comment, and move on.
- Readable code > clever code. Well-named types/dataclasses are welcome.
- You're free to add files; the entrypoint stays `reconcile.py`.
- Questions about the brief? Ping Marina on chat — she replies fast.
