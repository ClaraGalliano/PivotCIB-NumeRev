# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:48:38 2019

@author: dreymond
"""

import nltk
import re
from gensim.utils import simple_preprocess

stopwords = nltk.corpus.stopwords.words('french')

def FiltreChamps(LstTHZ, LstChamps, SeuilScore):
    """Renvoi la liste de Thz extraitre de LstTHZ dont les champs biblio correspondent 
    à la LstChamps (contrainte d'intégrité mais quelle que soit la valeur)
    ET dont le score de IPCCat du résumé est supérieur à SeuilScore """
    LstTHZ2 = []
    for Thz in LstTHZ:
        Thz2 = dict()
        for cle in Thz.keys():
              if cle in LstChamps:
                if cle == 'CatIPC': 
                    if "1" in Thz[cle].keys(): # sélection classement le plus important
                        #hiérarchisation
                        
                        Thz2['IPC3'] = Thz[cle]["1"][0][0:4]
                        Thz2['IPC7'] = Thz[cle]["1"][0][0:7]
                        Thz2['IPC11'] = Thz[cle]["1"][0]
                        Thz2['score'] = Thz[cle]["1"][1]

                        pass
                else:
                    Thz2[cle] = Thz[cle]
        if 'score' not in Thz2.keys():
            Thz2["score"] = 0
        # and Thz2['discipline'] != '?':
        if int(Thz2["score"]) > SeuilScore:
                LstTHZ2.append(Thz2)
        else:
            pass
#    else:
#        evites += 1
    return LstTHZ2




def GetIPCDefinition(): #buggy
    """renvoi un dictionnaire dont les étiquettes sont les CIB et les valeurs
    leur description en Fr. On devrait pouvoir facilement paramétrer la langue puisque
    l'OEB fournit l'XMl pour toutes les versions (depuis 2016) en fr et en en
    https://www.wipo.int/ipc/itos4ipc/ITSupport_and_download_area/20190101/MasterFiles/
    
    """
    from lxml import etree
    with open('FR_ipc_definitions_20190101.xml', 'rb') as fic:
        data=fic.read()
    
    IPCtree = etree.fromstring(data)
    dicoDef = dict()
    
    
#    nsmap = {}
#    for ns in IPCtree.xpath('//namespace::*'):
#        if ns[0]: # Removes the None namespace, neither needed nor supported.
#            nsmap[ns[0]] = ns[1]
#        else:
#            nsmap['wipo'] = ns[1]
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
    return dicoDef 

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stopwords] for doc in texts]

def Phrase_En_Mots(sentences):
    Renvoi = []
    for sentence in sentences:
        Renvoi.append(simple_preprocess(str(sentence), deacc=True))
    return Renvoi


def strip_accents(text):

    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    import unicodedata
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def CheckList(dico, indesir):
    if isinstance(dico, dict):
        CleASupprimer = [k for k, v in dico.items() if any([v is i for i in indesir])]
        if len(CleASupprimer)>0:
            return False
        else:
            return dico
    elif isinstance(dico, list):
        tempoList =[]
        for dic in dico:
            tempo = CheckList(dic, indesir)
            if tempo:
                tempoList.append(tempo)
        Liste = tempoList
    return Liste

def InsereTermesDebut(Liste, ListeTerme):
    for mot in ListeTerme:
        Liste.insert(0, mot)
        Liste.insert(0, strip_accents(mot))
    return Liste

def Nettoie(ch, Stop):
    ch=ch.lower()
    ch = strip_accents(ch)
    if Stop:
        return " ".join([mot for mot in re.split('\W+', ch) if mot not in stopwords]).strip()
    else:

        return " ".join([mot for mot in re.split('\W+', ch)]).strip()