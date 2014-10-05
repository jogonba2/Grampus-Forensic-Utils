import OleFileIO_PL
class extractoffi2003:
	
	def __init__(self,docFile):
		
		self.docFile = docFile
		self.metaData = {}
		self.__initOleFile()
		self.__detectType()
	
	def __initOleFile(self):
		
		if OleFileIO_PL.isOleFile(self.docFile)==False:
			self.metaData["Error"] = "Isn't an Ole File"
		else:
			self.oleFile = OleFileIO_PL.OleFileIO(self.docFile)
	
	# Actually only support Word,Excel,PowerPoint. It's easy add more extensions :D
	""" Extensions are separated by groups because Excel and Word need
		SummaryInformation but ppt no and it doesn't add extra information, there are also other areas such as
		Current User or Pictures.
	"""
	def __detectType(self):
		
		for docType in [['Workbook'],['WordDocument'],['PowerPoint Document']]:
			if docType in self.oleFile.listdir():
				self.__manageExtraction(docType)
	
	def __manageExtraction(self,docType):
		
		if docType==['WordDocument'] or docType==['Workbook']:
			self.__extractDocument()
		else:
			self.__extractPresentation()
	
	def __extractDocument(self):
		
		for oleDir in self.oleFile.listdir():
			try:
				Properties = self.oleFile.getproperties(oleDir)
				for propertie in Properties:
					try:
						self.__oleFileIndex(propertie,Properties)
					except:
						continue
			except:
				continue
		# Add size to metadata table because it isn't returned in getproperties method
		try:
			self.metaData["Size"] = self.oleFile.get_size("WordDocument")
		except:
			self.metaData["Size"] = self.oleFile.get_size("Workbook")
	
	def __oleFileIndex(self,propertie,Properties):
		
		if propertie==8:
			self.metaData["Last Author"] = str(Properties[propertie])
		elif propertie==3:
			self.metaData["Assumpt"] = str(Properties[propertie])
		elif propertie==18:
			self.metaData["Tool"] = str(Properties[propertie])
		elif propertie==4:
			self.metaData["Author"] = str(Properties[propertie])
		elif propertie==9:
			self.metaData["Revisions"] = str(Properties[propertie])
		elif propertie==2:
			self.metaData["Title"] = str(Properties[propertie])
		elif propertie==5:
			self.metaData["Tags"] = str(Properties[propertie])
		elif propertie==6:
			self.metaData["Comments"] = str(Properties[propertie])
		elif propertie==16:
			self.metaData["Characters"] = str(Properties[propertie])
		elif propertie==15:
			self.metaData["Organization"] = str(Properties[propertie])
		elif propertie==5:
			self.metaData["Lines"] = str(Properties[propertie])
		elif propertie==7:
			self.metaData["Template"] = str(Properties[propertie])
		else:
			self.metaData["Unknown Information"] = str(Properties[propertie])
		
				
	def __extractPresentation(self):
		
		for oleDir in self.oleFile.listdir():
			try:
				if oleDir in (['\x05DocumentSummaryInformation'],['Current User']):
					self.metaData[str(oleDir)] = self.oleFile.getproperties(oleDir)
			except:
				continue
		try:
			self.metaData["Size"] = self.oleFile.get_size("PowerPoint Document")
		except:
			pass
			
	def _extract(self):
		
		return self.metaData
