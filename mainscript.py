import warnings
from exceltosql import ExcelToSQL
warnings.simplefilter("ignore", UserWarning)

"""Module takes an excel file and database as inputs and runs the ExcelToSQL class to add excel files to a database."""

excel_file = raw_input('Enter excel file name with file extension: ')

db = 'Primer_v1.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()
