# -*- coding: utf-8 -*-

"""
Created on Tue Feb 02 13:36:47 2016

@author: dreymond
"""
import requests
import time
import json

import xmltodict
from IPCCat_lib import IPCCategorizer, IPCExtractPredictions
import codecs
#from io import StringIO
#io = StringIO()
with open('ScrapThese.json', 'r') as ficSrc:
    donnees = json.load(ficSrc)
  
FicRes = 'DonneesThese.json'
urlBase = 'http://www.theses.fr/'

cpt = 0 # nb de données de thz
cpt2 = 0 # thz traitées
inconsist = 0 #inconsistance des donnees bibli
Seuil = 0
LstTZ = []

with codecs.open(FicRes, "a", "utf8") as SavFic:
    SavFic.write('[\n')
    for thz in donnees:
        cpt +=1
        time.sleep(3) # l'ABES est strict : délai minimal à respecter
        urlThz = urlBase + thz['num']+ '.xml'
        page = requests.get(urlThz)                
        THZ = dict()
        if page.ok:
            data = xmltodict.parse(page.text)
            if  'rdf:RDF' in data.keys():
                if 'bibo:Thesis' in data['rdf:RDF'].keys():
                    if 'dcterms:abstract' in data['rdf:RDF']['bibo:Thesis'].keys():
                        cpt2 +=1
                        if isinstance(data['rdf:RDF']['bibo:Thesis']['dcterms:abstract'], dict):
                            resume = data['rdf:RDF']['bibo:Thesis']['dcterms:abstract']['#text']
                            if isinstance(resume, list):
                                resume=" ".join(resume)
                            resume=resume.replace(';', '!!!')
                            langue = data['rdf:RDF']['bibo:Thesis']['dcterms:abstract']['@xml:lang']
                        else:
                            for donnee in data['rdf:RDF']['bibo:Thesis']['dcterms:abstract']:
                                if donnee['@xml:lang'] =='fr': #priorité FR
                                    resume = donnee['#text']
                                                
                                    if isinstance(resume, list):
                                        resume=" ".join(resume)
                                    resume= resume.replace(';', '!!!')
                                    langue =  donnee['@xml:lang']          
                                elif donnee['@xml:lang'] =='en':
                                    resume = donnee['#text']
                                    if isinstance(resume, list):
                                        resume=" ".join(resume)
                                    resume=resume.replace(';', '!!!')
                                    langue =  donnee['@xml:lang'] 
                                else:
                                    resume = ""
                                    langue = "fr"
                                    pass
                        Categorie = IPCCategorizer(resume, langue)
                        if Categorie is not None:
                            Predict = IPCExtractPredictions(Categorie, Seuil)
                        else:
                            Predict= ""
                        Titre = data['rdf:RDF']['bibo:Thesis']['dc:title']
                        #Titre = Titre.replace(';', '!!!')
                        Date = data['rdf:RDF']['bibo:Thesis']['dc:date']
                        if Date is None:
                            Date =""
                        if resume is None:
                            resume = ""
                        if Titre is None:
                            Titre=""
                        if  thz['discipline'] is None:
                             thz['discipline'] =""
                        if langue is None:
                            langue =""
                        thz['abstract'] = resume
                        thz['Date'] = Date
                        thz['langue'] = langue
                        thz['CatIPC']= dict()
                        if Predict is not None:
                            for predict in Predict:
                                thz['CatIPC'] [predict['rank']] = [predict['category'], predict['score']]
                        else:
                            for idx in range(5):
                                thz['CatIPC'] [idx] = ['', 0]
        
                     else:
                        inconsist +=1
                else:
                        inconsist +=1
            else:
                        inconsist +=1
        else:
                        inconsist +=1
        Data = json.dumps( thz, ensure_ascii=False)
        if cpt == len(donnees):
             SavFic.write( Data + '\n] \n') #dernière entrée
        else:
            SavFic.write( Data + ',\n')
        
#with open("DonneesThese.json", "w") as SavJson:                        
#    SavJson.write(json.dumps(LstTZ))
    
print ("nombre d'enregistrement de thèses traitées ", cpt)                 
print ("nombre de thèses traitées ", cpt2)                 
print ("nombre de thèses inconsistantes ", inconsist)        

#    for IdThese in these.keys():
#        if these [IdThese]['LangueThese']=='fr' and IdThese not in DejaVu:
#            cpt+=1
#            print (cpt), " sur ", str(maxi)
#            
#            urlThz = urlBase + IdThese
#            page = requests.get(urlThz)
#            try:
#                indice = page.text.index('<span property="dc:description" xml:lang="fr">')
#                indice2 = page.text[indice:].index('</span') + indice 
#                resume = page.text[indice:indice2]
#                these [IdThese]['resume'] = resume
#                time.sleep(1)
#                pickle.dump([IdThese, these[IdThese]], SavFic)
#                DejaVu .append(IdThese)
#            except:
#                pass
#    
#
#   
#
#with open("TheseIramuteq.txt", "w") as ficRes:
#    for IdThese in these.keys():
#        Entete = '**** *Auteur_'+ these[IdThese]['Auteur']
#        try:
#            Entete += ' *Date_'+these[IdThese]['DateS'][6:]
#        except:
#            Entete += ' *Date_EnCours'
#        Entete += ' *Dir_'+these [IdThese]['DirecteurThese']
#        Entete += ' \n'
#        ficRes.write(Entete)
#        ficRes.write(these [IdThese]['resume'])
#        ficRes.write(' \n')
#


