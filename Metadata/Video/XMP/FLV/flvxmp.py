from mmap import mmap
from struct import unpack

## exiftool -xmp-dc:subject=Metadatos ./test.jpg ##
class flvxmp:
	
	def __init__(self,filename):
		self.mmaped = self.__mmap(filename)
		self.fst = self.__getmetadataheader()
		if self.fst != -1:
			print self.__getmetadatapayload(self.__getpacketsize())
			#self.parsemetadatakey(self.__getmetadatapayload(self.__getpacketsize()))

	def __mmap(self,filename):
		with open(filename,"r+b") as fd:
			_ = mmap(fd.fileno(),0)
			fd.close()
			return _
	
	"""
		Start of Last Packet 	uint32_be 	0 	For first packet set to NULL
		Packet Type 			uint8 		18 	For first packet set to AMF Metadata
		Payload Size 			uint24_be 	varies 	Size of packet data only
		Timestamp Lower 		uint24_be 	0 	For first packet set to NULL
		Timestamp Upper 		uint8 		0 	Extension to create a uint32_be value
		Stream ID 				uint24_be 	0 	For first stream of same type set to NULL
		Payload Data 			freeform 	varies 	Data as defined by packet type
	"""
	## Metatag -> 4 Null Bytes boundary, tag type = \x10, Timestamps (Lower and Upper) = 0 -> xmp in payload data
	## Pivoting by start of packet. It returns the initial pos of metadata header if it exists. This code can be used to
	## know if a file contains metadata.
	def __getmetadataheader(self):
		pos = self.mmaped.find("\x00\x00\x00\x00")
		while pos != -1:
			self.mmaped.seek(pos)
			## Check bytes 8-9-10 11 at the same time although they are from different tags. ##
			if self.mmaped[pos+4:pos+5]=="\x12" and unpack("cccc",self.mmaped[pos+8:pos+12]) == ("\x00","\x00","\x00","\x00"):
				return pos
			self.mmaped.seek(pos+5)
			pos = self.mmaped.find("\x00\x00\x00\x00")
		return pos

	def __getpacketsize(self):
		unpacked = unpack("ccc",self.mmaped[self.fst+5:self.fst+8])
		thx,trd = hex,ord
		return int("".join([thx(trd(x)) for x in unpacked]).replace("0x",""),16)
		
	def __getmetadatapayload(self,sizeofpacket):
		metadatapayload = self.mmaped[self.fst+15:self.fst+sizeofpacket+15]
		tstr = ""
		for i in metadatapayload:
			try:
				tstr += i.encode("utf-8")
			except:
				continue
		return tstr
if __name__ == "__main__":
	inst = flvxmp("test.flv")
