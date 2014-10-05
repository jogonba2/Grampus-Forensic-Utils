import re,urllib2,os

class crawlergrampus1:
	
	def __init__(self,url,totalResults,isIndex):
		###################################	
		self.initialCount = 0
		self.isIndex = isIndex
		self.url = url
		# Add more regExp -> list
		self.regExp = "(.*?)<a(.*?)href(.*?)=(.*?)[\"\'](.+?)[\"\'](.*?)"
		self.urlsCrawled = []
		self.otherInfo = {"Robots":"","CMS":"","Listing":""}

		####################################	
		self.__initOpener()
		if isIndex==True:
			self.__searchRobots()
			self.__searchCMS()
		self.__searchListing()
		self.__openUrl2Crawl(self.url)
		self.returnUrls()
	
	def __initOpener(self):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"),
								  ("Host",self.url),("Referer:",self.url)]
	def __searchRobots(self):
		
		urlRobots = self.url+"/robots.txt"
		try:
			robotsRead = self.opener.open(urlRobots).read()
			if "User-agent" in robotsRead:
				self.urlsCrawled.append(urlRobots)
			self.otherInfo["Robots"] = robotsRead
		except:
			self.otherInfo["Robots"] = "None"
			pass
		self.__resetConnection() # Reseteamos Conexion para seguir con el crawleo
	
	def __searchCMS(self):
		
		read = self.opener.open(self.url).read()
		if "joomla" in read:
			self.otherInfo["CMS"] = "Joomla"	
		elif "WordPress" in read:
			self.otherInfo["CMS"] = "Wordpress"		
		elif "drupal" in read:
			self.otherInfo["CMS"] = "Drupal"
		elif "Smf" in read:
			self.otherInfo["CMS"] = "SMF"
		elif "phpbb" in read:
			self.otherInfo["CMS"] = "PhpBB"
		elif "vbulletin" in read:
			self.otherInfo["CMS"] = "vBulletin"
		elif "ipb" in read:
			self.otherInfo["CMS"] = "Ip Board"
		else:
			self.otherInfo["CMS"] = "NoN Cms"
		self.__resetConnection() # Reseteamos Conexion para seguir con el crawleo
	
	def __searchListing(self):
		
		if self.url[len(self.url)-1]=="/":
			url2Listing = self.url+".listing"
		else:
			url2Listing = self.url+"/.listing"
		try:
			read = self.opener.open(url2Listing).read()
			if "drwx" in read:
				self.urlsCrawled.append(url2Listing)
				self.otherInfo["Listing"] = read
		except:
			pass
		self.__resetConnection()
		
	
	def __resetConnection(self):
		
		self.opener.close()
		self.__initOpener()
		
	def __openUrl2Crawl(self,url):
		
		try:
			self.url2Crawl =  self.opener.open(url)
			self.__matchRegExp()
		except:
			pass
		
	def __matchRegExp(self):
		
		for linea in self.url2Crawl.readlines():
			regExpMatch = re.match(self.regExp,linea.strip().lower())
			self.__execComprobation(regExpMatch)			
	
	# Add in this method conditions to add new urls
	def __execComprobation(self,regExpMatch):
		
		if regExpMatch!=None and "http://" not in regExpMatch.group(5) and "/" not in regExpMatch.group(5) and "javascript" not in regExpMatch.group(5) and regExpMatch.group(5) not in self.urlsCrawled:				
			self.urlsCrawled.append(self.url+"/"+regExpMatch.group(5))
			self.initialCount += 1
		elif regExpMatch!=None and "http://" not in regExpMatch.group(5) and "/" in regExpMatch.group(5) and "javascript" not in regExpMatch.group(5) and regExpMatch.group(5) not in self.urlsCrawled:
			self.urlsCrawled.append(self.url+regExpMatch.group(5))
			self.initialCount += 1
		elif regExpMatch!=None and self.url in regExpMatch.group(5) and regExpMatch.group(5) not in self.urlsCrawled:
			self.urlsCrawled.append(regExpMatch.group(5))	
			self.initialCount += 1
	
	def returnUrls(self):	

		try:
			htmlSource = """<!DOCTYPE html><html><title>| Grampus Crawler |</title><head>
						<link rel=\"stylesheet\" type=\"text/css\" href=\"CSS.css\">
						<style type=\"text/css\">body {background-color: #356AA0 }
						div#menu {text-align: center; background-color: #C3D9FF; float: left;
						text-decoration: none;color: #666;width: 200px;border: solid #F9F7ED;}
						div#menu a:hover {background:none;text-decoration: underline;color:#fff;
						text-decoration:none;} div#links {background-color: #C3D9FF;width: 650px;
						font:bold 12px \"Trebuchet MS\";color: black; height: auto;float: center;text-align: center;
						margin: 0 auto;color: #666;border-bottom: 40px;padding: 40px;border: solid #F9F7ED;}
						div#footer {background-color: #C3D9FF;width: 800px;font:bold 12px \"Trebuchet MS\";text-align: center;
						margin: 0 auto; margin-top: 40px; border: solid #F9F7ED; color: #666;}</style>
						<center><img src=\"http://www.image-share.com/upload/2052/46.png\"></center></head><body>
						<div id=\"menu\"><nav><a href=\"/1\">Links</a><br> <a href=\"/2\">Robots</a><br><a href=\"/3\">Listing</a><br>
						<a href=\"/4\">CMS</a><br></div><div id=\"links\">"""
	
			if len(self.urlsCrawled) != 0:
				dumpCrawl = open(self.url.replace(".","").replace("://","").replace("-","").replace("/","")+".html","w")
				#dumpCrawl.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"""/><title>Dump Crawl</title></head><body bgcolor=#000000><header><div align=\"center\"><img src=\"http://www.image-share.com/upload/2052/46.png\"/></div></header><div align=\"center\">This web is Index<section>")
				dumpCrawl.write(htmlSource)
				for url in self.urlsCrawled:
					dumpCrawl.write("<article><header><a href=\""+url+"\">"+url+"</a></header></article><br>\r\n")
				try:
					for infoName in self.otherInfo:
						dumpCrawl.write("<br><br><header><h3><b>----> "+infoName+" <----</b></h3></header><br>")
						dumpCrawl.write(self.otherInfo[infoName])
				except:
					pass
				dumpCrawl.write("</div><div id=\"footer\">Generated by Grampus</div></body></html>")			
				dumpCrawl.close()
			return self.urlsCrawled				
		except:
			pass 

class crawlermanager:
	
	def __init__(self,url2Crawl):
		
		self.yaIniciado = False
		self.isIndex = True # Evitar rebusqueda de robots.txt
		self.url2Crawl = url2Crawl
		newDir = self.url2Crawl.replace("http://","").replace(".","").replace("/","").replace("www","")
		os.mkdir(newDir)
		os.chdir(newDir)
		self.__configure()
		
	def __configure(self):
		
		self.manager = crawlergrampus1(self.url2Crawl,1000,self.isIndex)
		self.isIndex = False
		self.crawledList = []
		self.__loopCrawler()

	def __loopCrawler(self):	
		
		for urlCrawled in self.manager.returnUrls():
			try:
				if urlCrawled not in self.crawledList:
					self.crawledList.append(urlCrawled)
			except:
				continue
		if self.yaIniciado == False:
			self.__resetManagement()
					
	def __resetManagement(self):
	
		self.yaIniciado = True
		try:
			for urlCrawled in self.crawledList:
				self.url2Crawl = urlCrawled
				self.__configure()
		except:
			pass

#crawlermanager("http://marca.com")
