import pandas as pd
import os
import pybedtools as bed


class GetCoordinates(object):
    def __init__(self, df_primers, df_primers_dups, filename, df_snps):
        self.df_primers = df_primers
        self.filename = filename
        self.df_primers_dups = df_primers_dups
        self.df_snps = df_snps

    def make_csv(self):
        primer_list = []
        names_dup = []
        names = []
        exons = []
        dirs = []

        for row_index, row in self.df_primers.iterrows():
            primer_list.append(str(row['Primer_seq']))
            names_dup.append(str(row['Gene']) + "_" + str(row['Exon']) + "_" + str(row['Direction']))
            exons.append(str(row['Exon']))
            dirs.append(str(row['Direction']))
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

        return names, exons, dirs, primer_list

    def run_pcr(self):
        chromosomes = ['chr10.2bit', 'chr11.2bit', 'chr12.2bit', 'chr1.2bit', 'chr13.2bit', 'chr14.2bit', 'chr15.2bit',
                       'chr16.2bit', 'chr17.2bit', 'chr18.2bit', 'chr19.2bit', 'chr20.2bit', 'chr21.2bit', 'chr22.2bit',
                       'chr2.2bit', 'chr3.2bit', 'chr4.2bit', 'chr5.2bit', 'chr6.2bit', 'chr7.2bit', 'chr8.2bit',
                       'chr9.2bit', 'chrX.2bit', 'chrY.2bit']

        for chr in chromosomes:
            os.system(
                "/opt/kentools/isPcr -out=psl /media/genomicdata/ucsc_hg19_by_chr/2bit_chr/%s \
                primerseqs.csv %s.tmp.psl" % (chr, chr[:-5]))

            pslfile = "%s.tmp.psl" % chr[:-5]
            bedfile = "%s.tmp.bed" % chr[:-5]

            if os.path.getsize(pslfile) != 0:
                os.system("/opt/kentools/pslToBed %s %s" % (pslfile, bedfile))
                return bedfile
            else:
                os.system("rm %s" % pslfile)

    def get_coords(self):
        tool = bed.BedTool(self.run_pcr())
        start_coords = []
        end_coords = []
        chroms = []
        seq_position = 0
        names, exons, dirs, primer_list = self.make_csv()

        for row in tool:
            chroms.append(row.chrom)
            start_coords.append(row.start)
            end_coords.append(row.start + len(primer_list[seq_position]))
            chroms.append(row.chrom)
            end_coords.append(row.end)
            start_coords.append(row.end - len(primer_list[seq_position + 1]))
            seq_position += 1

        df_coords = pd.DataFrame([])
        df_coords.insert(0, 'chrom', chroms)
        df_coords.insert(1, 'start', start_coords)
        df_coords.insert(2, 'end', end_coords)
        df_coords.insert(3, 'name', names)

        return df_coords

    def make_bed(self):
        df_coords = self.get_coords()

        df_coords.to_csv('%s.csv' % self.filename, header=None, index=None, sep='\t')
        csv_file = bed.BedTool('%s.csv' % self.filename)
        csv_file.saveas('%s.bed' % self.filename)

        os.system("rm /home/cuser/PycharmProjects/PrimerDatabase/%s.csv" % self.filename)

    def col_to_string(self, row):
        return str(row['Exon'])

    def make_excel(self):
        df_coords = self.get_coords()
        names, exons, dirs, primer_list = self.make_csv()

        df_coords.insert(4, 'Exon', exons)
        df_coords.insert(5, 'Direction', dirs)

        df_coords['Exon'] = df_coords.apply(self.col_to_string, axis=1)  # converts to string for merging
        self.df_primers_dups['Exon'] = self.df_primers_dups.apply(self.col_to_string, axis=1)

        joined_df = pd.merge(self.df_primers_dups, df_coords, how='left', on=['Exon', 'Direction'])
        cols_to_drop = ['name', 'chrom']
        joined_df = joined_df.drop(cols_to_drop, axis=1)

        writer = pd.ExcelWriter('%s.xlsx' % self.filename)
        joined_df.to_excel(writer, sheet_name='Current primers', index=False)
        self.df_snps = self.df_snps.drop(['Exon', 'Direction'], axis=1)
        self.df_snps.to_excel(writer, sheet_name='Current primers', index=False, startrow=0, startcol=16)
        writer.save()

        os.system("mv /home/cuser/PycharmProjects/PrimerDatabase/%s.xlsx /media/sf_sarah_share" % self.filename)

    def run_all(self):
        self.make_csv()
        # self.run_pcr()
        self.get_coords()
        self.make_bed()
        self.make_excel()