# -*- coding: utf-8 -*-

"""
Created on Tue Feb 02 13:36:47 2016

@author: dreymond
"""
import requests
import time
with open ('ScrapThese4.csv', 'r') as fichier:
    donnees = fichier.readlines()
  
these = dict()
import cPickle as pickle

for thz in donnees[1:]:
    try:    
        decoupThz = thz.replace('"', '').split(";")
        
        IdThese = decoupThz[13]
        these [IdThese] = dict()
        these [IdThese]['Auteur'] = decoupThz[0]
        these [IdThese]['IdAuteur'] = decoupThz[1]
        these [IdThese]['Titre'] = decoupThz[2]
        these [IdThese]['DirecteurThese'] = decoupThz[4].split(',')
        these [IdThese]['Identifiant directeur'] = decoupThz[5].split(',')
        these [IdThese]['Etablissement'] = decoupThz[6]
        these [IdThese]['IdEtablissement'] = decoupThz[7]
        these [IdThese]['Discipline'] = decoupThz[8]
        these [IdThese]['Soutenue'] = decoupThz[9]
        
        these [IdThese]['DateS'] = decoupThz[11] 
        these [IdThese]['LangueThese'] = decoupThz[12]
    except:
        pass
        print ("Ignored :"), thz
urlBase = 'http://www.theses.fr/'
cpt = 0
maxi = len(these.keys())
DejaVu = []
try:
    with open("DonneesThez4.pkl", "r") as DoneFic:
        while 1:
            try:
                temp = pickle.load(DoneFic)
                DejaVu .append(temp[0])
                
            except EOFError:
                break
except:
    pass
with open("DonneesThez4.pkl", "a") as SavFic:
 
    for IdThese in these.keys():
        if these [IdThese]['LangueThese']=='fr' and IdThese not in DejaVu:
            cpt+=1
            print (cpt), " sur ", str(maxi)
            
            urlThz = urlBase + IdThese
            page = requests.get(urlThz)
            try:
                indice = page.text.index('<span property="dc:description" xml:lang="fr">')
                indice2 = page.text[indice:].index('</span') + indice 
                resume = page.text[indice:indice2]
                these [IdThese]['resume'] = resume
                time.sleep(1)
                pickle.dump([IdThese, these[IdThese]], SavFic)
                DejaVu .append(IdThese)
            except:
                pass
    

   
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


