import threading,sys
global d_global,mutex
d_global = {}
mutex = threading.Semaphore(10)
sys.path.append("../../../Core/")
from core import core

## Thread receives, the id of the thread, complete list, url to search, total n of threads, funct to execute in the thread ##
class genericthread(threading.Thread):
	
	def __init__(self,idthread,lst,url,nlist,nthread,functhread):
		threading.Thread.__init__(self)
		self.idthread = idthread
		self.tot = nlist / nthread
		self.ttable = lst[self.tot*(idthread-1):self.tot*idthread]
		self.url = url
		self.functhread = functhread
	
	def run(self):
		for i in range(0,len(self.ttable)):
			## Check which function is called to tight the name of key in dictionary ##
			self.keyname = self.ttable[i]+"."+self.url if "core._existsubdomain" in str(self.functhread) else self.url+"/"+self.ttable[i]
			auxt = self.functhread(self.url,self.ttable[i])
			## Entry Protocol ##
			mutex.acquire()
			## Critic Section ##
			d_global[self.keyname] = auxt
			## Exit Protocol ##
			mutex.release()

class genericfinger:
	
	# pathlst : full path of juicyfiles
	def __init__(self,url,pathlst,funct):
		self.juicytemp = pathlst
		self.funct = funct
		self.juicyfiles = self.__getjuicyfiles(url)	
		
	def __getjuicyfiles(self,url):	
		threadlst = self.__initializethreads(url)
		self.__jointhreads(threadlst)
		return d_global
	
	def __getversion(self,funcversion,*params):
		d_global["Version"] = funcversion(params)
		pass
	
	def __getplugins(self,funcversion,*params):
		d_global["Plugins"] = funcversion(params)
		pass	
	
	## idthread,lst,mutex,url
	## ids: 1..10 threads max
	## Thread Section ##
	def __initializethreads(self,url):
		threadlst = []
		nlist = len(self.juicytemp)
		for i in range(1,11):
			threadlst.append(genericthread(i,self.juicytemp,url,nlist,10,self.funct))
			threadlst[i-1].start()
		return threadlst
	
	def __jointhreads(self,threadlst):
		for i in range(1,11):
			threadlst[i-1].join()
