from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Page
import urllib.parse
import urllib.request

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

titulares = ""

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.title = ""
        self.link = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        global titulares

        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + "."
                self.title = self.theContent
                # To avoid Unicode trouble
                #print line.encode('utf-8')
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = self.theContent
                #print " Link: " + self.theContent + "."
                self.inContent = False
                self.theContent = ""

                titulares = titulares + "<a href='" + self.link + "'>" + self.title + "</a><br>"

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def mostrar(request):
    global titulares

    #Pido el XML de Barrapunto
    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')

    #Inicializo el parse de barrapunt
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    theParser.parse(xmlFile)

    salida = "<ul>"
    for listado in Page.objects.all():
        salida += "<li>" + str(listado.nombre)
    salida += "</ul>"

    return HttpResponse("<h1>Contenido de la base de datos:</h1>" + salida + "<br><h2>Titulares de Barrapunto</h2>" + titulares)

@csrf_exempt
def insertar(request, texto):
    if request.method == "GET":
        try:
            p = Page.objects.get(nombre = texto)
            return HttpResponse(p.contenido)
        except Page.DoesNotExist:
            return HttpResponse("No existe una página para ese recurso.")

    else:
        p = Page(nombre = texto, pagina = request.body.decode('utf-8'))
        p.save()
        return HttpResponse("Página con el nombre: '" + str(p.nombre) + "' y el contenido: " + str(p.contenido) + " ha sido creada.")
