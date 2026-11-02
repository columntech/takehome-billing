#!/usr/bin/env python3
"""Invoice reconciliation tool — Column take-home.

Cross-references issued invoices (CSV) with received payments (CSV) and produces
a per-invoice status report using only the Python standard library.

Usage:
    python3 reconcile.py --invoices fixtures/invoices.csv \
                         --payments fixtures/payments.csv \
                         --out report.txt
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List


@dataclass(frozen=True)
class Invoice:
    number: str
    amount: Decimal


@dataclass(frozen=True)
class Payment:
    invoice: str
    ref: str
    amount: Decimal


def _parse_money(text: str) -> Decimal:
    """Converts a US-style amount ('1,250.90' or '$1,250.90') into Decimal('1250.90')."""
    limpo = text.strip().replace("$", "", 1).replace(" ", "")
    limpo = limpo.replace(",", "")
    return Decimal(limpo)


def load_invoices(path: str) -> List[Invoice]:
    """Reads the invoices CSV (';' separator, header 'number;amount')."""
    raise NotImplementedError


def load_payments(path: str) -> List[Payment]:
    """Reads the payments CSV (';' separator, header 'invoice;ref;amount')."""
    raise NotImplementedError


def reconcile(invoices: List[Invoice], payments: List[Payment]) -> Dict[str, dict]:
    """Cross-references both lists.

    Returns {invoice_number: {"status": ..., "expected": Decimal, "received": Decimal}}
    for every invoice (including pending ones). A repeated ref counts once and
    forces the DUPLICATED status.
    """
    raise NotImplementedError


def format_money(value: Decimal) -> str:
    """Decimal -> '1,250.90' (US grouping ',', decimal '.', always 2 places)."""
    raise NotImplementedError


def build_report(results: Dict[str, dict]) -> str:
    """Assembles the final report: one line per invoice, sorted by number.

    Line format: INVOICE {number} | {status} | expected {amount} | received {amount}
    """
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconciles issued invoices with received payments."
    )
    parser.add_argument("--invoices", required=True, help="invoices CSV (;)")
    parser.add_argument("--payments", required=True, help="payments CSV (;)")
    parser.add_argument("--out", default=None, help="output file (default: stdout)")
    args = parser.parse_args()

    invoices = load_invoices(args.invoices)
    payments = load_payments(args.payments)
    texto = build_report(reconcile(invoices, payments))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(texto + "\n")
        print(f"report written to {args.out}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
