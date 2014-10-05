import pyexiv2
class cleanjpg:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.__replaceMetaData()
		print pathFile
	
	def __replaceMetaData(self):
		
		metaData = pyexiv2.metadata.ImageMetadata(self.pathFile)
		metaData.read()
		countKey = 0
		while countKey<=len(metaData.exif_keys):
			for keys in metaData.exif_keys:
				try:
					metaData.__delitem__(keys)
				except:
					continue
			metaData.write()
			countKey += 1
