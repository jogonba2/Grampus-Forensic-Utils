from mmap import mmap
from struct import unpack

## exiftool -xmp-dc:subject=Metadatos XMP de prueba ./test.jpg ##
class jpegxmp:
	
	## 33 = 2B metadata section, 2B LP, 29B namespace -> start of packet ##
	def __init__(self,filename):
		self.mmaped = self.__mmap(filename)
		self.fst = self.__checkxmp()
		if self.fst != -1:
			print self.mmaped[self.fst+33:self.fst+self.__getsizepacket()-31]
		else:
			self.metadata = {}
			
	def __mmap(self,filename):
		with open(filename,"r+b") as fd:
			_ = mmap(fd.fileno(),0)
			fd.close()
			return _
	
	def __checkxmp(self):
		return "".join(unpack("c"*self.mmaped.size(),self.mmaped.read(self.mmaped.size()))).find("\xFF\xE1")
	
	## Testear el 133 ##
	def __getsizepacket(self):
		return unpack("h",self.mmaped[self.fst+1:self.fst+3])[0]-133
	## Section LP is 2+29+sizeofpacket -> sizeofpacket = |sectionLP + 31|
		
if __name__ == "__main__":
	
	inst = jpegxmp("test.jpg")

