#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile

class extractapk:
	
	def __init__(self,nameFile):
		self.datadict = {}
		self.__manageProcess(nameFile)
		
	def __unzipXml(self,nameFile):
		with zipfile.ZipFile(nameFile,"r") as zipApk:
			return zipApk.open("AndroidManifest.xml","r")


	def __manageProcess(self,nameApk):
		crudeText = ""
		i = 0
		xmlFile = self.__unzipXml(nameApk)
		xmlRead = xmlFile.read()
		lenXml = len(xmlRead)
		while i != (lenXml):
			if xmlRead[i].isalnum() or xmlRead[i] == "." or xmlRead[i] == "/": # module to goodChar
				if ord(xmlRead[i+1]) == 0 and ord(xmlRead[i+2]) == 0: # x <space><space>	 
					crudeText += xmlRead[i] + "\n"
				else:
					crudeText += xmlRead[i]	
			i += 1
		xmlFile.close()
		return self.__createDatadict(crudeText.rsplit("\n")) # str -> aux []

	def __createDatadict(crudeText):
		c = 0
		dataDict = {}
		for i in range (0,len(crudeText)):
			if len(crudeText[i]) > 2:
				dataDict["Field: " + str(c)] = crudeText[i]
				c += 1
		self.datadict = dataDict
	
	def _getDatadict(self):
		return self.datadict

#if __name__ == "__main__":
#	manageProcess("app.apk")._getdaDatadict()

