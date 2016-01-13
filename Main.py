import warnings
from ExcelToSQL import ExcelToSQL
warnings.simplefilter("ignore", UserWarning)

"""Module takes an excel file and database as inputs and runs the ExcelToSQL class to add excel files to a database."""

excel_file = 'HSP_REEP1.xlsx'
db = 'Primer_v1.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()
