import urllib2,base64,json
class crawlerbing():
	
	def __init__(self,search,extension="",typeSearch=None):
		self.search = search
		self.ext = extension
		self.typeSearch = typeSearch
		self.skipValue = 0
		self.urlDictionary = {}
		self.__switchExtension()
		self.__executeAuthentication()
		self.__executeSearch()
	
	def __switchExtension(self):
		
		if self.typeSearch==None:
			if self.ext!="":
				self.search = "site:"+self.search+"%20filetype:"+self.ext
			else:
				self.search = "site:"+self.search
		else:
			self.search = self.search
		
	def __executeAuthentication(self):
		
		self.request = urllib2.Request("https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%27web%27&Query=%27"+str(self.search)+"%27&$skip="+str(self.skipValue)+"&$format=json")
		user = "youruser"
		passwd = "yourpasswd"
		authentication = base64.encodestring("%s:%s" % (user,passwd)).replace("\n","")
		self.request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
		self.request.add_header("Authorization","Basic %s"%authentication)
		self.resultQuery = urllib2.urlopen(self.request)
		
	def __executeSearch(self):
		
		queryJson = json.load(self.resultQuery)
		# Append Dictionary
		j = 0
		countUrl = 0
		i = 0
		while j<3:
			while(i<=100):
				try:
					self.urlDictionary[countUrl] = str(queryJson["d"]["results"][0]["Web"][i]["Url"])
					countUrl += 1
				except:
					try:
						self.urlDictionary[countUrl] = str(queryJson["d"]["results"][0]["Web"][i]["DisplayUrl"])
						countUrl += 1
					except:
						pass
				i += 1
			
			self.skipValue += countUrl
			j += 1
			self.__executeAuthentication()
			
	def _returnUrls(self):
		return self.urlDictionary	

#General search: crawlerbing("http://pecsanjaime.es","")._returnUrls()
#Ext search: crawlerbing("http://pecsanjaime.es","pdf")._returnUrls()
