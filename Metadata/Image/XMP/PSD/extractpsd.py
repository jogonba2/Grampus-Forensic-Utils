#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from struct import pack,unpack
from mmap import mmap


def grampus_modulo():
	return ("ext", mainPSD, ("psd",))
	
def mainPSD(nFile):
	xmlData = mapFile(nFile,500)
	return parseXml(xmlData[xmlData.find(">")+1:])#parseXml(mapFile(nFile,500))

def parseXml(xmlData):
	xmlData = xmlData.split("\n") # lines
	info = {}
	for lne in xmlData:
		header = lne[lne.find(":")+1:lne.find(">")].strip()
		info[header] = lne[lne.find(">")+1:lne.rfind("<")].strip()
	return info

# Find patterns in size of psd's to pre-know how many nulls form the boundary
# Predefined 500 (in main)
def mapFile(nFile,countNulls):
    try:
		with open(nFile,"r+b") as fd:
			mm = mmap(fd.fileno(),0)
			xmlData = ""
			xmlAux = ""
			countNull = 0
			for _ in range(0,mm.size()):
				if countNull <= countNulls:
					mm.seek(_)
					xmlAux = unpack('c',mm.read(1))[0]
					xmlData += xmlAux
					countNull = (countNull+1) if xmlAux == " " else countNull
				else: break
			xmlData = xmlData.strip()
			mm.close()
			fd.close()
		return xmlData
    except IOError as e:
		print >> stderr, "File cannot be opened!"
		exit()
    except ValueError as e:
		print >> stderr, "mmap offset bigger than file size!"
		exit()
	# More general
    except Exception as e:
		print >> stderr, e
		exit()
