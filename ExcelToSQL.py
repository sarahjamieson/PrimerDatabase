import pandas as pd
import re
from CheckPrimers import CheckPrimers
from CheckSNPs import CheckSNPs
import sqlite3 as lite


class ExcelToSQL(object):
    """Extracts data from excel spread sheet and imports into a sqlite database.

        Note:
            The data extraction is split into three functions to create three separate, linked tables within the
            database.

        Args:
           :param excel_file: excel file to be imported.
           :param db: database the excel file should be imported into.
    """

    def __init__(self, excel_file, db):
        self.excel_file = excel_file
        self.db = db

    def get_cursor(self):
        """Creates a connection to the database.

           Returns:
               :return: con (connection) for commit in to_sql function.
               :return: curs (cursor) to execute SQL queries.
        """

        con = lite.connect(
            self.db)  # This will create the database if it doesn't already exist.
        curs = con.cursor()

        return curs, con

    def get_sheet_name(self):
        """Returns the sheetname to be used to import data from."""

        xl = pd.ExcelFile(self.excel_file)
        sheet_names = xl.sheet_names
        for item in sheet_names:
            if re.match("(.*)Current primers", item, re.IGNORECASE):  # Only extracts most recent primers
                sheet_name = item

        return sheet_name

    def get_primers(self):
        """Extracts and checks primer data from sheet.

           Returns:
               :return: df_primers data frame containing extracted data.
               :return: primer_faults, the number of total errors in the primer data.
        """

        sheet_name = self.get_sheet_name()

        df_primers = pd.read_excel(self.excel_file, header=0, parse_cols='A:E,G:M', skiprows=2,
                                   names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'M13_tag',
                                          'Batch_no', 'Batch_test_MS_project', 'Order_date', 'Frag_size', 'Anneal_temp',
                                          'Other_info'],
                                   sheetname=sheet_name, index_col=None)

        for col in ['Gene', 'Exon', 'Direction', 'Primer_seq']:
            df_primers[col] = df_primers[col].fillna(method='ffill')  # These fields usually contain merged cells.

        df_primers = df_primers.where((pd.notnull(df_primers)), None)  # Easier to check than NaN.

        # Needed if multiple SNPs are present.
        df_primers = df_primers.drop_duplicates(subset=['Gene', 'Exon', 'Direction'])

        primer_faults = sum(CheckPrimers(df_primers).check_all())

        return df_primers, primer_faults

    def get_gene_info(self):
        """Extracts gene and chromosome data from sheet.

           Returns:
               :return: gene_chrom, a list containing the gene name and chromosome associated with the file.
        """

        sheet_name = self.get_sheet_name()

        df_chrom = pd.read_excel(self.excel_file, skiprows=2, parse_cols='A,F', names=['Gene', 'Chrom'],
                                 sheetname=sheet_name)

        gene_name = df_chrom.at[0, 'Gene']
        chrom_no = df_chrom.at[0, 'Chrom']
        gene_chrom = gene_name, chrom_no

        return gene_chrom

    def get_snps(self):
        """Extracts and check SNP data from the sheet.

           Returns:
                :return: df_snps data frame containing extracted data.
                :return: snp_faults, the number of total errors in the SNP data.

        """

        sheet_name = self.get_sheet_name()

        df_snps = pd.read_excel(self.excel_file, header=0, parse_cols='A:C,O:X', skiprows=2,
                                names=['Gene', 'Exon', 'Direction', 'SNPCheck_build', 'Total_SNPs', 'dbSNP_rs', 'HGVS',
                                       'Frequency', 'ss_refs', 'ss_projects', 'Other_info', 'Action_required',
                                       'Checked_by'],
                                index_col=False, sheetname=sheet_name)

        for col in ['Gene', 'Exon', 'Direction']:
            df_snps[col] = df_snps[col].fillna(method='ffill')  # These fields usually contain merged cells.

        df_snps = df_snps.where((pd.notnull(df_snps)), None)  # Easier to check than NaN.
        snp_faults = sum(CheckSNPs(df_snps).check_all())

        return df_snps, snp_faults

    def to_sql(self):
        """Imports data into the database.

           Note:
               The data is only imported if no errors are found.
               The data is initially added to draft tables then inserted into the actual tables to allow addition of
               primary key columns (Primer_Id, Gene_Id, SNP_Id).
               Creating the tables is only required at the beginning; comment out the indicated lines thereafter.

        """

        curs, con = self.get_cursor()
        df_primers, primer_faults = self.get_primers()
        gene_chrom = self.get_gene_info()
        df_snps, snp_faults = self.get_snps()

        if primer_faults == 0 and snp_faults == 0:
            print "All checks complete with no errors"

            df_primers.to_sql('Draft_Primers', con, if_exists='replace', index=False)

            curs.execute("DROP TABLE IF EXISTS 'Primers'")  # Use first time only
            curs.execute(
                "CREATE TABLE Primers(Primer_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Gene TEXT, Exon TEXT, "
                "Direction TEXT, Version REAL, Primer_Seq TEXT, M13_Tag TEXT, Batch_No TEXT, "
                "Batch_Test_MS_Project TEXT, Order_Date TIMESTAMP, Fragment_Size REAL, Annealing_Temp TEXT, "
                "Other_Info TEXT)")  # Use first time only

            curs.execute("INSERT INTO Primers (Gene, Exon, Direction, Version, Primer_Seq, M13_Tag, Batch_No, "
                         "Batch_Test_MS_Project, Order_Date, Fragment_Size, Annealing_Temp, Other_Info) SELECT * FROM "
                         "Draft_Primers")
            curs.execute("DROP TABLE Draft_Primers")

            curs.execute("DROP TABLE IF EXISTS 'Draft_Genes'")
            curs.execute("CREATE TABLE Draft_Genes(Gene TEXT, Chromosome INT)")
            curs.execute("INSERT INTO Draft_Genes VALUES (?,?)", gene_chrom)

            curs.execute("DROP TABLE IF EXISTS Genes")  # Use first time only
            curs.execute("CREATE TABLE Genes(Gene_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Gene TEXT, "
                         "Chromosome INT)")  # Use first time only
            curs.execute("INSERT INTO Genes (Gene, Chromosome) SELECT * FROM Draft_Genes")
            curs.execute("DROP TABLE Draft_Genes")

            df_snps.to_sql('Draft_SNPs', con, if_exists='replace', index=False)

            curs.execute("DROP TABLE IF EXISTS 'SNPs'")  # Use first time only
            curs.execute("CREATE TABLE SNPs(SNP_Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Gene TEXT, Exon TEXT, "
                         "Direction TEXT, SNPCheck_Build REAL, Total_SNPs INT, dbSNP_rs TEXT, HGVS TEXT, "
                         "Frequency TEXT, ss_refs TEXT, ss_Projects TEXT, Other_Info TEXT, Action_Required TEXT, "
                         "Checked_By TEXT)")  # Use first time only
            curs.execute("INSERT INTO SNPs (Gene, Exon, Direction, SNPCheck_Build, Total_SNPs, dbSNP_rs, HGVS, "
                         "Frequency, ss_refs, ss_Projects, Other_Info, Action_Required, Checked_By) SELECT * FROM "
                         "Draft_SNPs")
            curs.execute("DROP TABLE Draft_SNPs")

            con.commit()

        else:
            print "Errors must be fixed before adding to database"

