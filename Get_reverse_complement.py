dna_seq = 'ATGGTTCCAGCTA'


def get_reverse_complement():
    dna_seq_list = list(dna_seq)
    complement_seq = []
    for i in reversed(dna_seq_list):
        if i is 'A':
            complement_seq.append('T')
        elif i is 'G':
            complement_seq.append('C')
        elif i is 'C':
            complement_seq.append('G')
        elif i is 'T':
            complement_seq.append('A')
        else:
            print 'error'

    print ''.join(complement_seq)

get_reverse_complement()