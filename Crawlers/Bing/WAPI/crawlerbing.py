import urllib2,re
class crawlerbing:
	
	def __init__(self,search):
		self.search = search
		self.urlSearch = "http://www.bing.com/search?q="+self.search+"&first="
		self.dictUrls = {}
		self.__searchWebs()
	
	def __searchWebs(self):
		
		count = 0
		indexDict = 0
		while(count<=200):
			urlOpen = urllib2.urlopen(self.urlSearch+str(count))
			urlRead = urlOpen.read()
			for url in re.findall("<h3><a href=\"(.*?)\"",urlRead,re.I):
				if "r.msn" not in url:
					self.dictUrls[indexDict] = url
					indexDict += 1
			count += 10
			urlOpen.close()
	
	def _returnUrls(self):
		
		return self.dictUrls

#crawlerbing("http://pecsanjaime.es")._returnUrls()
