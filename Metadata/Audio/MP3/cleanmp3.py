from ID3 import *
class cleanmp3:
	
		def __init__(self, pathFile):
			self.pathFile = pathFile
			self.__cleanMetadata()
			
		def __cleanMetadata(self):
			
				self.id3info = ID3(self.pathFile)
				try:
						id3info['TITLE'] = ""
						id3info['ALBUM'] = ""
						id3info['COMMENT'] = ""
						id3info['ARTIST'] = ""
						id3info['YEAR'] = ""
						id3info['GENRE'] = ""
				except:
						pass
