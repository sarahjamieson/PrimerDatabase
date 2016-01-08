import warnings
from ExcelToSQL import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'Marfan_FBN1.xlsx'
db = 'Primer_v1.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()
