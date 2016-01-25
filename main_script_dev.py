import warnings
from excel_to_sql_dev import ExcelToSQL

warnings.simplefilter("ignore", UserWarning)

excel_file = 'TestETS_COL4A5.xlsx'
db = 'Test.db'

ets = ExcelToSQL(excel_file, db)
ets.to_sql()