from getcoordinates import GetCoordinates

excel_file = 'Alport_example.xlsx'

gc = GetCoordinates(excel_file)
gc.get_all()

bedfile = gc.run_pcr()
