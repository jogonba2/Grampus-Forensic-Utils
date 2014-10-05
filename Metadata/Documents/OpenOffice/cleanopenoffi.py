from tempfile import mkdtemp
from zipfile import ZipFile, is_zipfile
from shutil import rmtree, copyfileobj
from xml.dom.minidom import parse
import os
class cleanopenoffi():

    def __init__(self, sDocName, newDocName):
	self.sDocName = sDocName
        self.newDocName = newDocName
        self._ms_do()
		
    def _ms_do(self):
     
        #uncompressing
        if self.__uncompress():
            #cleaning xml files
            self._xml_cleaner()
            self._xml_extra_cleaner()
            #compressing , adding and deleting
            self.__compress()
            self._meta_adder()
        else:
            print "An error has ocurred uncompressing"
            sys.exit(0)


    def __uncompress(self):
        #uncompressing metadata containers
        if not is_zipfile(self.sDocName):
            return False
        buff = ZipFile(self.sDocName, 'r')
        for i in buff.namelist():
            if i in ('meta.xml', 'content.xml', 'settings.xml'):
                filename = os.path.basename(i)
                source = buff.open(i)
                target = file(os.path.join(filename), 'wb')
                copyfileobj(source, target)
                source.close()
                target.close()
        return True

    def _xml_cleaner(self):
        dom = parse(os.path.join('meta.xml'))
        metalist = ['meta:creation-date',
                    'dc:date',
                    'meta:editing-cycles',
                    'meta:editing-duration',
                    'meta:generator',
                    'dc:title',
                    'dc:description',
                    'meta:keyword',
                    'dc:language',
                    'meta:initial-creator',
                    'dc:creator']

        #cleaning tags values
        for i in metalist:
            try:
                for a in dom.getElementsByTagName(i):
                    a.childNodes[0].nodeValue = ""
            except:
                print "Error, tagname not found"
                sys.exit(0)
        #Saving in meta.xml
        f = open(os.path.join('meta.xml'), 'w')
        dom.writexml(f)
        f.close()

    def _xml_extra_cleaner(self):
        #cleaning tags values in content.xml
        content = parse(os.path.join('content.xml'))
        content_tag = content.getElementsByTagName("text:a")
        for node in content_tag:
            try:
                node.setAttribute('xlink:href', str(''))
            except:
                print "Error, tagname not found"
                sys.exit(0)

        f = open(os.path.join('content.xml'), 'w')
	content.writexml(f)
	f.close()

        #cleaning tags values in settings.xml(WILL MUST CORRECT IT)
        #PENDING A FIX FOR IT(when we have more time)
        """
        settings = parse(os.path.join('settings.xml'))
        settings_tag = settings.getElementsByTagName("config:config-item")
        for another_node in settings_tag:
            try:
               another_node.setAttribute('config:name', str(''))
            except:
               print "An error has ocurred, but not is very important, you can continue"

        j = open(os.path.join('settings.xml'), 'w')
        settings.writexml(j)
        j.close()
        """

    def __compress(self):
        zf = ZipFile(self.sDocName, 'r')
        zp = ZipFile(self.newDocName, 'w')

        for item in zf.infolist():
            try:
                #triying to write a new document without meta,content & settings .xml
                buffer = zf.read(item.filename)
                if (item.filename[-8:] != 'meta.xml') and (item.filename[-11:] != 'content.xml') and (item.filename[-12:] != 'settings.xml'):
                    zp.writestr(item, buffer)
            except:
                print "Can't write"
                sys.exit(0)

        zf.close()
        zp.close()

    def _meta_adder(self):
        zf = ZipFile(self.newDocName, 'a')
        zf.write('meta.xml')
        zf.write('content.xml')
        zf.write('settings.xml')
        zf.close()

        #deleting container files
        os.remove('meta.xml')
        os.remove('content.xml')
        os.remove('settings.xml')

cleanopenoffi("test.odt","test2.odt")
