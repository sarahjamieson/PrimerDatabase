import warnings
from ExcelToSQLDev import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'Marfan_FBN1.xlsx'
db = 'Test.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()