import pathlib
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf import teletype
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
            if addition_file.endswith('.cs') or addition_file.endswith('.xaml'):  # wpf + cs
                # if addition_file.endswith('.cs') or addition_file.endswith('.axaml'): # avalonia + cs
                # if addition_file.endswith('.java') or addition_file.endswith('.ftl') or addition_file.endswith('.ftlh'): #
                files.append([addition_file, path + '/' + addition_file])
    directories = [directory.name for directory in directory.iterdir() if directory.is_dir()
                   and not directory.name.startswith(".")]
    for directory in directories:
        directory_transversal(path + '/' + directory)


directory_transversal(main_path)

doc = OpenDocumentText()

styles = doc.styles
code_style = Style(name="Code Style", family="paragraph")
code_style.addElement(ParagraphProperties(attributes={"textalign": "left"}))
code_style.addElement(TextProperties(attributes={"fontsize": "12pt", "fontfamily": "Times New Roman"}))
styles.addElement(code_style)

for file_name, file_path in files:
    header_element = P(stylename='Основное')
    header_text = file_name
    teletype.addTextToElement(header_element, header_text)
    doc.text.addElement(header_element)
    content_element = P(stylename='Code Style')
    with open(file_path, 'r', encoding='utf-8') as file:
        content_text = file.read() + '\n'
        teletype.addTextToElement(content_element, content_text)
        doc.text.addElement(content_element)

doc.save('code.odt')
print('done')
