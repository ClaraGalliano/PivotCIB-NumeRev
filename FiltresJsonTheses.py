# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
with codecs.open('DonneesTheseTemp.csv', 'r', 'utf8') as ficSrc:
    donnees = ficSrc.readlines()

LstThz = []
LstThz2 = []
ChampsInitiaux = ['Id','Discipline','Date','Langue','Titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['Discipline','Date','Langue','IPC1', 'ScoreIPC1', 'Titre']
cpt=0
cptFini=0
for lig in donnees[1:]:
    cpt+=1
    lig= lig.split(';')
    IndChamp = 0
    Thz = dict()
    for Champ in ChampsInitiaux:
        if len(lig) > len(ChampsInitiaux):
            Thz[Champ] = lig[IndChamp]
            IndChamp +=1 
    if len(lig) > len(ChampsInitiaux):
        LstThz.append(Thz)
        cptFini +=1
    else:
        print(lig)
print (cpt)
print (cptFini)
with codecs.open('DataThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz))
for Thz in LstThz:
    Thz2 = dict()
    
    for cle in Thz.keys():
        if cle in ChampsEpures:
            if cle == 'IPC1':
                Thz2['IPC3'] = Thz[cle][0:4]
                Thz2['IPC7'] = Thz[cle][0:7]
                Thz2['IPC11'] = Thz[cle]
            else:
                Thz2[cle] = Thz[cle]
    LstThz2.append(Thz2)
with codecs.open('PivotThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz2))

LstIpc3 = [thz['IPC3'] for thz in LstThz2]
LstIpc7 = [thz['IPC7'] for thz in LstThz2]
LstIpc11 = [thz['IPC11'] for thz in LstThz2]

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
    feuilles['name'] = thz['Titre'].title().replace(' ', '')
    feuilles['value'] = int(thz['ScoreIPC1'])
    if thz['IPC11'] in NiveauIPC11.keys():
        NiveauIPC11[thz['IPC11']].append(feuilles)
    else:
        NiveauIPC11[thz['IPC11']] =  []
        NiveauIPC11[thz['IPC11']].append(feuilles)
    if thz['IPC7'] in NiveauIPC7.keys():
        NiveauIPC7[thz['IPC7']].append(thz['IPC7'])
    else:
        NiveauIPC7[thz['IPC7']] =  []
        NiveauIPC7[thz['IPC7']].append(thz['IPC7'])
    if thz['IPC3'] in NiveauIPC3.keys():
        NiveauIPC3[thz['IPC3']].append(thz['IPC3'])
    else:
        NiveauIPC3[thz['IPC3']] =  []
        NiveauIPC3[thz['IPC3']].append(thz['IPC3'])      
    if thz['Discipline'] in Discipline.keys():
        Discipline [thz['Discipline']].append(thz['IPC3'])
    else:
        Discipline [thz['Discipline']] =  []
        Discipline [thz['Discipline']].append(thz['IPC3'])
Niveau1 = dict()
for ipc3 in NiveauIPC3.keys():
    Niveau1['name'] = ipc3
    
    Hierarchie["children"].append(ipc3)   