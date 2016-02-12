import pandas as pd
import re
import os


class GetCoordinates(object):
    def __init__(self, excel_file):
        self.excel_file = excel_file

    def get_sheet_name(self):
        xl = pd.ExcelFile(self.excel_file)
        sheet_names = xl.sheet_names
        for item in sheet_names:
            if re.match("(.*)Current primers", item, re.IGNORECASE):
                sheet_name = item
        return sheet_name

    def get_primers(self):
        sheet_name = self.get_sheet_name()
        df_primers = pd.read_excel(self.excel_file, header=0, parse_cols='A:M', skiprows=2,
                                   names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'Chrom', 'M13_tag',
                                          'Batch_no', 'Batch_test_MS_project', 'Order_date', 'Frag_size', 'Anneal_temp',
                                          'Other_info'],
                                   sheetname=sheet_name, index_col=None)

        df_primers = df_primers.where((pd.notnull(df_primers)), None)
        df_primers = df_primers.drop_duplicates(subset=('Gene', 'Exon', 'Direction', 'Chrom'))
        return df_primers

    def make_csv(self):
        df_primers = self.get_primers()
        primer_list = []
        names_dup = []
        names = []

        for row_index, row in df_primers.iterrows():
            primer_list.append(str(row['Primer_seq']))
            names_dup.append(str(row['Gene']) + "_" + str(row['Exon']) + "_" + str(row['Direction']))
            for item in names_dup:
                if item not in names:
                    names.append(item)

        forwards = primer_list[::2]
        reverses = primer_list[1::2]

        list_position = 0
        primer_seqs = pd.DataFrame([])
        while list_position < len(forwards):
            ser = pd.Series([names[list_position], forwards[list_position], reverses[list_position]])
            primer_seqs = primer_seqs.append(ser, ignore_index=True)
            list_position += 1

        primer_seqs.to_csv('primerseqs.csv', header=None, index=None, sep='\t')

    def run_pcr(self):
        chromosomes = ['chr10.2bit', 'chr11.2bit', 'chr12.2bit', 'chr1.2bit', 'chr13.2bit', 'chr14.2bit', 'chr15.2bit',
                       'chr16.2bit', 'chr17.2bit', 'chr18.2bit', 'chr19.2bit', 'chr20.2bit', 'chr21.2bit', 'chr22.2bit',
                       'chr2.2bit', 'chr3.2bit', 'chr4.2bit', 'chr5.2bit', 'chr6.2bit', 'chr7.2bit', 'chr8.2bit',
                       'chr9.2bit', 'chrX.2bit', 'chrY.2bit']

        for chr in chromosomes:
            os.system(
                "/opt/kentools/isPcr -out=psl /media/genomicdata/ucsc_hg19_by_chr/2bit_chr/%s \
                primerseqs.csv %s.tmp.psl" % (chr, chr[:-5]))

            chrfile = "%s.tmp.psl" % chr[:-5]

            if os.path.getsize(chrfile) != 0:
                os.system("/opt/kentools/pslToBed %s.tmp.psl coords.tmp.bed" % chr[:-5])
            else:
                os.system("rm %s.tmp.psl" % chr[:-5])

    def get_all(self):
        self.get_sheet_name()
        self.get_primers()
        self.make_csv()
        self.run_pcr()
