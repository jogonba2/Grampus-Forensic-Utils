from pyPdf import PdfFileReader,PdfFileWriter
from pyPdf.generic import createStringObject	
	
class extractpdf():

    def __init__(self):
        self.metaData = {}

    def _extract(self, pdfname):
        pdf = PdfFileReader(file(pdfname, 'rb'))
        try:
            meta_info = pdf.getDocumentInfo()
            for meta_obj in meta_info:
                self.metaData[meta_obj[1:]] = meta_info[meta_obj]
        except:
            self.metaData["Error"] = "Ocurrio un error"
        return self.metaData

extractpdf()._extract("test.pdf")
