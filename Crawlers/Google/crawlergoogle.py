import urllib2,json

class crawlergoogle:
	
	def __init__(self,url,ext="",typeSearch=None):
		
		self.url = url
		self.ext = ext
		self.typeSearch = typeSearch
		self.search = ""
		self.startCount = 0
		self.filesWithExt = {}
		self.allCount = 0
		self.__switchFunction()
	
	def __switchFunction(self):
		
		if self.typeSearch==None:
			if self.ext!="":
				self.search = "q=inurl:"+self.url.replace("http://","//")+"+and+ext:"+self.ext
			else:
				self.search = "q=site:"+self.url
		else:
			self.search = "q=intext:"+self.url
		self.__extractUrls()
		
	def __extractUrls(self):
		
			# Coste cuadratico en peor caso n->inf, intentar reducir.
			while(True):
				try:
					# Proxy: &userip=53.22.11.65 (EJ)
					self.url2Crawl = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"+self.search+"&start="+str(self.startCount)+"&rsz=large"
					connect_url2Crawl = urllib2.urlopen(self.url2Crawl)
					urls_Ext = json.load(connect_url2Crawl)
					urls_Json = urls_Ext["responseData"]["results"]
					for url_Extracted in urls_Json:
						self.filesWithExt[self.allCount] = url_Extracted["url"]
						self.allCount += 1
					connect_url2Crawl.close()
					self.startCount += 8
				except:
					break;

	def _returnUrls(self):

		return self.filesWithExt
		
# General search: crawlergoogle("pecsanjaime.es","")._returnUrls()
# Search by ext: crawlergoogle("pecsanjaime.es","pdf")._returnUrls()
