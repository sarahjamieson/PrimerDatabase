import pandas as pd
import sqlite3 as lite

con = lite.connect('test.db')  # Makes a connection to the test.db database if present, creates test.db if not.
curs = con.cursor()
excel_file = 'primer_batch_records.xlsx'

curs.execute('DROP TABLE IF EXISTS Genes')
curs.execute('DROP TABLE IF EXISTS Primers')

# Takes an excel document, pulls data from specified columns and names those columns.
df_primers = pd.read_excel(excel_file, header=0, skiprows=2, parse_cols='A:C,E,G,I:K',
                           names=['Gene_name', 'Exon', 'Direction', 'Primer_seq', 'M13_tag?', 'Frag_size',
                                  'Anneal_temp', 'Other info'], index_col=False)

# Changes the index column from "Index" to "Primer_Id"
df_primers.index.names = ['Primer_Id']

# Converts excel data into SQLite table
df_primers.to_sql('Primers', con, if_exists='replace')

df_chrom = pd.read_excel(excel_file, header=0, skiprows=2, parse_cols='A,F', names=['Gene_name', 'Chrom'],
                         index_col=False)

# Gets gene_name and chromosome_number from data
gene_name = df_chrom.at[0, 'Gene_name']
chrom_no = int(df_chrom.at[0, 'Chrom'])

# Creates a table containing the gene_name and chromosome_number corresponding to the file.
curs.execute("CREATE TABLE Genes(Gene_name TEXT PRIMARY KEY, Chromosome_no INT)")
pairing = [gene_name, chrom_no]
curs.execute("INSERT INTO Genes VALUES (?,?)", pairing)
con.commit()

