#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self, xmlFile):
        # Load parser and driver
        theParser = make_parser()
        theHandler = myContentHandler()
        theParser.setContentHandler(theHandler)

        # Ready, set, go!
        theParser.parse(xmlFile)
        
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.title = ""
        self.link = ""

        print "Parse complete"

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
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

                respuesta = "HTTP/1.1 200 OK \r\n\r\n<html><body><a href='" + self.link + "'>" + self.title + "</a>\r\n"
                print(respuesta)

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Usage: python xml-parser-barrapunto.py <document>"
        print
        print " <document>: file name of the document to parse"
        sys.exit(1)

    # Ready, set, go!
    xmlFile = open(sys.argv[1],"r")
    theParser.parse(xmlFile)

    print "Parse complete"
