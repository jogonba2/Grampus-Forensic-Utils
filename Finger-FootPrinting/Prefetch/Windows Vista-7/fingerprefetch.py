from mmap import mmap
from struct import unpack
from time import ctime

class fingerprefetch:
	
	def __init__(self,filename):
		self.mmaped = self.__mmap(filename)
		if self.__isvistaseven():
			self.doffset = self.__getblockdoffset()
			self.metadatamap = self.__getdictmetadata()
				
	def __mmap(self,filename):
		with open(filename,"r+b") as fd:
			_ = mmap(fd.fileno(),0)
			fd.close()
			return _

	def __isvistaseven(self):
		return True if unpack("I",self.mmaped[0:4])[0] == 23 else False
	
	## Offset 152 0x98, 4B Unsigned n launched ##
	def __getnumlaunched(self):
		return unpack("I",self.mmaped[152:156])[0]
	
	## Split spaces later ##
	def __getnameexecutable(self):
		unpacked = "".join(unpack("c"*60,self.mmaped[16:76]))
		return unpacked[:unpacked.find("\x00\x00\x00\x00")].replace("\x00","")
	
	##  0x0078 	8 	FTIME 	Latest execution time (or run time) of executable (FILETIME) ##
	def __getlastexecution(self):
		return ctime(unpack("d",self.mmaped[120:128])[0])
	
	"""  Section D - Volume information (block)
		 Section D contains one or more subsections. The number is (most likely) determined by the DWORD at file offset 0x0070. Each subsection refers to directories on an identified volume.
		 In this section, all offsets are assumed to be counted from the start of the D section. 
	"""
	## Block D Methods Volume information - version 17 ##
	
	## Get offset block D: H14 	0x006C 	4 	DWORD 	Offset to section D. The offset is relative from the start of the file.  ##
	def __getblockdoffset(self):
		return unpack("I",self.mmaped[108:112])[0]
	
	## DH1 	+0x0000 	4 	DWORD 	Offset to volume string (Unicode, terminated by U+0000) ##
	def __getvolumestringoffset(self):
		return unpack("I",self.mmaped[self.doffset:self.doffset+4])[0]
	
	## DH2 	+0x0004 	4 	DWORD 	Length of volume string (nr of characters, including terminating U+0000) ##
	def __getvolumestringlength(self):
		return unpack("I",self.mmaped[self.doffset+4:self.doffset+8])[0]
	
	## self.mmaped[getvolumestringoffset:getvolumestringoffset+getvolumestringlength] ##
	def __getvolumestring(self):
		vsoffset = self.__getvolumestringoffset()
		vslength = self.__getvolumestringlength()
		return unpack("c"*vslength,self.mmaped[vsoffset:vsoffset+vslength])
	
	## DH3 	+0x0008 	8 	FILETIME 	Volume creation time. ##
	def __getvolumecreationtime(self):
		return ctime(unpack("d",self.mmaped[self.doffset+8:self.doffset+16])[0])
	
	## DH4 	+0x0010 	4 	DWORD 	Volume serial number of volume indicated by volume string ##
	def __getvolumeserialnumber(self):
		return unpack("I",self.mmaped[self.doffset+16:self.doffset+20])[0]
	
	## General ##
	def __getdictmetadata(self):
		return {"Executable Name":self.__getnameexecutable(),
				"Num Executed":self.__getnumlaunched(),
				"Last Execution":self.__getlastexecution(),
				"Volume String":self.__getvolumestring(),
				"Volume Creation Time":self.__getvolumecreationtime(),
				"Volume Serial Number":self.__getvolumeserialnumber()
			   }
		
	def _getdatamap(self):
		for i in self.metadatamap:
			print i + ": " + str(self.metadatamap[i])	
		return self.metadatamap		 
								
#fingerprefetch("test.pf")._getdatamap()
