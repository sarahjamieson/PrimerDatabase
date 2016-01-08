import pandas as pd
import re
from CheckFields import CheckFields
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
        curs, con = self.get_cursor()  # split up tuple returned by function so only con can be used.

        df_primers = pd.read_excel(self.excel_file, header=0, parse_cols='A:E,G:M', skiprows=2,
                                   names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'M13_tag',
                                          'Batch_no',
                                          'Batch_test_MS_project', 'Order_date', 'Frag_size', 'Anneal_temp',
                                          'Other info'],
                                   sheetname=sheet_name, index_col=None)

        df_primers = df_primers.fillna(method='ffill')  # forward fills empty cells (deals with merged cells)
        df_primers = df_primers.where((pd.notnull(df_primers)), None)
        df_primers = df_primers.drop_duplicates()
        df_primers = df_primers.reset_index()
        del df_primers['index']
        df_primers.index.names = ['Primer_Id']  # Changes index title from "Index" to "Primer_Id".

        check = CheckFields(df_primers)
        check.get_all()

        df_primers.to_sql('Primers', con, if_exists='append')

    def get_gene_info(self):
        curs, con = self.get_cursor()
        sheet_name = self.get_sheet_name()

        # curs.execute("DROP TABLE IF EXISTS 'Genes'")  # for testing only

        df_chrom = pd.read_excel(self.excel_file, skiprows=2, parse_cols='A,F', names=['Gene', 'Chrom'],
                                 sheetname=sheet_name)

        gene_name = df_chrom.at[0, 'Gene']
        chrom_no = df_chrom.at[0, 'Chrom']
        gene_chrom = [gene_name, chrom_no]

        # curs.execute("CREATE TABLE Genes(Gene TEXT PRIMARY KEY, Chromosome_no INT)")  # only use this the first time
        curs.execute("INSERT INTO Genes VALUES (?,?)", gene_chrom)
        con.commit()

    def get_snps(self):
        curs, con = self.get_cursor()
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

        df_snps.to_sql('SNPs', con, if_exists='append')  # Creates SQL table from data

    def get_all(self):
        self.get_cursor()
        self.get_sheet_name()
        self.get_primers()
        self.get_gene_info()
        self.get_snps()
