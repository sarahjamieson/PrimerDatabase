import pandas as pd
import sqlite3 as lite

con = lite.connect('test.db')  # Makes a connection to the test.db database if present, creates test.db if not.
curs = con.cursor()  # Grabs the cursor for SQLite queries later on.
excel_file = 'primer_batch_records.xlsx'


# Pulls data from specific columns in excel file and adds to SQLite table "Primers" in test database.
def get_primers():
    curs.execute('DROP TABLE IF EXISTS Primers')

    df_primers = pd.read_excel(excel_file, header=0, skiprows=2, parse_cols='A:C,E,G,I:K',
                               names=['Gene_name', 'Exon', 'Direction', 'Primer_seq', 'M13_tag?', 'Frag_size',
                                      'Anneal_temp', 'Other info'],
                               index_col=False)

    df_primers.index.names = ['Primer_Id']  # Changes index title from "Index" to "Primer_Id" to act as primary key.

    df_primers = df_primers.fillna(method='ffill')  # overcomes issues with merged cells; forward fills data if NaN.

    df_primers.to_sql('Primers', con, if_exists='replace')  # creates SQL table from data


# Pulls gene and chromosome info from excel file and adds to SQLite table "Genes" in test database.
def get_gene_info():
    curs.execute('DROP TABLE IF EXISTS Genes')
    df_chrom = pd.read_excel(excel_file, header=0, skiprows=2, parse_cols='A,F', names=['Gene_name', 'Chrom'],
                             index_col=False)

    gene_name = df_chrom.at[0, 'Gene_name']
    chrom_no = int(df_chrom.at[0, 'Chrom'])
    gene_chrom = [gene_name, chrom_no]

    curs.execute("CREATE TABLE Genes(Gene_name TEXT PRIMARY KEY, Chromosome_no INT)")
    curs.execute("INSERT INTO Genes VALUES (?,?)", gene_chrom)
    con.commit()


def get_snps():
    curs.execute('DROP TABLE IF EXISTS SNPs')

    df_snps = pd.read_excel(excel_file, header=0, skiprows=2, parse_cols='M:V',
                            names=['SNPCheck_build', 'Total_SNPs', 'dbSNP_rs', 'HGVS', 'Frequency', 'ss_refs',
                                   'ss_projects', 'Other_info', 'Action_taken', 'Checked_by'],
                            index_col=False)

    df_snps.index.names = ['SNP_Id']  # Changes index title from "Index" to "Primer_Id" to act as primary key.

    df_snps.to_sql('SNPs', con, if_exists='replace')  # creates SQL table from data


get_primers()
get_gene_info()
get_snps()