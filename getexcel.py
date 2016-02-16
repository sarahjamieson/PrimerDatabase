import pandas as pd
import re


class GetExcel(object):
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
        df_primers_dups = pd.read_excel(self.excel_file, header=0, parse_cols='A:M', skiprows=2,
                                        names=['Gene', 'Exon', 'Direction', 'Version_no', 'Primer_seq', 'Chrom',
                                               'M13_tag', 'Batch_no', 'Batch_test_MS_project', 'Order_date',
                                               'Frag_size', 'Anneal_temp', 'Other_info'],
                                        sheetname=sheet_name, index_col=None)

        df_primers_dups = df_primers_dups.where((pd.notnull(df_primers_dups)), None)
        df_primers = df_primers_dups.drop_duplicates(subset=('Gene', 'Exon', 'Direction', 'Chrom'))
        df_primers = df_primers.reset_index(drop=True)

        return df_primers_dups, df_primers

    def get_snps(self):
        sheet_name = self.get_sheet_name()
        df_snps = pd.read_excel(self.excel_file, header=0, parse_cols='B:C,O:X', skiprows=2,
                                names=['Exon', 'Direction', 'SNPCheck_build', 'Total_SNPs', 'dbSNP_rs', 'HGVS',
                                       'Frequency', 'ss_refs', 'ss_projects', 'Other_info', 'Action_required',
                                       'Checked_by'],
                                index_col=False, sheetname=sheet_name)
        df_snps = df_snps.where((pd.notnull(df_snps)), None)

        return df_snps