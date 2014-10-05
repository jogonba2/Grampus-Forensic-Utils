import gif
class extractgif:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		try:
			self.gifFile = gif.GifInfo(self.pathFile)
			self.dirMetaData = {"Version":self.gifFile.version,"Width":self.gifFile.width,
								"Height":self.gifFile.height,"LoopCount":self.gifFile.loopCount,"PixelAspect":self.gifFile.pixelAspect,
								"PaletteSize":self.gifFile.paletteSize,"BgColor":self.gifFile.bgColor,
								"Comments":self.gifFile.comments,"Text":self.gifFile.otherText}
		except:
			self.dirMetaData = {"Error":"Isn't a valid GIF"}
					
	def _extract(self):
		
		return self.dirMetaData

print extractgif("test.gif")._extract()
