"""Invoice reconciler tests — run with: python3 -m unittest discover -s tests -v"""
import os
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import reconcile  # noqa: E402

FIX = ROOT / "fixtures"


class TestParseMoney(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(reconcile._parse_money("1250.90"), Decimal("1250.90"))

    def test_grouping(self):
        self.assertEqual(reconcile._parse_money("1,250,999.00"), Decimal("1250999.00"))

    def test_dollar_prefix(self):
        self.assertEqual(reconcile._parse_money("$ 872.55"), Decimal("872.55"))


class TestLoaders(unittest.TestCase):
    def test_invoices(self):
        invoices = reconcile.load_invoices(str(FIX / "invoices.csv"))
        self.assertEqual(len(invoices), 5)
        self.assertEqual(invoices[0].number, "0001")
        self.assertEqual(invoices[0].amount, Decimal("1250.90"))

    def test_payments(self):
        payments = reconcile.load_payments(str(FIX / "payments.csv"))
        self.assertEqual(len(payments), 6)
        self.assertEqual(payments[0].ref, "P-9821")


class TestReconcile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.invoices = reconcile.load_invoices(str(FIX / "invoices.csv"))
        cls.payments = reconcile.load_payments(str(FIX / "payments.csv"))
        cls.res = reconcile.reconcile(cls.invoices, cls.payments)

    def test_every_invoice_present(self):
        self.assertEqual(set(self.res), {"0001", "0002", "0003", "0004", "0005"})

    def test_statuses(self):
        esperado = {
            "0001": "MATCHED",
            "0002": "MISMATCH",
            "0003": "MATCHED",
            "0004": "PENDING",
            "0005": "DUPLICATED",
        }
        for numero, status in esperado.items():
            self.assertEqual(self.res[numero]["status"], status, f"invoice {numero}")

    def test_duplicate_counts_once(self):
        self.assertEqual(self.res["0005"]["received"], Decimal("1000.00"))

    def test_pending_received_zero(self):
        self.assertEqual(self.res["0004"]["received"], Decimal("0.00"))

    def test_installments_sum(self):
        self.assertEqual(self.res["0003"]["received"], Decimal("872.55"))


class TestFormat(unittest.TestCase):
    def test_format_basic(self):
        self.assertEqual(reconcile.format_money(Decimal("1250.90")), "1,250.90")

    def test_format_grouping(self):
        self.assertEqual(reconcile.format_money(Decimal("1250990")), "1,250,990.00")

    def test_format_zero(self):
        self.assertEqual(reconcile.format_money(Decimal("0")), "0.00")

    def test_report_matches_fixture(self):
        invoices = reconcile.load_invoices(str(FIX / "invoices.csv"))
        payments = reconcile.load_payments(str(FIX / "payments.csv"))
        texto = reconcile.build_report(reconcile.reconcile(invoices, payments))
        esperado = (FIX / "expected_report.txt").read_text(encoding="utf-8").strip()
        self.assertEqual(texto.strip(), esperado)


class TestCLI(unittest.TestCase):
    def test_cli_writes_out(self):
        tmp = FIX / "_report_test.txt"
        env = dict(os.environ, PYTHONPATH=str(ROOT))
        proc = subprocess.run(
            [sys.executable, str(ROOT / "reconcile.py"),
             "--invoices", str(FIX / "invoices.csv"),
             "--payments", str(FIX / "payments.csv"),
             "--out", str(tmp)],
            capture_output=True, text=True, env=env, cwd=str(ROOT),
        )
        self.addCleanup(tmp.unlink, missing_ok=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        conteudo = tmp.read_text(encoding="utf-8").strip()
        esperado = (FIX / "expected_report.txt").read_text(encoding="utf-8").strip()
        self.assertEqual(conteudo, esperado)


if __name__ == "__main__":
    unittest.main()
