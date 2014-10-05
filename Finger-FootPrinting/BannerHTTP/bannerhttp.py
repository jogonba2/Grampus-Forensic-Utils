import httplib
class bannerhttp:
	
	def __init__(self,url):
		self.url = url.replace("http://","")
		self.infoDict = {}
		self.__httpConnect()
		self.__httpRequest()
		
	def __httpConnect(self):
		try:
			self.connect = httplib.HTTPConnection(self.url)
		except:
			self.infoDict = {"Error":"No Connected"}
			return self.infoDict
			
	def __httpRequest(self):
		
		for method in ("HEAD"):
			try:
				self.connect.request(method,"/")
				self.response = self.connect.getresponse()
				self.__httpResponse()
				break;
			except:
				self.connect.close()
				self.__httpConnect()
				continue
	
	def __httpResponse(self):
			auxDict = {}
			for responsex in self.response.getheaders():
				try:
					auxDict[responsex[0]] = responsex[1]
				except:
					continue
			self.infoDict = auxDict
	
	def _returnDictionary(self):
		return self.infoDict
		
print bannerhttp("hackplayers.com")._returnDictionary()
