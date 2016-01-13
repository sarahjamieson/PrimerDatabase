import unittest
from ExcelToSQLDev import ExcelToSQL
from CheckPrimers import CheckPrimers


class TestCheckPrimers(unittest.TestCase):
    def setUp(self):
        self.ets = ExcelToSQL('TestCP_COL4A5.xlsx', 'Test.db')
        df_primers, primer_faults = self.ets.get_primers()
        self.cp = CheckPrimers(df_primers)

    def test_check_gene(self):
        checks = self.cp.check_gene()
        self.assertEqual(checks, 8)

    def test_check_exon(self):
        checks = self.cp.check_exon()
        self.assertEqual(checks, 4)

    def test_check_direction(self):
        checks = self.cp.check_direction()
        self.assertEqual(checks, 2)

    def test_check_version(self):
        checks = self.cp.check_version()
        self.assertEqual(checks, 1)

    def test_check_seq(self):
        checks = self.cp.check_seq()
        self.assertEqual(checks, 3)

    def test_check_tag(self):
        checks = self.cp.check_tag()
        self.assertEqual(checks, 2)

    def test_check_batch(self):
        checks = self.cp.check_batch()
        self.assertEqual(checks, 4)

    def test_check_dates(self):
        checks = self.cp.check_dates()
        self.assertEqual(checks, 1)

    def test_check_frag_size(self):
        checks = self.cp.check_frag_size()
        self.assertEqual(checks, 2)

    def test_check_anneal_temp(self):
        checks = self.cp.check_anneal_temp()
        self.assertEqual(checks, 1)

    def test_check_all(self):
        self.assertEqual(len(self.cp.check_all()), 10)