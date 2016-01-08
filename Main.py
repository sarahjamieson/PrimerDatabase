from ExcelToSQL import ExcelToSQL

excel_file = 'CHARGE_CHD7.xlsx'
db = 'Primer_v1.db'

ets = ExcelToSQL(excel_file, db)
ets.get_all()
