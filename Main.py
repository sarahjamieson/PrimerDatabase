import warnings
from ExcelToSQL import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'HSP_REEP1.xlsx'
db = 'Primer_v1.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()
