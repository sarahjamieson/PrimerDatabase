import warnings
from ExcelToSQLTest import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'HSP_ATL1.xlsx'
db = 'Test.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()