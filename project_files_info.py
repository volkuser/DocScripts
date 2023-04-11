import pathlib
import os
import math
# console table
from tabulate import tabulate
# docx table
# from docx import Document
# odt table
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

print('enter the path to project:', end=' ')
main_path = input()
if main_path.endswith('/'):
    main_path = main_path[:-1]

files = []


def directory_transversal(path):
    directory = pathlib.Path(path)
    addition_files = [cs.name for cs in directory.iterdir() if cs.is_file()]
    if addition_files != 0:
        global files
        for addition_file in addition_files:
            if addition_file.endswith('.java') or addition_file.endswith('.xml'): # android (xml + java)
            # if addition_file.endswith('.java'): # only java
            #if addition_file.endswith('.cs') or addition_file.endswith('.xaml'):  # wpf + cs
            # if addition_file.endswith('.cs') or addition_file.endswith('.axaml'): # avalonia + cs
            # if addition_file.endswith('.java') or addition_file.endswith('.ftl') or addition_file.endswith('.ftlh'): # java + freemarker
                files.append([addition_file, sum(1 for _ in open(path + '/' + addition_file)),
                              math.ceil(os.path.getsize(path + '/' + addition_file) / 1024)])
    directories = [directory.name for directory in directory.iterdir() if directory.is_dir()
                   and not directory.name.startswith(".")]
    for directory in directories:
        directory_transversal(path + '/' + directory)


directory_transversal(main_path)

# console version
headers = ['file name', 'row count', 'weight']
print(tabulate(files, headers=headers, tablefmt="grid"))

# docx version
"""
docx_doc = Document()
table = docx_doc.add_table(rows=0, cols=3)
for file_name, row_count, weight in files:
    row = table.add_row().cells
    row[0].text = file_name
    row[1].text = str(row_count)
    row[2].text = str(weight)
docx_doc.save('table.docx')
"""

# ods version
ods_doc = OpenDocumentSpreadsheet()
table = Table(name="information about project files")
number = 1


def get_cell(input_str):
    cell = TableCell(valuetype='string', stylename='Table Contents')
    cell.addElement(P(text=str(input_str)))
    return cell


for file_name, row_count, weight in files:
    row = TableRow()
    row.addElement(get_cell(number))
    number += 1
    row.addElement(get_cell(file_name))
    row.addElement(get_cell(row_count))
    row.addElement(get_cell(weight))
    table.addElement(row)
ods_doc.spreadsheet.addElement(table)
ods_doc.save('table.ods')

print('uploaded information in table for ' + str(len(files)) + ' files')
