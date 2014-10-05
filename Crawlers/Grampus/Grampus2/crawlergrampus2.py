import re,urllib2
class crawlergrampus2():

    def __init__(self, Url, Profundidad, ext=""):
        self.Url = Url
        self.Profundidad = Profundidad
        AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        REFERER = Url
        self.ext = ext
        self.limit = 0
        EXPRESION = ".*?<a href.?=.?[\"\'](.*?)[\"\'].*?>"
        
        self.Regular = re.compile(EXPRESION, re.I)
        self.Crawled = []
        self.Crawl = [Url]
        self.Encontrados = []
        self.containsAll = {}
        self.fullDictionary = {}
        self.count = 0
        self.Cantidad = 0
        
        self.Opener = urllib2.build_opener()
        self.Opener.addheaders = [("User-Agent", AGENT), ("Host", Url), ("Referer", REFERER)]
        self.Crawler(self.Profundidad)
    
    def _returnUrls(self):
		if self.ext=="":
			return self.containsAll
		else:
			try:
				auxDictionary = {}
				self.count = 0
				for urlCrawled in self.containsAll:
					if urlCrawled[urlCrawled.rfind('.'):] in self.ext:
						auxDictionary[self.count] = urlCrawled
						self.count += 1
			except:
				pass
			return auxDictionary
		
    
    def Limpiar(self, Link):
        Buff = None
        for i in Link:
            if i.split(".")[-1] in self.ext:
				if not i in self.Encontrados:
				    self.Encontrados.append(i)
				    self.Cantidad += 1
                    #print len(self.Encontrados), "Encontrados"
            else:
                if i.startswith('/'):
                    Buff = self.Url + i
                elif i.startswith(self.Url):
                    Buff = i
                else:
                    if not i.startswith("http://")or not i.startswith("#"):
                        Buff = self.Url + "/" + i
                if not Buff == None:
                    if not Buff in self.Crawled:
                        self.Crawl.append(Buff)

    def Crawler(self, Profundidad):
        #print len(self.Crawl), "A revisar"
        if Profundidad > 0:
            for i in self.Crawl:
				if self.limit >= 100:
					break;
				self.limit += 1
				self.Abrir(i)
				try:
					self.Crawler(Profundidad - 1)
				except:
					continue
		
    
    def Abrir(self, Url):
        if Url in self.Crawled:
		    self.Crawl.remove(Url)
		    return
        #print "Abriendo", Url
        try:
			self.containsAll[self.count] = Url
			self.count += 1
			Data = self.Opener.open(Url).read()
			Links = self.Regular.findall(Data)
			self.Crawled.append(Url)
			self.Crawl.remove(Url)
			self.Limpiar(Links)
        except:
			pass

# crawlergrampus2("http://pecsanjaime.es",1,"pdf")._returnUrls()
