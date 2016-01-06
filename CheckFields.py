class CheckFields(object):
    def __init__(self, primer_df):
        self.primer_df = primer_df

    def check_special(self):
        import re
        check = 0
        for row_index, row in self.primer_df.iterrows():
            for colname in self.primer_df.columns:
                row_element = row[colname]
                if (row_element is not None) and (type(row_element) != float) and (type(row_element) != int):
                    for letter in row_element:
                        if re.match("[?!~@#^&+:;,%'{}]", letter):
                            check += 1
                            print "Error: invalid entry"
                            print row_element

        if check == 0:
            print "No invalid characters detected"

    def check_nucs(self):
        nuc_list = ['A', 'T', 'C', 'G']
        check = 0
        for row_index, row in self.primer_df.iterrows():
            for letter in row['Primer_seq']:
                if letter not in nuc_list:
                    check += 1
                    print "Error: Invalid sequence"
                    print row['Primer_seq']

        if check == 0:
            print "All primer sequences valid"

    def check_direction(self):
        check = 0
        direction_list = ['R', 'F']
        for row_index, row in self.primer_df.iterrows():
            for letter in row['Direction']:
                if letter not in direction_list:
                    check += 1
                    print "Error: Invalid primer direction"
                    print row['Direction']

        if check == 0:
            print "All primer directions valid"

    def check_fragments(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (not isinstance(row['Frag_size'], float)) and (not isinstance(row['Frag_size'], int)):
                check += 1
                print "Error: Fragment size not a number"
                print row['Frag_size']
            if (row['Frag_size'] < 0) or (row['Frag_size'] > 1000):
                check += 1
                print "Error: Fragment size not within acceptable range"
                print row['Frag_size']

        if check == 0:
            print "All fragment sizes valid"

    def check_version(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (not isinstance(row['Version'], float)) and (not isinstance(row['Version'], int)):
                check += 1
                print "Error: Version not a number"
                print row['Version']

        if check == 0:
            print "All version numbers valid"

    def check_anneal(self):
        check = 0
        for row_index, row in self.primer_df.iterrows():
            if (not isinstance(row['Anneal_temp'], float)) and (not isinstance(row['Anneal_temp'], int)):
                check += 1
                print "Error: Annealing temperature not a number"
                print row['Anneal_temp']
            if (row['Anneal_temp'] < 0) or (row['Anneal_temp'] > 150):
                check += 1
                print "Error: Annealing temperature not within acceptable range"
                print row['Anneal_temp']

        if check == 0:
            print "All annealing temperatures valid"
        else:
            print "Done"
