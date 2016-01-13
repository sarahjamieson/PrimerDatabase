class CheckSNPs(object):
    def __init__(self, primer_df):
        self.primer_df = primer_df

    def check_no_snps(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Total_SNPs'] != 0 and row['Total_SNPs'] is not None:
                if (not isinstance(row['Total_SNPs'], float)) and (not isinstance(row['Total_SNPs'], int)):
                    check += 1
                    print "Error: invalid entry in 'Total_SNPs' column, see row", row_index+4
        return check

    def check_rs(self):
        import re
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['dbSNP_rs'] is not None:
                if not re.match("rs(.*)", row['dbSNP_rs']):
                    check += 1
                    print "Error: invalid dbSNP rs number, see row", row_index+4
        return check

    def check_hgvs(self):
        import re
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['HGVS'] is not None:
                if not re.match("c(.*)", row['HGVS']):
                    check += 1
                    print "Error: invalid HGVS nomenclature, see row", row_index+4
        return check

    def check_all(self):
        return self.check_no_snps(), self.check_rs(), self.check_hgvs()
