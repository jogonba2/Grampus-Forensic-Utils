from mmap import mmap
from struct import unpack

## exiftool -xmp-dc:subject=Metadatos XMP de prueba ./test.png ##

class pngxmp:
	
	def __init__(self,filename):
		self.mmaped = self.__mmap(filename)
		self.fst = self.__checkxmp()
		if self.fst != -1:
			self.xml = self.__loadxmppacket(self.__getsizepacket())
			
	def __mmap(self,filename):
		with open(filename,"r+b") as fd:
			_ = mmap(fd.fileno(),0)
			fd.close()
			return _
	
	## Se pivota a partir de la primera ocurrencia de iTXt ##
	def __checkxmp(self):
		return self.mmaped.find("iTXt")
	
	def __getsizepacket(self):
		return unpack("i",self.mmaped[self.fst-5:self.fst-1])[0]
	
	## Boundary -> 17B keyword + 4Bytes due to the fact of situate the pointer at Chunk Type + 5B (Null separator
	## compression flag, compression method, language tag, Null separator) ##
	def __loadxmppacket(self,size):
		return self.mmaped[self.fst+26:size]
	
	## Parse XML ##
				
		
if __name__ == "__main__":
	inst = pngxmp("test.png")
