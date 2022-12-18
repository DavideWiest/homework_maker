import PyPDF2


class PdfManager():
    def __init__(self):
        self.prelineindicators = ["Aufgaben", "Arbeitsauftrag", "Arbeitsaufträge", "Aufgabe"]
        self.inlineindicators = ["Begründe", "Erläuter", "Beschreib", "Benenne", "nimm Stellung", "Schreibe", "Erörter", "Charakterisier"] + self.prelineindicators
        self.ugly_starts = list(":.-,)1234567890") + self.prelineindicators


    def pdf_to_text(self, pdf_filepath, merge=True):

        pdffileobj = open(pdf_filepath,'rb')

        pdfreader = PyPDF2.PdfFileReader(pdffileobj)
        
        #This will store the number of pages of this pdf file
        pagenum = pdfreader.numPages

        page_texts = []

        for i in range(pagenum):
            #create a variable that will select the selected number of pages
            #(x-1) because python indentation starts with 0.
            #create text variable which will store all text datafrom pdf file
            pageobj = pdfreader.getPage(i)

            text = pageobj.extractText()
            page_texts.append(text)

        if merge:
            page_texts = "\n".join(page_texts)

        return page_texts

    def _cleanstr(self, string):
        string = " ".join(string.split())

        while any([string.startswith(a) for a in self.ugly_starts]):            
            string = string[1:]

        while any([string.endswith(a) for a in self.ugly_starts]):            
            string = string[1:]

        return string

    def get_possible_tasks(self, text):
        textlines = text.replace("\t", " ").split(".")
        tasks = []

        for i in range(len(textlines)):
            
            if textlines[i].replace(" ", "") == "" or textlines[i].split() == []:
                continue

            append = False
            if i > 0:
                if any([a.lower() in textlines[i-1].lower() for a in self.prelineindicators]):
                    append = True

                elif textlines[i-1][-1].isnumeric():
                    append = True
            
            if append != True:
                if any([a.lower() in textlines[i].lower() for a in self.inlineindicators]):
                    append = True

                elif textlines[i].split()[0].isnumeric():
                    append = True
                    

            if append:
                task = self._cleanstr(textlines[i])

                tasks.append(task)
        
        tasks = [task for task in tasks if task != ""]

        return tasks


if __name__ == '__main__':
    pm = PdfManager()
    text = pm.pdf_to_text("sample2.pdf")
    tasks = pm.get_possible_tasks(text)
    print(tasks)
    print(len(tasks))


