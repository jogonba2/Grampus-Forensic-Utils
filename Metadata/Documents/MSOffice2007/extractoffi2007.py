from tempfile import mkdtemp
from zipfile import ZipFile, is_zipfile
from shutil import rmtree, copyfileobj
from xml.dom.minidom import parse
import os

class extractoffi2007():
    def __init__(self):
        self.fecha = {"01": "Enero",
        "02": "Febrero",
        "03": "Marzo",
        "04": "Abril",
        "05": "Mayo",
        "06": "Junio",
        "07": "Julio",
        "08": "Agosto",
        "09": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre"}

        self.metaDatos = {"Titulo": "",
        "Usuarios": [],
        "Fecha": {"Creado": "", "Modificado": "", "Impreso": ""},
        "Aplicacion": "",
        "Empresa": "",
        "Editado": ""}

    def extract(self, archivo):
        self.archivo = archivo
        self.ruta = mkdtemp(prefix='gra')
        if self.__descomprimir():
            self.__docProps()
            self.__extraData()
        else:
            return {"Error": "No es un archivo valido"}
        rmtree(self.ruta)

        return self.metaDatos

    def __descomprimir(self):
        if not is_zipfile(self.archivo):
            return False
        buff = ZipFile(self.archivo, 'r')
        for i in buff.namelist():
            if i in ('docProps/core.xml', 'docProps/app.xml',
                'word/document.xml', 'word/_rels/document.xml.rels'):
                filename = os.path.basename(i)
                source = buff.open(i)
                target = file(os.path.join(self.ruta, filename), 'wb')
                copyfileobj(source, target)
                source.close()
                target.close()
        return True

    def __docProps(self):
        core = parse(os.path.join(self.ruta, 'core.xml'))
        app = parse(os.path.join(self.ruta, 'app.xml'))

        self.metaDatos["Usuarios"].append(
        self.__getMetaData(core, "dc:creator"))
        self.metaDatos["Titulo"] = \
        self.__getMetaData(core, "dc:title")
        self.metaDatos["Usuarios"].append(
        self.__getMetaData(core, "cp:lastModifiedBy"))

        self.metaDatos["Aplicacion"] = self.__getMetaData(app, "Application")
        self.metaDatos["Empresa"] = self.__getMetaData(app, "Company")
        self.metaDatos["Editado"] = \
        self.__getMetaData(core, "cp:revision") + " veces"

        self.metaDatos["Fecha"]["Creado"] = \
        self.__W3CDTF(self.__getMetaData(core, "dcterms:created"))
        self.metaDatos["Fecha"]["Modificado"] = \
        self.__W3CDTF(self.__getMetaData(core, "dcterms:modified"))
        self.metaDatos["Fecha"]["Impreso"] = \
        self.__W3CDTF(self.__getMetaData(core, "cp:lastPrinted"))

    def __W3CDTF(self, fecha):
        if fecha is None:
            return "Nunca"
        return str(fecha[5:7] + " de " + self.fecha[fecha[5:7]] + " del " +
        fecha[0:4] + " a las: " + fecha[14:19])

    def __getMetaData(self, xml, tag):
        buff = xml.getElementsByTagName(tag)
        if len(buff):
            if not buff[0].firstChild is None:
                return buff[0].firstChild.toxml()
            else:
                return None

    def __extraData(self):
        self.metaDatos["Links"] = []
        doc = os.path.join(self.ruta, 'document.xml')
        rel = os.path.join(self.ruta, 'document.xml.rels')
        if os.path.isfile(doc) and os.path.isfile(rel):
            document = parse(doc)
            links = parse(rel)

            buff = document.getElementsByTagName('w:ins')
            if len(buff):
                for i in buff:
                    usuario = i.getAttribute('w:author')
                    if not usuario in self.metaDatos["Usuarios"]:
                        self.metaDatos["Usuarios"].append(usuario)

            buff = links.getElementsByTagName('Relationship')
            if len(buff):
                for i in buff:
                    if i.getAttribute('TargetMode'):
                        link = i.getAttribute('Target')
                        if not link in self.metaDatos["Links"]:
                            self.metaDatos["Links"].append(link)
