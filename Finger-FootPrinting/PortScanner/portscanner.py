#from scapy.all import *
class portscanner:
	
	def __init__(self,dnsIp):
				
		self.dnsIp = dnsIp
		self.portFirewall = {}
		self.statusPort = {}
		self.__scanPFilter()
		self.__portStatus()
		self.__showPortStatus()
	
	def __scanPFilter(self):	
		
		for port in range(0,30): 
			resp,uresp = sr(IP(dst=self.dnsIp)/TCP(dport=[port],flags="A"),timeout=0.1) 
			if len(resp) != 0: 
				for s,r in resp:
					if s[TCP].dport==s[TCP].sport: 
						self.portFirewall[port] = False
					else:
						self.portFirewall[port] = True
			else: 
				self.portFirewall[port] = True
	
	def __portStatus(self): # XMAS Scan

		for port in self.portFirewall:
			resp,uresp = sr(IP(dst=self.dnsIp)/TCP(dport=port,flags="FPU"),timeout=0.1)
			if len(resp) != 0:
				for s,r in resp:
					if s[TCP].dport==s[TCP].sport:
						self.statusPort[port] = "Open"
					else:
						self.statusPort[port] = "Close"
			else:
				self.statusPort[port] = "Close"
	def __showPortStatus(self):
		
		# Clear Window
		if os.name=="nt":
			os.system("cls")
		else:
			os.system("clear")
			
		# Show Status	
		print "-- If port is filtered the status may not be reliable --\n"
		for port in self.statusPort:
			if self.portFirewall[port]:
				print "Port Filtered: " + str(port) + "  " + self.statusPort[port]
			else:
				print "Port NoN Filtered: " + str(port) + "  " + self.statusPort[port]
