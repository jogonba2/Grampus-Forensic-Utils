from mmap import mmap

## exiftool -xmp-dc:subject=Metadatos XMP de prueba ./test.gif ##

class gifxmp:
	
	def __init__(self,filename):
		self.mmaped = self.__mmap(filename)
		self.fst = self.__checkxmp()
		if self.fst != -1:
			self.xml = self.__loadxmppacket()
			print self.xml
		## dict = ModuleXML.parsexmp(self.xml) ##
			
	def __mmap(self,filename):
		with open(filename,"r+b") as fd:
			_ = mmap(fd.fileno(),0)
			fd.close()
			return _
	
	## Comprueba que el header es correcto, solo se comprobara la existencia de 
	## unos cuantos caracteres clave en el hader, si es correcto, devuelve el indice
	## de la primera aparicion de XMP en la cabecera. Se pivotara a partir de aqui
	def __checkxmp(self):
		return self.mmaped.find("XMP Data")
	
	## Leemos el paquete, boundary primera ocurrencia del header + 12 bytes de la comprobacion, hasta el mismo + 256 
	## 256 -> (258 - 2 bytes del block terminate)
	def __loadxmppacket(self):
		blcktrmt = self.mmaped.find("\x00\x00",self.fst,self.mmaped.size())
		return self.mmaped[self.fst+11:blcktrmt-256]
					
if __name__ == "__main__":
	inst = gifxmp("test.gif")
