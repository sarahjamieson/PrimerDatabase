class CheckPrimers(object):
    """Checks extracted Primer data for valid data entries

        Note:
           Checks are only performed on columns with consistent data entries.
        Args:
            :param primer_df: data frame to be checked.
    """

    def __init__(self, primer_df):
        self.primer_df = primer_df

    def check_gene(self):
        """Returns the number of errors in the 'Gene' column (checks for special characters)."""
        global specials
        check = 0
        specials = ['?', '!', '~', '@', '#', '^', '&', '+', ':', ';', '%', '{', '}', '[', ']', ',']
        for row_index, row in self.primer_df.iterrows():
            for char in row['Gene']:
                if char in specials:
                    check += 1
                    print "Error: special character found in column 'Gene', see row", row_index+4
        return check

    def check_exon(self):
        """Returns the number of errors in the 'Exon' column (checks for special characters)."""
        check = 0
        for row_index, row in self.primer_df.iterrows():
            for char in str(row['Exon']):
                if char in specials:
                    check += 1
                    print "Error: special character found in column 'Exon', see row", row_index+4
        return check

    def check_direction(self):
        """Returns the number of errors in the 'Direction' column (should only contain "F" or "R")."""
        check = 0
        direction_list = ['F', 'R']
        for row_index, row in self.primer_df.iterrows():
            if row['Direction'] not in direction_list:
                check += 1
                print "Error: invalid primer direction, see row", row_index+4
        return check

    def check_version(self):
        """Returns the number of errors in the 'Version' column (should be a numerical value)."""
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (row['Version_no'] is not None) and (not isinstance(row['Version_no'], float)) and (
                    not isinstance(row['Version_no'], int)):
                check += 1
                print "Error: version number not a valid entry, see row", row_index+4
        return check

    def check_seq(self):
        """Returns the number of errors in the 'Primer-Seq' column (should only contain "A", "T", "C" or "G")."""
        nuc_list = ['A', 'T', 'C', 'G']
        check = 0
        for row_index, row in self.primer_df.iterrows():
            for letter in row['Primer_seq'].strip():
                if letter not in nuc_list:
                    check += 1
                    print "Error: invalid DNA primer sequence, see row", row_index+4
        return check

    def check_tag(self):
        """Returns the number of errors in the 'M13_tag' column (should only contain "Y" or "N")."""
        check = 0
        tag_list = ['Y', 'N']
        for row_index, row in self.primer_df.iterrows():
            if (row['M13_tag'] is not None) and (row['M13_tag'].upper() not in tag_list):
                check += 1
                print "Error: M13_tag not a valid entry, see row", row_index+4
        return check

    def check_batch(self):
        """Returns the number of errors in the 'Batch_no' column (checks for special characters)."""
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Batch_no'] is not None:
                for char in row['Batch_no']:
                    if char in specials:
                        check += 1
                        print "Error: special character found in column 'Batch_no', see row", row_index+4
        return check

    def check_dates(self):
        """Returns the number of errors in the 'Order_date' column (should be a datetime object)."""
        import datetime
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (row['Order_date'] is not None) and (not isinstance(row['Order_date'], datetime.datetime)):
                check += 1
                print "Error: order date not a valid date, see row", row_index+4
        return check

    def check_frag_size(self):
        """Returns the number of errors in the 'Frag_size' column (should be numerical and a valid length)."""
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Frag_size'] is not None:
                if (not isinstance(row['Frag_size'], float)) and (not isinstance(row['Frag_size'], int)):
                    check += 1
                    print "Error: fragment size not a valid entry, see row", row_index+4
                elif (row['Frag_size'] < 0) or (row['Frag_size'] > 1000):
                    check += 1
                    print "Error: fragment size not within acceptable range, see row", row_index+4
        return check

    def check_anneal_temp(self):
        """Returns the number of errors in the 'Anneal_temp' column (should be numerical and a valid temperature)."""
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Anneal_temp'] is not None:
                if (isinstance(row['Anneal_temp'], float)) or (isinstance(row['Anneal_temp'], int)):
                    if (row['Anneal_temp'] < 0) or (row['Anneal_temp'] > 150):
                        check += 1
                        print "Error: Annealing temperature not within acceptable range, see row", row_index+4
        return check

    def check_all(self):
        """Returns all checks as a list"""
        return self.check_gene(), self.check_exon(), self.check_direction(), self.check_version(), self.check_seq(), \
               self.check_tag(), self.check_batch(), self.check_dates(), self.check_frag_size(), \
               self.check_anneal_temp()

    def check_chrom(self):
        """Returns the number of errors in the 'Chrom' column (should be 1-23, X or Y)."""
        check = 0
        chromosomes = [range(1, 23), 'X', 'Y']
        for row_index, row in self.primer_df.iterrows():
            if row['Chrom'] is not None:
                if row['Chrom'] not in chromosomes:
                    check +=1
                    print "Error: invalid chromosome, see row", row_index+4, row['Chrom']
        return check
