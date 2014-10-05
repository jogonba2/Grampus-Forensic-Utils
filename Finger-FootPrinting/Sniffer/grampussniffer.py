#from scapy.all import *
class grampussniffer():
	
	def __init__(self,limit,iface,filter=""):
		
		logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
		self.filter = filter
		self.limit = limit
		self.iface = iface
		self.hostSniffed = []
		self.SnifferSummary = []
		self.__startSniffer()
	
	# Init Sniffer depend if filter is selected or not
	def __startSniffer(self):
		
		self.finSniff = sniff(iface=self.iface,count=self.limit) if self.__selectedFilter==True else sniff(iface=self.iface,filter=self.filter,count=self.limit)
		self.__showDataHeaders()
		self.__showSummary()
		
	def __showDataHeaders(self):
		
		#Algunos hosts no poseen alguno de estos items por lo que provocan un excepcion y se crea un diccionario vacio. ARREGLAR
		numDictionary = 0
		for tcount in range(0,len(self.finSniff)):
			try:
				self.hostSniffed.append({})
				self.hostSniffed[numDictionary]["dst"] = self.finSniff[tcount].dst
				self.hostSniffed[numDictionary]["src"] = self.finSniff[tcount].src
				self.hostSniffed[numDictionary]["type"] = self.finSniff[tcount].type
				self.hostSniffed[numDictionary]["version"] = self.finSniff[tcount].version
				self.hostSniffed[numDictionary]["ihl"] = self.finSniff[tcount].ihl
				self.hostSniffed[numDictionary]["tos"] = self.finSniff[tcount].tos
				self.hostSniffed[numDictionary]["len"] = self.finSniff[tcount].len
				self.hostSniffed[numDictionary]["id"] = self.finSniff[tcount].id
				self.hostSniffed[numDictionary]["flags"] = self.finSniff[tcount].flags
				self.hostSniffed[numDictionary]["frag"] = self.finSniff[tcount].frag
				self.hostSniffed[numDictionary]["ttl"] = self.finSniff[tcount].ttl
				self.hostSniffed[numDictionary]["proto"] = self.finSniff[tcount].proto
				self.hostSniffed[numDictionary]["chksum"] = self.finSniff[tcount].chksum
				self.hostSniffed[numDictionary]["src"] = self.finSniff[tcount].src
				self.hostSniffed[numDictionary]["dst"] = self.finSniff[tcount].dst
				self.hostSniffed[numDictionary]["options"] = self.finSniff[tcount].options
				self.hostSniffed[numDictionary]["sport"] = self.finSniff[tcount].sport
				self.hostSniffed[numDictionary]["dport"] = self.finSniff[tcount].dport
				self.hostSniffed[numDictionary]["len"] = self.finSniff[tcount].len
				self.hostSniffed[numDictionary]["chksum"] = self.finSniff[tcount].chksum
				self.hostSniffed[numDictionary]["load"] = self.finSniff[tcount].load	
				numDictionary += 1
			except:
				continue
	
	# Hay que redireccionar la salida de summary a la tabla self.SnifferSummary
	def __showSummary(self):
		
		self.finSniff.summary()
	
	# Manage Filter Selection
	def __selectedFilter(self):
		
		if self.filter=="":
			return False
		else:
			return 
	
	def _resultSniffer(self):
		return self.hostSniffed,self.SnifferSummary
