import sqlite3 as lite
import pandas as pd
import re
import numpy as np

con = lite.connect('test.db')
curs = con.cursor()
excel_file = 'CHARGE_CHD7.xlsx'

xl = pd.ExcelFile(excel_file)
sheet_names = xl.sheet_names
for item in sheet_names:
    if re.match("(.*)Current primers", item, re.IGNORECASE):
        sheet_name = item

df_primers = pd.read_excel(excel_file, header=0, parse_cols='A:E,G:M', skiprows=2, names=['Gene', 'Exon', 'Direction',
                                                                                          'Version_no', 'Primer_seq',
                                                                                          'M13_tag', 'Batch_no',
                                                                                          'Batch_test_MS_project',
                                                                                          'Order_date', 'Frag_size',
                                                                                          'Anneal_temp', 'Other_info'],
                           sheetname=sheet_name, index_col=None)

df_primers = df_primers.where((pd.notnull(df_primers)), None)

primer_list = []
names = []
for row_index, row in df_primers.iterrows():
    if row['Primer_seq'] is not None:
        primer_list.append(str(row['Primer_seq']))
    if row['Exon'] is not None:
        names.append(str(row['Exon']))

forwards = primer_list[::2]
reverses = primer_list[1::2]

position = 0
primer_seqs = pd.DataFrame([])
while position < len(forwards):
    ser = pd.Series([names[position], forwards[position], reverses[position]])
    primer_seqs = primer_seqs.append(ser, ignore_index=True)
    position += 1

print primer_seqs

primer_seqs.to_csv('primerseqs.csv', header=None, index=None, sep='\t')






