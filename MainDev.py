import warnings
from ExcelToSQLDev import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'TestETS_COL4A5.xlsx'
db = 'Test.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()