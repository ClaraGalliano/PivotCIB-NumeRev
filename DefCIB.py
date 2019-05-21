# -*- coding: utf-8 -*-
"""
Created on Sun May 19 18:05:37 2019

@author: dreymond
"""
from Utils import Nettoie
from lxml import etree
CIB = dict()
with open('FR_ipc_definitions_20190101.xml', 'rb') as fic:
    data=fic.read()


parser = etree.XMLParser()
IPCtree = etree.fromstring(data)
dicoDef = dict()


nsmap = {}
for ns in IPCtree.xpath('//namespace::*'):
    if ns[0]: # Removes the None namespace, neither needed nor supported.
        nsmap[ns[0]] = ns[1]
    else:
        nsmap['wipo'] = ns[1]

#finalement çà marche pas en utilisant les espaces de nom :-(
# méthode plus bricolage
# on recherche les entrées des sections        
Definitions= IPCtree.findall('{http://www.wipo.int/classifications/ipc/masterfiles}IPCDefinitionsSection')

for section in Definitions: #
    #on récupère les définitions des éléements '{http://www.wipo.int/classifications/ipc/masterfiles}DEFINITION-STATEMENT',
#    # en excluant les autres éléments (je c'est c'est pas beau: 
#    [
#    '{http://www.wipo.int/classifications/ipc/masterfiles}LARGESUBJECTS', 
#    '{http://www.wipo.int/classifications/ipc/masterfiles}REFERENCES', 
#    '{http://www.wipo.int/classifications/ipc/masterfiles}GLOSSARYOFTERMS']
    Def = [truc for truc in section.iterdescendants(tag='{http://www.wipo.int/classifications/ipc/masterfiles}IPC-DEFINITION')]
    #ét on récupère le xhtml (en destructurant les paragraphes et les énumérations)
    for el in Def:
        defi = [truc.text for truc in el.iterdescendants('{http://www.w3.org/1999/xhtml}p')]
        if len(defi)>0:
            tempoch=""
            for ch in defi:
                if ch:
                    temp = Nettoie(ch.strip(), False)
                    if len(temp)>0:
                        tempoch += ch +" \n "
            dicoDef[el.attrib['IPC']] =tempoch

