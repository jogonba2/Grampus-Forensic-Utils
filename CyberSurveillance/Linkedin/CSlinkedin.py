from linkedin import server
import webbrowser
class CSlinkedin:
	
	def __init__(self):
		API_KEY = ''
		API_SECRET = ''
		self.application = server.quick_api(API_KEY,API_SECRET)
		print self.application.search_profile(selectors=[{'people': ['first-name', 'last-name']}], params={'keywords': 'grampus'})
		print "\n+++++++++++++++++++++++++++++++++++++++++\n\n"
		self.__searchcompanies()
		
	def __searchcompanies(self):
		print self.application.search_company(selectors=[{'companies': ['name', 'universal-name', 'website-url']}], params={'keywords': 'grampus',"count":20})
		
		

CSlinkedin()
