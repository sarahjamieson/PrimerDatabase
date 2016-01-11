import pandas as pd
import re
from CheckPrimers import CheckPrimers
import sqlite3 as lite


class ExcelToSQL(object):
    def __init__(self, excel_file, db):
        self.excel_file = excel_file
        self.db = db

    def get_cursor(self):
        con = lite.connect(
            self.db)  # Makes a connection to the test.db database if present, creates test.db if not.
        curs = con.cursor()

        return curs, con  # returns multiple variables (tuple)

    def get_sheet_name(self):
        xl = pd.ExcelFile(self.excel_file)
        sheet_names = xl.sheet_names
        for item in sheet_names:
            if re.match("(.*)Current primers", item, re.IGNORECASE):
                sheet_name = item

        return sheet_name

    def get_primers(self):
        sheet_name = self.get_sheet_name()

        df_primers = pd.read_excel(self.excel_file, header=0, parse_cols='A:E,G:M', skiprows=2,
                                   names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'M13_tag',
                                          'Batch_no', 'Batch_test_MS_project', 'Order_date', 'Frag_size', 'Anneal_temp',
                                          'Other_info'],
                                   sheetname=sheet_name, index_col=None)

        for col in ['Gene', 'Exon', 'Direction', 'Primer_seq']:
            df_primers[col] = df_primers[col].fillna(method='ffill')

        for col in ['Frag_size', 'Anneal_temp', 'Other_info']:
            df_primers[col] = df_primers[col].fillna(method='ffill', limit=1)

        df_primers = df_primers.where((pd.notnull(df_primers)), None)
        df_primers = df_primers.drop_duplicates()
        df_primers = df_primers.reset_index()
        del df_primers['index']

        check = CheckPrimers(df_primers)
        check.check_all()

        return df_primers

    def get_gene_info(self):
        sheet_name = self.get_sheet_name()

        df_chrom = pd.read_excel(self.excel_file, skiprows=2, parse_cols='A,F', names=['Gene', 'Chrom'],
                                 sheetname=sheet_name)

        gene_name = df_chrom.at[0, 'Gene']
        chrom_no = df_chrom.at[0, 'Chrom']
        gene_chrom = [gene_name, chrom_no]

        return gene_chrom

    def get_snps(self):
        sheet_name = self.get_sheet_name()

        df_snps = pd.read_excel(self.excel_file, header=0, parse_cols='A:C,O:X', skiprows=2,
                                names=['Gene', 'Exon', 'Direction', 'SNPCheck_build', 'Total_SNPs', 'dbSNP_rs', 'HGVS',
                                       'Frequency', 'ss_refs', 'ss_projects', 'Other_info', 'Action_required',
                                       'Checked_by'],
                                index_col=False, sheetname=sheet_name)

        df_snps.index.names = ['SNP_Id']  # Changes index title from "Index" to "SNP_Id" to act as primary key.

        for col in ['Gene', 'Exon', 'Direction']:
            df_snps[col] = df_snps[col].fillna(
                method='ffill')  # forward fills empty cells (deals with merged cells) but for specified columns only

        return df_snps

    def to_sql(self):
        curs, con = self.get_cursor()
        df_primers = self.get_primers()
        gene_chrom = self.get_gene_info()
        df_snps = self.get_snps()

        df_primers.to_sql('Primers', con, if_exists='replace')

        curs.execute("DROP TABLE IF EXISTS 'Genes'")  # for testing only
        curs.execute("CREATE TABLE Genes(Gene TEXT PRIMARY KEY, Chromosome_no INT)")  # only use this the first time
        curs.execute("INSERT INTO Genes VALUES (?,?)", gene_chrom)
        con.commit()

        df_snps.to_sql('SNPs', con, if_exists='replace')
