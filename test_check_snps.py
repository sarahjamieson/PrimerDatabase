import unittest
from excel_to_sql_dev import ExcelToSQL
from check_snps import CheckSNPs


class TestCheckSNPs(unittest.TestCase):
    def setUp(self):
        self.ets = ExcelToSQL('TestCS_COL4A5.xlsx', 'Test.db')
        df_snps, snp_faults = self.ets.get_snps()
        self.cs = CheckSNPs(df_snps)

    def test_check_no_snps(self):
        checks = self.cs.check_no_snps()
        self.assertEqual(checks, 2)

    def test_check_rs(self):
        checks = self.cs.check_rs()
        self.assertEqual(checks, 3)

    def test_check_hgvs(self):
        checks = self.cs.check_hgvs()
        self.assertEqual(checks, 2)

    def test_check_all(self):
        self.assertEqual(len(self.cs.check_all()), 3)

