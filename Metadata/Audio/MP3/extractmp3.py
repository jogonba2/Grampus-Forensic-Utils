from ID3 import *
class extractmp3:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.metaData = {}
	
	def _extract(self):
		try:
			self.id3info = ID3(self.pathFile)
			for self.elemento in self.id3info.keys():
				self.metaData[self.elemento.lower().capitalize()] = str(self.id3info[self.elemento])
		except:
			self.metaData["Error"] = "Isn't a valid mp3 file"
		return self.metaData
