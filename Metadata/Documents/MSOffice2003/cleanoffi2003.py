from extractoffi2003 import extractoffi2003
class cleanoffi2003:
	
	def __init__(self,docFile):
		
		self.docFile = docFile
		self.metaData = extractoffi2003(self.docFile)._extract()
		self._executeClean()
	
	def _executeClean(self):
		
		with file(self.docFile,"rb") as fileNew:
			text = fileNew.read()
			fileNew.close()	
			for data in self.metaData:			
				if str(self.metaData[data]) in text:
					text = text.replace(str(self.metaData[data]),"")
		with file(self.docFile,"wb") as fileNew:
			fileNew.write(text)
			fileNew.close()			

cleanoffi2003("test.doc")
