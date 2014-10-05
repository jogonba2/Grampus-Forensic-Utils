#from zipfile import ZipFile, is_zipfile
import zipfile,os
class cleanoffi2007:
	
	def __init__(self,fileName):
		self._ms_do(fileName, (fileName[0:fileName.rfind('.')]+"CLEANED"+fileName[fileName.rfind('.'):]))

	def _ms_do(self, sDocName, newDocName):
		self.sDocName = sDocName
		self.newDocName = newDocName
		self.ErrorDic = {}
		try:
			self.__uncompress()
		except:
			self.ErrorDic['Error'] = 'An error has ocurred uncompressing'
		try:
			self._xml_cleaner()
		except:
			self.ErrorDic['Error'] = 'An error has ocurred cleaning metadata'

		self.__compress()
		self._meta_adder()
		self._image_manag()
		try:
			os.remove(self.sDocName)
			os.rename(self.newDocName, self.sDocName)
		except:
			self.ErrorDic['Error'] = 'An error has ocurred writing the file'


	def __uncompress(self):
		#Uncompressing core.xml and app.xml to edit metadata
		if not zipfile.is_zipfile(self.sDocName):
			return False
		buff = zipfile.ZipFile(self.sDocName, 'r')
		for i in buff.namelist():
			if i in ('docProps/core.xml', 'docProps/app.xml'):
				filename = os.path.basename(i)
				source = buff.open(i)
				target = file(os.path.join(filename), 'wb')
				copyfileobj(source, target)
				source.close()
				target.close()
		return True

	def _xml_cleaner(self):
		#parsing core.xml to replace the values
		core = parse(os.path.join('core.xml'))
		corelist = ['dc:creator', 'dc:title', 'cp:lastModifiedBy', 'cp:revision',
					'dcterms:created', 'dcterms:modified', 'cp:lastPrinted']
		for i in corelist:
			try:
				core.getElementsByTagName(i)[0].childNodes[0].nodeValue = ""
			except:
				continue
		#saving
		f = open(os.path.join('core.xml'), 'w')
		core.writexml(f)
		f.close()
		#parsing app.xml to replace values
		app = parse(os.path.join('app.xml'))
		applist = ['Application', 'Company']

		for x in applist:
			try:
				app.getElementsByTagName(x)[0].childNodes[0].nodeValue = ""
			except:
				continue
        #saving
		j = open(os.path.join('app.xml'), 'w')
		app.writexml(j)
		j.close()

	def __compress(self):
        #creating the new doc
		zf = zipfile.ZipFile(self.sDocName, 'r')
		zp = zipfile.ZipFile(self.newDocName, 'w')
		try:
			for item in zf.infolist():
				buffer = zf.read(item.filename)
				#core and app .xml will be joined later in meta_adder func
				if (item.filename[-8:] != 'core.xml') and (item.filename[-7:] != 'app.xml') and (item.filename[-5:] != '.jpeg'):
					zp.writestr(item, buffer)
			zf.close()
			zp.close()
		except:
			self.ErrorDic['Error'] = "compressing error"

	def _meta_adder(self):
    #joining core and app.xml
		zf = zipfile.ZipFile(self.newDocName, 'a')
		try:
			zf.write('core.xml')
			zf.write('app.xml')
			zf.close()
		except:
			self.ErrorDic['Error'] = "error in writting"
        #removing core and app .xml because it's already joined
		os.remove('core.xml')
		os.remove('app.xml')


#adding another functions to clean exif metadata from the images where are into the 2007 office documents

	def __img_uncompress(self):
		buff = zipfile.ZipFile(self.sDocName, 'r')
		for name in buff.namelist():
			#we must to add another extensions
			if (name.find('.jpeg')!= -1):
				buff.extract(name)

	def _img_meta_extractor(self):
		ext = self.sDocName[self.sDocName.rfind('.'):]
		if ext == '.docx':
			images = os.listdir('word/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('word/media/%s'%(i), "word/media/image%s.jpg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			images = os.listdir('word/media/')
			var = 0
			while (var<5):
				for x in images:
					obj = Exif.clean_EXIF('word/media/%s'% x)
				var = var+1
		
		elif ext == '.pptx':
			images = os.listdir('ppt/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('ppt/media/%s'%(i), "ppt/media/image%s.jpg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			images = os.listdir('ppt/media/')
			var = 0
			while (var<5):
				for x in images:
					obj = Exif.clean_EXIF('ppt/media/%s'% x)
					var = var+1

		elif ext == '.xlsx':
			images = os.listdir('xl/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('xl/media/%s'%(i), "xl/media/image%s.jpg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			images = os.listdir('xl/media/')
			var = 0
			while (var<5):
				for x in images:
					obj = Exif.clean_EXIF('xl/media/%s'% x)
				var = var+1

	def _adder(self):
        #before to add the cleaned images into the document
        #we must to change the ext again
		var = self.sDocName[self.sDocName.rfind('.'):]
		if var == '.docx':
			images = os.listdir('word/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('word/media/%s'%(i), "word/media/image%s.jpeg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			zf = zipfile.ZipFile(self.newDocName, 'a')
			images = os.listdir('word/media/')
			for x in images:
				try:
					zf.write('word/media/%s'% x)
				except:
					self.ErrorDic['Error'] = "error in Writing"
					sys.exit(0)
			zf.close()
			rmtree('word/')

		if var == '.pptx':
			images = os.listdir('ppt/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('ppt/media/%s'%(i), "ppt/media/image%s.jpeg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue
			zf = zipfile.ZipFile(self.newDocName, 'a')
			images = os.listdir('ppt/media/')
			for x in images:
				try:
					zf.write('ppt/media/%s'% x)
				except:
					self.ErrorDic['Error'] = "error in Writing"
					sys.exit(0)
			zf.close()
			rmtree('ppt/')

		if var == '.xlsx':
			images = os.listdir('xl/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('xl/media/%s'%(i), "xl/media/image%s.jpeg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue
			zf = zipfile.ZipFile(self.newDocName, 'a')
			images = os.listdir('xl/media/')
			for x in images:
				try:
					zf.write('xl/media/%s'% x)
				except:
					print "error in Writing"
					sys.exit(0)
			zf.close()
			rmtree('xl/')

	def _image_manag(self):
		self.__img_uncompress()
		self._img_meta_extractor()
		self._adder()

cleanoffi2007("test.docx")
