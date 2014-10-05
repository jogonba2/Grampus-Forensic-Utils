import pyexiv2
class extractjpg:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.metaDictionary = {}
		self.__openFile()
		self._extract()
	
	# Open File To Extract Metadata
	def __openFile(self):
		
		try:
			self.metaData = pyexiv2.ImageMetadata(self.pathFile)
			self.__extractMetadata()
		except:
			self.metaDictionary["Error"] = "Isn't JPG File"
	
	# Extract Metadata From Image With EXIF Especification
	def __extractMetadata(self):
		
		try:
			self.metaData.read()
		except:
			self.metaDictionary["Error"] = "Isn't a valid JPG"
			
		for self.data in self.metaData.exif_keys:
			try:
				self.metaDictionary[(self.metaData.__getitem__(self.data).key.replace("Exif.",""))] = (self.metaData.__getitem__(self.data)).value
			except:
				pass
		
			
	#Show Extracted Metadata From Image
	def _extract(self):
		
		return self.metaDictionary

print extractjpg("test.jpg")._extract()
