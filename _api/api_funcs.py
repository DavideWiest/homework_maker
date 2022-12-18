import uuid
import os

from modules.pdfmanager import PdfManager
from modules.doc_creator import DocCreator
from modules.gptinterface import GPTInterface

class ApiFunctions():
    def __init__(self):
        self.pm = PdfManager()
        self.dc = DocCreator({})
        self.gi = GPTInterface()

    def text_to_tasks(self, text):
        tasks = self.pm.get_possible_tasks(text)

        return tasks

    def tasks_to_answers(self, tasks):
        
        answers = [self.gi.get_answer(i) for i in tasks]

        return answers

    def answers_to_pdf(self, params):
        _uuid = uuid.uuid4().hex

        homework_done = self.dc.render_homework(params)
        pdfpath = f"homework_maker/out_pdfs/{_uuid}.pdf"

        try:
            self.dc.pdf_from_str(homework_done, pdfpath)
        except OSError:
            pass
        
        pdf = open(pdfpath, 'rb')

        os.remove(pdfpath)

        return pdf