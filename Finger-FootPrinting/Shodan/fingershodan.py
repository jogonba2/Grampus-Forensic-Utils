from shodan import WebAPI
from shodan.wps import GoogleLocation
import socket
class fingershodan:
	
	def __init__(self,search,typeSearch):		
		self.search = search
		self.typeSearch = typeSearch
		self.searchList = {}
		self.allCount = 0
		self.__initKey()
		self.__switchSearch()
		
	def __initKey(self):
			self.api = WebAPI("CvXzhcMm3YemfeNnNKE7ed9xRSCKfAhY")
				
	def __switchSearch(self):
		if self.typeSearch=="search":
			self.__execSearch()
		elif self.typeSearch=="lookup":
			self.search = socket.gethostbyname(self.search)
			self.webHost = self.api.host(self.search)
			self.__execLookup()
		#elif self.typeSearch=="mac":
		#	self.__macLocation()
			
	
	def __execSearch(self):
		searched = self.api.search(self.search)
		for search in searched["matches"]:
			try:
				self.searchList["Result "+str(self.allCount)] = {"Ip":search["ip"],"Updated":search["updated"],
				"Country":search["country_name"],"Latitude":search["latitude"],"Longitude":search["longitude"],
				"Port":search["port"],"Data":search["data"],"Os":search["os"]}
				self.allCount += 1
			except:
				continue
	
	def __execLookup(self):
		try:
			self.searchList["Result "+str(self.allCount)] = {"Ip":self.webHost["ip"],"Country":self.webHost["country_name"],"City":self.webHost["city"],
			"Os":self.webHost["os"],"Banner":self.webHost["data"][0]["banner"],"Port":self.webHost["data"][0]["port"],
			"TimeStamp":self.webHost["data"][0]["timestamp"]}
		except:
			print "Fail Lookup"
	
	#def __macLocation(self):

		
	def _returnData(self):
		return self.searchList
