import pandas as pd
import sqlite3 as lite
from CheckFields import CheckFields
import re

con = lite.connect('Primer_v1.db')  # Makes a connection to the test.db database if present, creates test.db if not.
curs = con.cursor()  # Grabs the cursor for SQLite queries later on.
excel_file = 'CHARGE_CHD7.xlsx'
xl = pd.ExcelFile(excel_file)
sheet_names = xl.sheet_names
for item in sheet_names:
    if re.match("(.*)Current primers", item, re.IGNORECASE):
        sheet_name = item


# Pulls data from specific columns in excel file and adds to SQLite table "Primers" in test database.
def get_primers():
    curs.execute('DROP TABLE IF EXISTS Primers')  # only include this for testing code

    df_primers = pd.read_excel(excel_file, header=0, parse_cols='A:E,G:M', skiprows=2,
                               names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'M13_tag', 'Batch_no',
                                      'Batch_test_MS_project', 'Order_date', 'Frag_size', 'Anneal_temp', 'Other info'],
                               sheetname=sheet_name)

    df_primers.index.names = ['Primer_Id']  # Changes index title from "Index" to "Primer_Id" to act as primary key.

    df_primers = df_primers.fillna(method='ffill')  # Overcomes issues with merged cells; forward fills data if NaN.

    df_primers_modified = df_primers.where((pd.notnull(df_primers)), None)

    print df_primers_modified

    check = CheckFields(df_primers_modified)
    check.check_special()
    check.check_nucs()
    check.check_direction()
    check.check_fragments()
    check.check_version()
    check.check_anneal()

    df_primers_modified.to_sql('Primers', con, if_exists='append')  # Creates SQL table from data


# Pulls gene and chromosome info from excel file and adds to SQLite table "Genes" in test database.
def get_gene_info():
    curs.execute('DROP TABLE IF EXISTS Genes')  # only include this for testing code
    df_chrom = pd.read_excel(excel_file, skiprows=2, parse_cols='A,F', names=['Gene', 'Chrom'], sheetname=sheet_name)

    gene_name = df_chrom.at[0, 'Gene']
    chrom_no = int(df_chrom.at[0, 'Chrom'])
    gene_chrom = [gene_name, chrom_no]

    curs.execute("CREATE TABLE Genes(Gene TEXT PRIMARY KEY, Chromosome_no INT)")  # only use this the first time
    curs.execute("INSERT INTO Genes VALUES (?,?)", gene_chrom)
    con.commit()


def get_snps():
    curs.execute('DROP TABLE IF EXISTS SNPs')  # only include this for testing code

    df_snps = pd.read_excel(excel_file, header=0, parse_cols='O:X', skiprows=2,
                            names=['SNPCheck_build', 'Total_SNPs', 'dbSNP_rs', 'HGVS', 'Frequency', 'ss_refs',
                                   'ss_projects', 'Other_info', 'Action_required', 'Checked_by'],
                            index_col=False, sheetname=sheet_name)

    df_snps.index.names = ['SNP_Id']  # Changes index title from "Index" to "SNP_Id" to act as primary key.

    df_snps = df_snps.fillna(method='ffill')

    df_snps.to_sql('SNPs', con, if_exists='append')  # Creates SQL table from data


get_primers()
get_gene_info()
get_snps()
