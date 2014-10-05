import os.path
from time import ctime
## Absolute Paths ##

class metadataOS:
	
	def __init__(self,filename):
		self.datamap = self.__setdatamap(filename)

	def __setdatamap(self,filename):
		return {"Absolute Path":metadataOS.__getlocalpath(filename),
				"Last Access Time":metadataOS.__getlastaccesstime(filename),
				"Last Modified Time":metadataOS.__getlastmodifiedtime(filename),
				"Creation Time":metadataOS.__getcreationtime(filename),
				"Size":metadataOS.__getsize(filename),
				"Mount Point":metadataOS.__ismountpoint(filename)
			   }
			   
	def _getdatamap(self):
		return self.datamap
		
	@staticmethod
	def __getlastaccesstime(filename):
		return ctime(os.path.getatime(filename))
		
	@staticmethod
	def __getlastmodifiedtime(filename):
		return ctime(os.path.getmtime(filename))
		
	@staticmethod
	def __getcreationtime(filename):
		return ctime(os.path.getctime(filename))
	
	@staticmethod
	def __getsize(filename):
		return os.path.getsize(filename)
	
	@staticmethod
	def __getlocalpath(filename):
		return os.path.abspath(filename)
	
	@staticmethod
	def __ismountpoint(filename):
		return os.path.ismount(filename)

if __name__ == "__main__":
	dictx = metadataOS("test.jpg")._getdatamap()
	for i in dictx:
		print i + ":"+str(dictx[i])
	
