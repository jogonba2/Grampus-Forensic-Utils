import sys
sys.path.append("../../Crawlers/Bing/WAPI/")
from crawlerbing import crawlerbing
sys.path.append("../../Crawlers/Google/")
from crawlergoogle import crawlergoogle
class fingergrampushttp:
	
	def __init__(self,key,header):
		
		self.key = key
		self.header = header
		self.__selectUrls()
		
	def __searchUrls(self):	
		allUrls = {}
		allUrls.update(crawlergoogle(self.key,"",1)._returnUrls())
		allUrls.update(crawlerbing(self.key)._returnUrls())
		endUrls = {}
		for key in allUrls:
			endUrls[allUrls[key]] = ""
		return endUrls
	
	def __getHeaders(self,url):
		
		self.socketClient = socket.socket()
		try:
			#(socket.gethostbyname(self.__replacedUrl(url))
			self.socketClient.connect((self.__replacedUrl(url),80))
			self.socketClient.send("HEAD / HTTP/1.0\r\n\r\n")
			data = self.socketClient.recv(1024)
			return data
		except:
			return None
	
	def __getOptions(self,url):
		
		self.socketClient = socket.socket()
		try:
			self.socketClient.connect((self.__replacedUrl(url),80))
			self.socketClient.send("OPTIONS / HTTP/1.0\r\n\r\n")
			data = self.socketClient.recv(1024)
			indexAllow = data.find("Allow")
			data = data[indexAllow:data.find("\r\n",indexAllow)]
			return data
		except:
			return ""
	
	def __replacedUrl(self,url):
		url = url.replace("http://","")
		url = url[:url.find('/')]
		return url
			
	def __selectUrls(self):
		
		self.allUrls = self.__searchUrls()
		self.selectedUrls = {}
		for key in self.allUrls:
			try:
				self.allUrls[key] = self.__getHeaders(key)
				self.allUrls[key] += self.__getOptions(key)
				if self.header in self.allUrls[key]:
					self.selectedUrls[key] = self.allUrls[key]
			except:
				continue
	
	def _returnSelected(self):
		return self.selectedUrls
	
	def _returnAll(self):
		return self.allUrls
		
#print fingergrampushttp("futbol","IIS")._returnAll()
