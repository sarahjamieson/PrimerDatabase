class CheckSNPs(object):
    """Checks extracted SNP data for valid data entries.

       Note:
           Checks are only performed on the three columns with consistent data input.

       Args:
           :param snp_df: data frame to be checked.
    """

    def __init__(self, snp_df):
        self.snp_df = snp_df

    def check_no_snps(self):
        """Returns the number of errors in the 'Total SNPs' column (this should be a numerical value)."""
        check = 0
        for row_index, row in self.snp_df.iterrows():
            if row['Total_SNPs'] is not None:
                if (not isinstance(row['Total_SNPs'], float)) and (not isinstance(row['Total_SNPs'], int)):
                    check += 1
                    print "Error: invalid entry in 'Total_SNPs' column, see row", row_index+4  # prints row in excel doc
        return check

    def check_rs(self):
        """Returns the number of errors in the 'dbSNP rs' column (IDs should all begin with "rs")."""
        import re
        check = 0
        for row_index, row in self.snp_df.iterrows():
            if row['dbSNP_rs'] is not None:
                if not re.match("rs(.*)", row['dbSNP_rs']):
                    check += 1
                    print "Error: invalid dbSNP rs number, see row", row_index+4  # prints row in excel doc
        return check

    def check_hgvs(self):
        """Returns the number of errors in the 'HGVS' column (Nomenclature should begin with "c.")."""
        import re
        check = 0
        for row_index, row in self.snp_df.iterrows():
            if row['HGVS'] is not None:
                if not re.match("c(.*)", row['HGVS']):
                    check += 1
                    print "Error: invalid HGVS nomenclature, see row", row_index+4  # prints row in excel doc
        return check

    def check_all(self):
        return self.check_no_snps(), self.check_rs(), self.check_hgvs()