import datetime
import os
import sys
from django.core.management.base import BaseCommand

from django.core.files import File

import os

from article.models import *
from io import BytesIO
from PyPDF2 import PdfReader

def create_file_from_pdf(pdf_path):
    # 打开 PDF 文件并获取内容
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        pdf_content = b''
        for page in pdf_reader.pages:
            pdf_content += page.extract_text().encode('utf-8')

    # 在 Django 中创建文件对象
    file_name = os.path.basename(pdf_path)
    django_file = File(open(pdf_path, 'rb'), name=file_name)

    # 更新文件内容为 PDF 视图内容
    django_file.file = BytesIO(pdf_content)

    return django_file


class Command(BaseCommand):
    help = 'Upload all PDF files in a directory to database'

    def add_arguments(self, parser):
        parser.add_argument('pdf_dir', type=str)

    def handle(self, *args, **options):
        pdf_dir = options['pdf_dir']
        count = 1
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                file_pure, pdf_end = filename.split('.')
                work_name, writer_who = file_pure.split('_')
                set_id = count
                has_pdf = 1
                content = 'nothing'
                send_time = datetime.datetime.now()
                if '乡村振兴' in filename:
                    category = '社会科学'
                else:
                    category = '信息科技'
                pdf_path = os.path.join(pdf_dir, filename)
                uploaded_file = create_file_from_pdf(pdf_path)
                my_model = Work.objects.create(
                    id=set_id,
                    pdf=uploaded_file,
                    work_name=work_name,
                    author_id=writer_who,
                    has_pdf=has_pdf,
                    content=content,
                    send_time=send_time,
                    author=writer_who,
                    category=category
                )
                my_model.save()
                count = count + 1
                self.stdout.write(self.style.SUCCESS(f'Successfully uploaded {filename}'))