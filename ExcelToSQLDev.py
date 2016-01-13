import pandas as pd
import re
from CheckPrimers import CheckPrimers
from CheckSNPs import CheckSNPs
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

        df_primers = df_primers.where((pd.notnull(df_primers)), None)
        df_primers = df_primers.drop_duplicates(subset=['Gene', 'Exon', 'Direction'])

        primer_faults = sum(CheckPrimers(df_primers).check_all())

        return df_primers, primer_faults

    def get_gene_info(self):
        sheet_name = self.get_sheet_name()

        df_chrom = pd.read_excel(self.excel_file, skiprows=2, parse_cols='A,F', names=['Gene', 'Chrom'],
                                 sheetname=sheet_name)

        gene_name = df_chrom.at[0, 'Gene']
        chrom_no = df_chrom.at[0, 'Chrom']
        gene_chrom = gene_name, chrom_no

        return gene_chrom

    def get_snps(self):
        sheet_name = self.get_sheet_name()

        df_snps = pd.read_excel(self.excel_file, header=0, parse_cols='A:C,O:X', skiprows=2,
                                names=['Gene', 'Exon', 'Direction', 'SNPCheck_build', 'Total_SNPs', 'dbSNP_rs', 'HGVS',
                                       'Frequency', 'ss_refs', 'ss_projects', 'Other_info', 'Action_required',
                                       'Checked_by'],
                                index_col=False, sheetname=sheet_name)

        for col in ['Gene', 'Exon', 'Direction']:
            df_snps[col] = df_snps[col].fillna(
                method='ffill')  # forward fills empty cells (deals with merged cells) but for specified columns only

        df_snps = df_snps.where((pd.notnull(df_snps)), None)

        snps_er, rs_er, hgvs_er = CheckSNPs(df_snps).check_all()
        snp_faults = snps_er + rs_er + hgvs_er

        return df_snps, snp_faults

    def to_sql(self):
        curs, con = self.get_cursor()
        df_primers, primer_faults = self.get_primers()
        gene_chrom = self.get_gene_info()
        df_snps, snp_faults = self.get_snps()

        if primer_faults == 0 and snp_faults == 0:
            print "All checks complete with no errors"

            df_primers.to_sql('Draft_Primers', con, if_exists='replace', index=False)

            curs.execute("DROP TABLE IF EXISTS 'Primers'")  # use first time only
            curs.execute(
                "CREATE TABLE Primers(Primer_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Gene TEXT, Exon TEXT, "
                "Direction TEXT, Version REAL, Primer_Seq TEXT, M13_Tag TEXT, Batch_No TEXT, "
                "Batch_Test_MS_Project TEXT, Order_Date TIMESTAMP, Fragment_Size REAL, Annealing_Temp TEXT, "
                "Other_Info TEXT)")  # run first time only

            curs.execute("INSERT INTO Primers (Gene, Exon, Direction, Version, Primer_Seq, M13_Tag, Batch_No, "
                         "Batch_Test_MS_Project, Order_Date, Fragment_Size, Annealing_Temp, Other_Info) SELECT * FROM "
                         "Draft_Primers")
            curs.execute("DROP TABLE Draft_Primers")

            curs.execute("DROP TABLE IF EXISTS 'Draft_Genes'")
            curs.execute("CREATE TABLE Draft_Genes(Gene TEXT, Chromosome INT)")
            curs.execute("INSERT INTO Draft_Genes VALUES (?,?)", gene_chrom)

            curs.execute("DROP TABLE IF EXISTS Genes")  # use first time only
            curs.execute("CREATE TABLE Genes(Gene_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Gene TEXT, "
                         "Chromosome INT)")  # use first time only
            curs.execute("INSERT INTO Genes (Gene, Chromosome) SELECT * FROM Draft_Genes")
            curs.execute("DROP TABLE Draft_Genes")

            df_snps.to_sql('Draft_SNPs', con, if_exists='replace', index=False)

            curs.execute("DROP TABLE IF EXISTS 'SNPs'")  # use first time only
            curs.execute("CREATE TABLE SNPs(SNP_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Gene TEXT, Exon TEXT, "
                         "Direction TEXT, SNPCheck_Build REAL, Total_SNPs INT, dbSNP_rs TEXT, HGVS TEXT, "
                         "Frequency TEXT, ss_refs TEXT, ss_Projects TEXT, Other_Info TEXT, Action_Required TEXT, "
                         "Checked_By TEXT)")  # use first time only
            curs.execute("INSERT INTO SNPs (Gene, Exon, Direction, SNPCheck_Build, Total_SNPs, dbSNP_rs, HGVS, "
                         "Frequency, ss_refs, ss_Projects, Other_Info, Action_Required, Checked_By) SELECT * FROM "
                         "Draft_SNPs")
            curs.execute("DROP TABLE Draft_SNPs")

            con.commit()

        else:
            print "Errors must be fixed before adding to database"
