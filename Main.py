import warnings
from ExcelToSQL import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'Alport_COL4A5.xlsx'
db = 'Primer_v1.db'

ets = ExcelToSQL(excel_file, db)
ets.get_all()
