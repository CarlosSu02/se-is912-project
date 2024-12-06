from markdown import markdown
from docx import Document


def convert_md_to_docx(content, output_file):
    html_content = markdown(content)

    doc = Document()

    for line in html_content.splitlines():
        print(line)


def text_to_docx(content, output_file):
    doc = Document()

    doc.add_paragraph(content)

    doc.save(output_file)
