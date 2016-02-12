import pybedtools as bed
from getcoordinates import GetCoordinates as gc


class MakeBedFile(object):
    def __init__(self, bedfile, primer_list):
        self.bedfile = bedfile
        self.primer_list = primer_list

    def get_coordinates(self):
        coord_bed = bed.BedTool(self.bedfile)
        start_coords = []
        end_coords = []
        seq_position = 0

        for row in coord_bed:
            start_coords.append(row.start)
            end_coords.append(row.start + len(self.primer_list[seq_position]))
            end_coords.append(row.end)
            start_coords.append(row.end - len(self.primer_list[seq_position + 1]))
            seq_position += 1

    output_df = pd.DataFrame([])
output_df.insert(0, 'chrom', chroms)
output_df.insert(1, 'start', start_coords)
output_df.insert(2, 'end', end_coords)
output_df.insert(3, 'name', names)

output_df.to_csv('final.csv', header=None, index=None, sep='\t')
final = bed.BedTool('final.csv')
final.saveas('final2.bed')
