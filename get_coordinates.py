import sqlite3 as lite
import pandas as pd
import re
import pybedtools as bed
import os

con = lite.connect('test.db')
curs = con.cursor()
excel_file = 'Alport_example.xlsx'

xl = pd.ExcelFile(excel_file)
sheet_names = xl.sheet_names
for item in sheet_names:
    if re.match("(.*)Current primers", item, re.IGNORECASE):
        sheet_name = item

df_primers = pd.read_excel(excel_file, header=0, parse_cols='A:M', skiprows=2,
                           names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'Chrom', 'M13_tag',
                                  'Batch_no', 'Batch_test_MS_project', 'Order_date', 'Frag_size', 'Anneal_temp',
                                  'Other_info'],
                           sheetname=sheet_name, index_col=None)

df_primers = df_primers.where((pd.notnull(df_primers)), None)

df_primers = df_primers.drop_duplicates(subset=('Gene', 'Exon', 'Direction', 'Chrom'))

primer_list = []
exons = []
exons2 = []
genes = []
chroms = []
directions = []
names = []

for row_index, row in df_primers.iterrows():
    primer_list.append(str(row['Primer_seq']))
    exons.append(str(row['Exon']))
    genes.append(str(row['Gene']))
    chroms.append("chr" + str(row['Chrom']))
    directions.append(str(row['Direction']))
    names.append(str(row['Gene']) + "_" + str(row['Exon']) + "_" + str(row['Direction']))

for item in exons:
    if item not in exons2:
        exons2.append(item)

gene_name = df_primers.at[0, 'Gene']

forwards = primer_list[::2]

reverses = primer_list[1::2]

position = 0
primer_seqs = pd.DataFrame([])
while position < len(forwards):
    ser = pd.Series([exons2[position], forwards[position], reverses[position]])
    primer_seqs = primer_seqs.append(ser, ignore_index=True)
    position += 1

primer_seqs.to_csv('primerseqs.csv', header=None, index=None, sep='\t')

tool = bed.BedTool('coords.tmp.bed')

start_coords = []
end_coords = []

seq_position = 0
for row in tool:
    start_coords.append(row.start)
    end_coords.append(row.start + len(primer_list[seq_position]))
    end_coords.append(row.end)
    start_coords.append(row.end - len(primer_list[seq_position + 1]))
    seq_position += 1

coords_df = pd.DataFrame([])
coords_df.insert(0, 'Gene', genes)
coords_df.insert(1, 'Chromosome', chroms)
coords_df.insert(2, 'Exon', exons)
coords_df.insert(3, 'Direction', directions)
coords_df.insert(4, 'Sequence', primer_list)
coords_df.insert(5, 'Start', start_coords)
coords_df.insert(6, 'End', end_coords)
coords_df.insert(7, 'name', names)

output_df = pd.DataFrame([])
output_df.insert(0, 'chrom', chroms)
output_df.insert(1, 'start', start_coords)
output_df.insert(2, 'end', end_coords)
output_df.insert(3, 'name', names)

print output_df

output_df.to_csv('final.csv', header=None, index=None, sep='\t')
final = bed.BedTool('final.csv')
final.saveas('final2.bed')


'''
for row in tool:
    start_coords.append(row.start)
    end_coords.append(row.end)

coords_df = pd.DataFrame([])

primer_seqs.insert(4, '4', start_ser)
primer_seqs.insert(5, '5', end_coords)
primer_seqs.insert(1, '1', chroms)

columns_labels = ('Gene', 'Chromosome', 'Exon', 'Forward', 'Reverse', 'Start', 'End')
writer = pd.ExcelWriter('%s_updated_batch_records.xlsx' % gene_name)
primer_seqs.to_excel(writer, sheet_name='Current primers', header=columns_labels, index=False)
writer.save()

'''

os.system("mv /home/cuser/PycharmProjects/PrimerDatabase/final2.bed /media/sf_sarah_share")

