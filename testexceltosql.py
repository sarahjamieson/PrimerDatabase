import unittest
from exceltosqldev import ExcelToSQL
import pandas as pd


class TestExcelToSQL(unittest.TestCase):
    def setUp(self):
        self.ets = ExcelToSQL('TestETS_COL4A5.xlsx', 'Test.db')
        self.sheet_name = self.ets.get_sheet_name()
        self.df_primers, self.primer_faults = self.ets.get_primers()
        self.df_snps, self.snp_faults = self.ets.get_snps()
        self.curs, self.con = self.ets.get_cursor()

    def test_get_sheet_name(self):
        self.assertIsNotNone(self.sheet_name, msg="Sheet_name is empty")  # tests sheetname has been obtained
        self.assertIn('Current primers', self.sheet_name, msg="Selected sheetname does not contain 'Current primers'")

    def test_get_primers(self):
        self.assertIsInstance(self.primer_faults, int, msg="No of primer_faults is not an integer")
        self.assertIsInstance(self.df_primers, pd.DataFrame, msg="df_primers is not a data frame")
        self.assertEqual(len(self.df_primers), 84, msg="Incorrect number of rows")
        self.assertEqual(len(self.df_primers.columns), 12, msg="Incorrect number of columns")
        self.assertEqual(str(self.df_primers.iat[8, 4]), 'GTGCAATGAAGACAATGCTCC', "Entry does not match predicted")

    def test_get_snps(self):
        self.assertIsInstance(self.snp_faults, int, msg="No of snp_faults is not an integer")
        self.assertIsInstance(self.df_snps, pd.DataFrame, msg="df_snps is not a data frame")
        self.assertEqual(len(self.df_snps), 92, msg="Incorrect number of rows")
        self.assertEqual(len(self.df_snps.columns), 13, msg="Incorrect number of columns")
        self.assertEqual(str(self.df_snps.iat[2, 6]), 'c.82-82T>C')

    def test_to_sql(self):
        self.ets.to_sql()

        self.curs.execute("SELECT * FROM 'Primers'")
        primer_result = self.curs.fetchone()
        self.assertIsNotNone(primer_result, msg="Primers table is empty")

        self.curs.execute("SELECT * FROM 'Genes'")
        gene_result = self.curs.fetchone()
        self.assertIsNotNone(gene_result, msg="Genes table is empty")

        self.curs.execute("SELECT * FROM 'SNPs'")
        snp_result = self.curs.fetchone()
        self.assertIsNotNone(snp_result, msg="SNPs table is empty")



