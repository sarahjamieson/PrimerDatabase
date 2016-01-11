class CheckPrimers(object):
    def __init__(self, primer_df):
        self.primer_df = primer_df

    def check_gene(self):
        global specials
        check = 0
        specials = ['?', '!', '~', '@', '#', '^', '&', '+', ':', '.', ';', '%', '{', '}', '[', ']', ',']
        for row_index, row in self.primer_df.iterrows():
            for char in row['Gene']:
                if char in specials:
                    check += 1
                    print "Error: special character found in column 'Gene', ", row['Gene']
        return check

    def check_exon(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            for char in str(row['Exon']):
                if char in specials:
                    check += 1
                    print "Error: special character found in column 'Exon', ", row['Exon']
        return check

    def check_direction(self):
        check = 0
        direction_list = ['F', 'R']
        for row_index, row in self.primer_df.iterrows():
            if row['Direction'] not in direction_list:
                check += 1
                print "Error: invalid primer direction, see exon", row['Exon']
        return check

    def check_version(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (row['Version_no'] is not None) and (not isinstance(row['Version_no'], float)) and (
                    not isinstance(row['Version_no'], int)):
                check += 1
                print "Error: version number not a valid entry, see exon", row['Exon']
        return check

    def check_seq(self):
        nuc_list = ['A', 'T', 'C', 'G']
        check = 0
        for row_index, row in self.primer_df.iterrows():
            for letter in row['Primer_seq'].strip():
                if letter not in nuc_list:
                    check += 1
                    print "Error: invalid DNA primer sequence, see exon", row['Exon']
        return check

    def check_tag(self):
        check = 0
        tag_list = ['Y', 'N']
        for row_index, row in self.primer_df.iterrows():
            if (row['M13_tag'] is not None) and (row['M13_tag'].upper() not in tag_list):
                check += 1
                print "Error: M13_tag not a valid entry, see exon", row['Exon']
        return check

    def check_batch(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Batch_no'] is not None:
                for char in row['Batch_no']:
                    if char in specials:
                        check += 1
                        print "Error: special character found in column 'Batch_no', see exon", row['Exon']
        return check

    def check_dates(self):
        import datetime
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (row['Order_date'] is not None)and (not isinstance(row['Order_date'], datetime.datetime)):
                check += 1
                print "Error: order date not a valid date, see exon", row['Exon']
        return check

    def check_frag_size(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Frag_size'] is not None:
                if (not isinstance(row['Frag_size'], float)) and (not isinstance(row['Frag_size'], int)):
                    check += 1
                    print "Error: fragment size not a valid entry, see exon", row['Exon']
                if (row['Frag_size'] < 0) or (row['Frag_size'] > 1000):
                    check += 1
                    print "Error: fragment size not within acceptable range, see exon", row['Exon']
        return check

    def check_anneal_temp(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if row['Anneal_temp'] is not None:
                if (isinstance(row['Anneal_temp'], float)) or (isinstance(row['Anneal_temp'], int)):
                    if (row['Anneal_temp'] < 0) or (row['Anneal_temp'] > 150):
                        check += 1
                        print "Error: Annealing temperature not within acceptable range, see exon", row['Exon']
        return check

    def check_all(self):
        gene_faults = self.check_gene()
        if gene_faults == 0:
            exon_faults = self.check_exon()
            if exon_faults == 0:
                direction_faults = self.check_direction()
                if direction_faults == 0:
                    version_faults = self.check_version()
                    if version_faults == 0:
                        seq_faults = self.check_seq()
                        if seq_faults == 0:
                            tag_faults = self.check_tag()
                            if tag_faults == 0:
                                batch_faults = self.check_batch()
                                if batch_faults == 0:
                                    date_faults = self.check_dates()
                                    if date_faults == 0:
                                        frag_faults = self.check_frag_size()
                                        if frag_faults == 0:
                                            anneal_faults = self.check_anneal_temp()
                                            if anneal_faults == 0:
                                                print "All checks complete with no errors."