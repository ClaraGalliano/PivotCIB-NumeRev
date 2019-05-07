# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
with open('DonneesThese2.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre']
cpt=0
cptFini=0

print (cpt)
print (cptFini)
with codecs.open('DataThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz))
evites = 0
for Thz in LstThz:
    Thz2 = dict()
    
    for cle in Thz.keys():
        if cle in ChampsEpures:
            if cle == 'CatIPC': 
                if "1" in Thz[cle].keys(): # sélection classement le plus important
                    #hiérarchisation
                    Thz2['IPC3'] = Thz[cle]["1"][0:4]
                    Thz2['IPC7'] = Thz[cle]["1"][0:7]
                    Thz2['IPC11'] = Thz[cle]["1"]
                else:
                    pass
            else:
                Thz2[cle] = Thz[cle]
    if 'IPC3' in Thz2.keys():
        LstThz2.append(Thz2)
    else:
        evites += 1
print ('Theses ignorées', evites)
with codecs.open('PivotThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz2))

LstIpc3 = [thz['IPC3'][0] for thz in LstThz2]
LstIpc7 = [thz['IPC7'][0] for thz in LstThz2]
LstIpc11 = [thz['IPC11'][0] for thz in LstThz2]

LstIpc3 = list(set(LstIpc3))
LstIpc7 = list(set(LstIpc7))
LstIpc11 = list(set(LstIpc11))

Discipline = dict()
NiveauIPC11 = dict()
NiveauIPC7 = dict()
NiveauIPC3 = dict()
Hierarchie = dict()
Hierarchie["name"] = "Eau"
Hierarchie["children"] = []
feuilles = dict()
for thz in LstThz2:
    #le bout des feuilles
    feuilles['name'] = thz['titre'].title().replace(' ', '')
    feuilles['value'] = int(thz['IPC11'][1])
    if thz['IPC11'][0] in NiveauIPC11.keys():
        NiveauIPC11[thz['IPC11'][0]].append(feuilles)
    else:
        NiveauIPC11[thz['IPC11'][0]] =  []
        NiveauIPC11[thz['IPC11'][0]].append(feuilles)
    if thz['IPC7'][0] in NiveauIPC7.keys():
        NiveauIPC7[thz['IPC7'][0]].append(thz['IPC7'][0])
    else:
        NiveauIPC7[thz['IPC7'][0]] =  []
        NiveauIPC7[thz['IPC7'][0]].append(thz['IPC7'][0])
    if thz['IPC3'][0] in NiveauIPC3.keys():
        NiveauIPC3[thz['IPC3'][0]].append(thz['IPC3'][0])
    else:
        NiveauIPC3[thz['IPC3'][0]] =  []
        NiveauIPC3[thz['IPC3'][0]].append(thz['IPC3'][0])      
    if thz['discipline'] in Discipline.keys():
        Discipline [thz['discipline']].append(thz['IPC3'][0])
    else:
        Discipline [thz['discipline']] =  []
        Discipline [thz['discipline']].append(thz['IPC3'][0])
Niveau1 = dict()
Hierarchie = dict()
Hierarchie ['name'] = "Eau"
Hierarchie ['children'] = []
for dis in Discipline.keys():
    Niveau1 = dict()
    Niveau1['name']= dis
    for ipc3 in NiveauIPC3.keys():
        if ipc3 in Discipline[dis]:
            if 'children' in Niveau1.keys():
                Niveau1["children"].append(ipc3) 
            else:
                Niveau1["children"] = []
                Niveau1["children"].append(ipc3) 
    if 'children' in Hierarchie.keys():
        Hierarchie['children'].append(Niveau1) 
    else:
        Hierarchie['children'] = []
        Hierarchie['children'].append(Niveau1) 
toto = json.dumps(Hierarchie, ensure_ascii=False)