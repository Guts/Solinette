import xlrd
from time import strftime

xlspath = r'C:\Documents and Settings\Utilisateur\Mes documents\GitHub\Solinette\Sources\municipalidades_multi.xls'

exp = open(r'C:\Documents and Settings\Utilisateur\Mes documents\GitHub\Solinette\Sources\municipalidades_multi.txt', 'wb')

dico = {}
dico2 = {}

book = xlrd.open_workbook(xlspath)

sh = book.sheet_by_index(0)
# method 1
for row in range(1, sh.nrows):
    dico[row] = sh.row_values(row)

print dico
print '########################'

# method 2
for row in range(1, sh.nrows):
    dico2[row] = []
    for col in range(sh.ncols):
        if sh.cell_type(row, col) is not 3:
            dico2[row].append(unicode(sh.cell_value(row, col)))
        else:
            date = xlrd.xldate_as_tuple(sh.cell_value(row, col), book.datemode)
            dico2[row].append('-'.join([str(i) for i in date[:3]]))

print dico2
print '########################'

# method 3
sh.dump(exp)
exp.close()


