# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
with open('DonneesTheseTest.csv', 'r') as ficSrc:
    donnees = ficSrc.readlines()

LstThz = []
LstThz2 = []
ChampsInitiaux = ['Id','Discipline','Date','Langue','Titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['Discipline','Date','Langue','IPC1', 'ScoreIPC1']
for lig in donnees[1:]:
    lig= lig.split(';')
    IndChamp = 0
    Thz = dict()
    for Champ in ChampsInitiaux:
        Thz[Champ] = lig[IndChamp]
        IndChamp +=1 
    LstThz.append(Thz)

for Thz in LstThz:
    Thz2 = dict()
    
    for cle in Thz.keys():
        if cle in ChampsEpures:
            if cle == 'IPC1':
                Thz2[cle] = Thz[cle][0:4]
            else:
                Thz2[cle] = Thz[cle]
    LstThz2.append(Thz2)
with open('PivotThese.json', 'w') as ficRes:
    ficRes.write(json.dumps(LstThz2))
