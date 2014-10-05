from tempfile import mkdtemp
from zipfile import ZipFile, is_zipfile
from shutil import rmtree, copyfileobj
from xml.dom.minidom import parse
import os

class extractopenoffi():

    def __init__(self):
        self.metaData = {"Date": {},
        "Links": [],
        "Mails": []}

    def _ms_do(self, archivo):
        self.archivo = archivo
        self.ruta = mkdtemp(prefix='gra')
        if self.__uncompress():
            self._ms_xml_parser()
            self._ms_extraxml_parser()
            return self.metaData
        else:
            return {'Error': 'El archivo no es valido'}

    def __uncompress(self):
        if not is_zipfile(self.archivo):
            return False
        buff = ZipFile(self.archivo, 'r')
        for i in buff.namelist():
            if i in ('meta.xml', 'content.xml', 'settings.xml'):
                filename = os.path.basename(i)
                source = buff.open(i)
                target = file(os.path.join(self.ruta, filename), 'wb')
                copyfileobj(source, target)
                source.close()
                target.close()
        return True

    def _ms_xml_parser(self):
        core = parse(os.path.join(self.ruta, 'meta.xml'))
        self.metaData["Date"]["Creation"] =\
        self.__getMetaData(core, "meta:creation-date")
        self.metaData["Date"]["Modification"] =\
        self.__getMetaData(core, "dc:date")
        self.metaData["Date"]["Modification Times"] =\
        self.__getMetaData(core, "meta:editing-cycles")
        #self.metaData["Aplication"] =\
        #self.__version(self.__getMetaData(core, "meta:generator"))
        self.metaData["Title"] = self.__getMetaData(core, "dc:title")
        self.metaData["Description"] =\
        self.__getMetaData(core, "dc:description")
        self.metaData["Keywords"] = self.__getMetaData(core, "meta:keyword")
        self.metaData["Languaje"] = self.__getMetaData(core, "dc:language")
        self.metaData["User"] =\
        self.__getMetaData(core, "meta:initial-creator")

    def _ms_extraxml_parser(self):
        content = parse(os.path.join(self.ruta, 'content.xml'))
        settings = parse(os.path.join(self.ruta, 'settings.xml'))
        buff = content.getElementsByTagName('text:a')
        if len(buff):
            for i in buff:
                if i.getAttribute('xlink:href'):
                    link = i.getAttribute('xlink:href')
                    if link[0:7] == 'mailto:':
                        if not link in self.metaData["Mails"]:
                            self.metaData["Mails"].append(link[7:])
                    else:
                        if not link in self.metaData["Links"]:
                            self.metaData["Links"].append(link)

            buff = settings.getElementsByTagName('config:config-item')
            if len(buff):
                for i in buff:
                    if i.getAttribute('config:name') == 'PrinterName':
                        if not i.firstChild is None:
                            self.metaData["Printer"] = i.firstChild.toxml()

    def __getMetaData(self, xml, tag):
        buff = xml.getElementsByTagName(tag)
        if len(buff):
            if not buff[0].firstChild is None:
                return buff[0].firstChild.toxml()
            else:
                return None

    """def __version(self, data):
        data = re.findall('(.*)\.org/(.*)\$(.*) (.*)/(.*).*', data)
        self.metaData["SO"] = data[0][2]
        return data[0][0] + " " + data[0][1]"""
#extractopenoffi()._ms_do("test.odt")
