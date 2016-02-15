from getprimers import GetPrimers
from getcoordinates import GetCoordinates

excel_file = 'Alport_example.xlsx'  # user input for excel file

df_primers_dups, df_primers = GetPrimers(excel_file).get_primers()
df_snps = GetPrimers(excel_file).get_snps()

filename = 'TestOutput'

# filename = raw_input('What name would you like to save the output as? ')

GetCoordinates(df_primers, df_primers_dups, filename, df_snps).run_all()
