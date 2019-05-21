# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:07:18 2019

@author: dreymond
"""


import json

with open('DonneesTheseEtendues.json', 'r') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre', 'Domaine', 'SousDomaine']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
evites = 0
for Thz in LstThz:
    Thz2 = dict()
#    if Thz["discipline"] in SousDiscipline.keys() or Thz["discipline"].lower() in SousDiscipline.keys() or Thz["discipline"].strip().lower()  in SousDiscipline.keys():
#        try:
#            Thz["discipline"]= SousDiscipline[Thz["discipline"].lower() ]
#        except:
#            try:
#                Thz["discipline"]= SousDiscipline[Thz["discipline"].strip().lower() ]
#            except:
#                
#                Thz["discipline"]= SousDiscipline[Thz["discipline"]]
#    else:
#        print ('bug -->', Thz["discipline"].lower() )
    for cle in Thz.keys():
        if cle in ChampsEpures:
            if cle == 'CatIPC': 
                if "1" in Thz[cle].keys(): # sélection classement le plus important
                    #hiérarchisation
                    
                    Thz2['IPC3'] = Thz[cle]["1"][0][0:4]
                    Thz2['IPC7'] = Thz[cle]["1"][0][0:7]
                    Thz2['IPC11'] = Thz[cle]["1"][0]
                    Thz2['score'] = Thz[cle]["1"][1]
                else:
                    pass
            else:
                Thz2[cle] = Thz[cle]
    if 'IPC3' in Thz2.keys() and len(Thz2['IPC3']) >0:# and Thz2['discipline'] != '?':
        LstThz2.append(Thz2)
    else:
        evites += 1
HierarchieJsonFin = dict()
HierarchieJsonFin['name'] ="Eau"


HierarchieJsonFin ['children'] = []
Domaines= list(set([thz['Domaine'] for thz in LstThz2]))
SousDomaines = dict()
for dom in Domaines:
    SousDomaines[dom] = list(set([thz['SousDomaine'] for thz in LstThz2 if thz['Domaine']==dom]))

IPC7IPC3SousDomDom = dict()
for thz in LstThz2:
    if thz['Domaine'] in IPC7IPC3SousDomDom.keys():
        if thz['SousDomaine'] in IPC7IPC3SousDomDom[thz['Domaine']].keys():
            if thz['IPC3'] in IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']].keys():
                if thz['IPC7'] in IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']].keys():
                    IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']].append(thz['titre'])
                else:
                    IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=[thz['titre']]
            else:
                 IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=dict()
                 IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=[thz['titre']]
        else:
            IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']]= dict()
            IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=dict()
            IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=[thz['titre']]
    else:
        IPC7IPC3SousDomDom[thz['Domaine']]= dict()
        IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']]= dict()
        IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=dict()
        IPC7IPC3SousDomDom[thz['Domaine']][thz['SousDomaine']][thz['IPC3']]=[thz['titre']]

Nodes = dict()
Links = dict()
compteNoeud = 0
for dom in IPC7IPC3SousDomDom.keys():
    HierarchieJsonFin['name'] = dom
    Nodes [dom] = compteNoeud
    compteNoeud +=1 
    for sousDom in IPC7IPC3SousDomDom[dom].keys():
        tempoDict=dict()
        tempoDict['name'] = sousDom
        Nodes [sousDom] = compteNoeud
        compteNoeud +=1
        tempoDict['children'] = []
        for IPC7 in IPC7IPC3SousDomDom[dom][sousDom].keys():
            tempotempoDict=dict()
            tempotempoDict['name'] = IPC7
            
            Nodes [IPC7] = compteNoeud
            compteNoeud +=1
            tempotempoDict['children'] = []
            for IPC3 in IPC7IPC3SousDomDom[dom][sousDom][IPC7].keys():
                tempotempotempoDict=dict()
                tempotempotempoDict['name'] = IPC3
                Nodes [IPC3] = compteNoeud
                compteNoeud +=1
                tempotempotempoDict['children'] = [titre for titre in IPC7IPC3SousDomDom[dom][sousDom][IPC7]['IPC3']]
                for titre in IPC7IPC3SousDomDom[dom][sousDom][IPC7]['IPC3']:
                     Nodes [titre] = compteNoeud
                     compteNoeud +=1
            tempotempoDict['children'].append(tempotempotempoDict)
        tempoDict['children'].append(tempotempoDict)
    HierarchieJsonFin['children'].append(tempoDict)

for thz in LstThz:
    cle = (Nodes[thz['Domaine']],Nodes[thz['SousDomaine']])
    if cle in Links.keys():
         Links [cle] +=1
    else:
        Links [cle] =1
    cle = (Nodes[thz['SousDomaine']],Nodes[thz['IPC7']])
    if cle in Links.keys():
         Links [cle] +=1
    else:
        Links [cle] =1
    cle = (Nodes[thz['IPC7']],Nodes[thz['IPC3']])
    if cle in Links.keys():
         Links [cle] +=1
    else:
        Links [cle] =1
    cle = (Nodes[thz['IPC3']],Nodes[thz['titre']])
    if cle in Links.keys():
         Links [cle] +=1
    else:
        Links [cle] =1
IdxNoeuds = dict()
for noeud in Nodes.keys():
    IdxNoeuds[Nodes[noeud]] = noeud 
Graphdico = dict()

Graphdico ['nodes'] = []
for ind in range(max(IdxNoeuds.keys())):
    dicoTemp =dict()
    dicoTemp ['name'] = IdxNoeuds[ind]
    Graphdico ['nodes'].append( dicoTemp)
Graphdico ['links'] = []
for link in Links.keys():
    dicoTemp =dict()
    dicoTemp ['source'] = link [0]
    dicoTemp ['target'] = link [1]
    dicoTemp ['value'] = Links ['link']

toto = json.dumps(Graphdico, ensure_ascii=False, indent=1)
with open('GraphDisciplineCIB.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8')) 

toto = json.dumps(HierarchieJsonFin, ensure_ascii=False, indent=1)
with open('HierarchieDisciplineCIB.js', 'wb') as ficRes:
    ficRes.write(b"function getData() {    return "
                 + toto.encode('utf8')+b" };")  
with open('HierarchieDisciplineCIB.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))      
