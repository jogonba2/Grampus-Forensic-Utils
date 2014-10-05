from mmap import mmap
from struct import unpack

## exiftool -xmp-dc:subject=Metadatos ./test.jpg ##

class jpeg2000xmp:
	
	## [self.fst+16] -> pivot at \xBE, +16B which contains this UUID header = init of xmp packet
	## [self.__getsizepacket()] -> getsizepacket = totalblock - 4B - 4B - 16B
	def __init__(self,filename):
		self.mmaped = self.__mmap(filename)
		self.fst = self.__checkxmp()
		if self.fst != -1:
			self.xml = self.mmaped[self.fst+16:self.__getsizepacket()]
			
	def __mmap(self,filename):
		with open(filename,"r+b") as fd:
			_ = mmap(fd.fileno(),0)
			fd.close()
			return _
	
	## 4B size (unsigned integer big endian which contains size of all packet including the size of the size block)
	## 4B header uuid 0x75756964 (unsigned integer big endian)
	## 16B UUID header value defined by ISO IEC:11578:1996 (BE 7A CF CB 97 A9 42 E8 9C 71 99 94 91 E3 AF AC)
	## Test reading unsigned integer offset 4
	def __checkxmp(self):
		return "".join(unpack("c"*self.mmaped.size(),self.mmaped.read(self.mmaped.size()))).find("\xBE\x7A\xCF\xCB")
	
	## To read the size of packet, it's necessary to move to init of packet. Pivot -> UUID Header -> -8 = Init of block
	def __getsizepacket(self):
		return unpack(">I",self.mmaped[self.fst-8:self.fst-4])[0]
		
if __name__ == "__main__":
	inst = jpeg2000xmp("test.jpg")
