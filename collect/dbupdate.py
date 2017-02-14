from openpyxl import load_workbook
from xlrd import open_workbook
from collect.models import TitTesouro

wb = open_workbook(filename="../Download/LTN_2016_auto.xls")

print(wb.sheet_names())
print(wb.nsheets)
print(wb.sheet_by_index(0).nrows)
print(wb.sheet_by_index(1).cell_value(rowx=3, colx= 4))
wb.sheets()

def updatedb(wb):
    print(wb.nsheets)
    for sheet in wb.sheets():
        t = TitTesouro()
        t.Nome = sheet.name
        for row in (sheet.nrows-3):
            t.Dia = sheet.cell_value(rowx=row+3,colx=1)
            t.TxCompra = sheet.cell_value(rowx=row+3,colx=2)
            t.TxVenda = sheet.cell_value(rowx=row+3,colx=3)
            t.PUCompra = sheet.cell_value(rowx=row+3,colx=4)
            t.PUVenda = sheet.cell_value(rowx=row+3,colx=5)
            t.PUBase = sheet.cell_value(rowx=row+3,colx=6)
t = TitTesouro()
# ws = wb['big_data']
#
# print(ws.row[1].cell[1].value)