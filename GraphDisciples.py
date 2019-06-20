# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:07:18 2019

@author: dreymond
"""


import json
from Utils import GetIPCDefinition, strip_accents

with open('DonneeThzEtendues.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre', 'Domaine', 'Section', 'DiscipNorm']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()

RepertoireDestination ="./Visualisations/JSON/"
seuilScore = 1200

Titres = True #présence des titres dans les graphes (à n'utiliser qu'après avoir beaucoup seuillé ^_^)


FichierJsonHierarchie = "HierarchieDiscipline" #+ str(seuilScore)+Titres*'Titre'

LstThz2 = []
evites = 0 # compteur des entrées ignorée (consistance ou seuillage)



IPC7IPC3DiscipSectionDom = dict()

for thz in LstThz:
    if thz['Domaine'] in IPC7IPC3DiscipSectionDom.keys():
        if thz['Section'] in IPC7IPC3DiscipSectionDom[thz['Domaine']].keys():
            if thz['DiscipNorm'] in IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']].keys():
                if thz['discipline'] not in IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]:
                    IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']].append(thz['discipline'])
                else:
                    pass
                    
            else:
                IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=[thz['discipline']]
        else:
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']]= dict()
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=dict()
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=[thz['discipline']]
    else:
        IPC7IPC3DiscipSectionDom[thz['Domaine']]= dict()
        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']]= dict()
        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=[thz['discipline']]


#création des hierarchies au format sunburst et autres
HierarchieJsonFin = dict()
HierarchieJsonFin['name'] ="CNU"

HierarchieJsonFin ['children'] = []

HierarchieJsonFin ['value'] = len(IPC7IPC3DiscipSectionDom.keys())
for dom in IPC7IPC3DiscipSectionDom.keys():
    HierarchieJsonFinDom = dict()
    HierarchieJsonFinDom['name'] = dom
    HierarchieJsonFinDom['children'] = []
    HierarchieJsonFinDom['value'] = len(IPC7IPC3DiscipSectionDom[dom].keys())
    for section in IPC7IPC3DiscipSectionDom[dom].keys():
        tempoDict=dict()
        tempoDict['name'] = section
        tempoDict['children'] = []
        tempoDict['value'] = len(IPC7IPC3DiscipSectionDom[dom][section].keys())
        for discip in IPC7IPC3DiscipSectionDom[dom][section].keys():
            tempoDiscipDict=dict()
            tempoDiscipDict['name'] = discip
            tempoDiscipDict['children'] = [{'name' : dis, 'value':1 } for dis in IPC7IPC3DiscipSectionDom[dom][section][discip]]
            tempoDiscipDict['value'] = len(IPC7IPC3DiscipSectionDom[dom][section][discip])
                         
            tempoDict['children'].append(tempoDiscipDict)
        HierarchieJsonFinDom['children'].append(tempoDict)
        
    HierarchieJsonFin['children'].append(HierarchieJsonFinDom)
DumpHierarchie = json.dumps(HierarchieJsonFin, ensure_ascii=False, indent=1)


with open(RepertoireDestination+FichierJsonHierarchie +'.json', 'wb') as ficRes:
    ficRes.write(DumpHierarchie.encode('utf8'))    

print(" Fichier de Hierachie Discipline ", FichierJsonHierarchie +'.json correctement écrit' )   

 