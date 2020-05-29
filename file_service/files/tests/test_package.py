import textract
import re
import os
from plugins import (pdf_file_generator, png_file_generator, docx_file_generator)
from django.test import TestCase


class PluginTests(TestCase):
    def test_pdf_file_generator(self):
        template = """<head>
                    <title>{{title}}</title>
                    </head>
                    <body>
                        <div>
                            <h1>{{text}}</h1>
                        </div>
                    </body>
                    """
        path = os.getcwd()
        file = pdf_file_generator.PDFFileGenerator.create(template, {'title': 'Проверка', 'text': 'Текст'})
        pdf_file = open(path + '/generated.pdf', 'wb')
        pdf_file.write(file)
        pdf_file.close()
        b_text = textract.process(path + '/generated.pdf')
        raw_text = b_text.decode("utf-8")
        text = re.sub(r'\s+', ' ', re.sub(r'<[^<]+>', ' ', raw_text))
        os.remove('./generated.pdf')
        self.assertEqual(text, 'Текст ')

    def test_png_file_generator(self):
        template = """
                    <body>
                        <div>
                            <h1>{{text}}</h1>
                        </div>
                    </body>
                    """
        path = os.getcwd()
        file = png_file_generator.PNGFileGenerator.create(template, {'text': 'Текст'})
        pdf_file = open(path + '/generated.png', 'wb')
        pdf_file.write(file)
        pdf_file.close()
        b_text = textract.process(path + '/generated.png')
        raw_text = b_text.decode("utf-8")
        text = re.sub(r'\s+', ' ', re.sub(r'<[^<]+>', ' ', raw_text))
        os.remove('./generated.png')
        self.assertEqual(text, 'Текст ')

    def test_docx_file_generator(self):

        template = """
                 <style>
                    @page { size: A4; }
                    * { }
                </style>
                    <div>
                        <h1>{{text}}</h1>
                    </div>
                    """
        path = os.getcwd()
        file = docx_file_generator.DOCXFileGenerator.create(template, {'text': 'Текст'})
        pdf_file = open(path + '/generated.docx', 'wb')
        pdf_file.write(file)
        pdf_file.close()
        b_text = textract.process(path + '/generated.docx')
        raw_text = b_text.decode("utf-8")
        text = re.sub(r'\s+', ' ', re.sub(r'<[^<]+>', ' ', raw_text))
        os.remove('./generated.docx')
        self.assertEqual(text, 'Текст')
