import csv, xlrd
from os import path

xlspath = r'E:\Mes documents\GitHub\Solinette\sources\municipalidades_multi.xls'


def xls2csv(xlspath):
    u""" export an Excel 2003 file (.xls) to a CSV file
    see: http://stackoverflow.com/a/10803229 """
    with xlrd.open_workbook(xlspath) as book:
        sheet = book.sheet_by_index(0)
        with open('temp/' + path.splitext(path.basename(xlspath))[0] + '.csv', 'wb') as f:
            out = csv.writer(f, delimiter='\t', dialect = 'excel-tab', quotechar='"')
            for row in range(sheet.nrows):
##                out.writerow(sheet.row_values(row))
                try:
                    out.writerow(sheet.row_values(row))
                except:
                     out.writerow([unicode(s).encode("latin-1") for s in sheet.row_values(row)])

    # End of function
    return book, f



xls2csv(xlspath)