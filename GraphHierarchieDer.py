# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:07:18 2019

@author: dreymond
"""


import json
from Utils import GetIPCDefinition
with open('DonneeThzEtendues.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre', 'Domaine', 'Section', 'DiscipNorm']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
evites = 0
seuilScore = 0
SeuilNoeud = 0
IPCDef = GetIPCDefinition()

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
        Ok=False
        if cle in ChampsEpures:
            if cle == 'CatIPC': 
                if "1" in Thz[cle].keys(): # sélection classement le plus important
                    #hiérarchisation
                    
                    Thz2['IPC3'] = Thz[cle]["1"][0][0:4]
                    Thz2['IPC7'] = Thz[cle]["1"][0][0:7]
                    Thz2['IPC11'] = Thz[cle]["1"][0]
                    Thz2['score'] = Thz[cle]["1"][1]
#                    if Thz2['IPC7'] in IPCDef.keys():
#                        defi = IPCDef[Thz2['IPC7']]
#                    elif Thz2['IPC3'] in IPCDef.keys():
#                        defi = IPCDef[Thz2['IPC3']]
#                    else:
#                        defi ='Pas trouvé'
#                    Thz2['DefIPC'] = defi
#                    Ok=True
#                else:
                    pass
            else:
                Thz2[cle] = Thz[cle]
    if 'score' not in Thz2.keys():
        Thz2["score"] = 0
    # and Thz2['discipline'] != '?':
    if int(Thz2["score"]) > seuilScore and Thz2['Domaine'] != 'Autres':
            LstThz2.append(Thz2)
    else:
            evites += 1
#    else:
#        evites += 1
print ("Nombre d'entrées évitéées: ", seuilScore)
HierarchieJsonFin = dict()
HierarchieJsonFin['name'] ="Eau"

# 


HierarchieJsonFin ['children'] = []
Domaines= list(set([thz['Domaine'] for thz in LstThz2]))
Section = dict()
DiscipNorm = dict()
for dom in Domaines:
    Section[dom] = list(set([thz['Section'] for thz in LstThz2 if thz['Domaine']==dom]))

IPC7IPC3DiscipSectionDom = dict()

for thz in LstThz2:
    if thz['Domaine'] in IPC7IPC3DiscipSectionDom.keys():
        if thz['Section'] in IPC7IPC3DiscipSectionDom[thz['Domaine']].keys():
            if thz['DiscipNorm'] in IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']].keys():
                
                if thz['IPC3'] in IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']].keys():
                    if thz['IPC7'] in IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']].keys():
                        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']][thz['IPC7']].append(thz['titre'])
                    else:
                        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']][thz['IPC7']]=[thz['titre']]
                else:
                     IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']]=dict()
                     IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']][thz['IPC7']]=[thz['titre']]
            else:
                IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=dict()
                IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']]=dict()
                IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']][thz['IPC7']]=[thz['titre']]
        else:
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']]= dict()
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=dict()
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']]=dict()
            IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']][thz['IPC7']]=[thz['titre']]
    else:
        IPC7IPC3DiscipSectionDom[thz['Domaine']]= dict()
        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']]= dict()
        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']]=dict()
        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']]=dict()
        IPC7IPC3DiscipSectionDom[thz['Domaine']][thz['Section']][thz['DiscipNorm']][thz['IPC3']][thz['IPC7']]=[thz['titre']]

Nodes = dict()
Links = dict()
DejaVu = []
compteNoeud = 0
for dom in IPC7IPC3DiscipSectionDom.keys():
    HierarchieJsonFin['name'] = dom
    if dom not in DejaVu:
        Nodes [dom] = compteNoeud
        compteNoeud +=1 
        DejaVu.append(dom)
    for section in IPC7IPC3DiscipSectionDom[dom].keys():
        tempoDict=dict()
        tempoDict['name'] = section
        if section not in DejaVu:
            Nodes [section] = compteNoeud
            compteNoeud +=1
            DejaVu.append(section)
        tempoDict['children'] = []
        for discip in IPC7IPC3DiscipSectionDom[dom][section].keys():
            tempoDiscipDict=dict()
            tempoDiscipDict['name'] = discip
            if discip not in DejaVu:
                Nodes [discip] = compteNoeud
                compteNoeud +=1
                DejaVu.append(discip)
            tempoDiscipDict['children'] = []
            
            for IPC3 in IPC7IPC3DiscipSectionDom[dom][section][discip].keys():
                tempotempoDict=dict()
                tempotempoDict['name'] = IPC3
                if IPC3 not in DejaVu:
                    Nodes [IPC3] = compteNoeud
                    compteNoeud +=1
                    DejaVu.append(IPC3)
                tempotempoDict['children'] = []
                for IPC7 in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3].keys():
                    tempotempotempoDict=dict()
                    tempotempotempoDict['name'] = IPC7
                    if IPC7 not in DejaVu:
                        Nodes [IPC7] = compteNoeud
                        DejaVu.append(IPC7)
                        compteNoeud +=1

#                    tempotempotempoDict['children'] = Thz2['DefIPC']
#                    Nodes [Thz2['DefIPC']]= compteNoeud
#                    DejaVu.append(Thz2['DefIPC'])
#                    tempotempoDict['children'].append(tempotempotempoDict)
# Les titres sont longs le diagrame est illisible                    
                    tempotempotempoDict['children'] = [titre for titre in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7]]
                    if isinstance(IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7], list) and len(IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7])>0:
                        for titre in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7]:
                            if titre not in DejaVu:
                                Nodes [titre] = compteNoeud
                                compteNoeud +=1
                                DejaVu.append(titre)
                    else:
                        titre = IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7][0]
                        if titre not in DejaVu:
                                Nodes [titre] = compteNoeud
                                compteNoeud +=1
                                DejaVu.append(titre)
                tempotempoDict['children'].append(tempotempotempoDict)
            tempoDiscipDict['children'].append(tempotempoDict)
        tempoDict['children'].append(tempotempoDict)
    HierarchieJsonFin['children'].append(tempoDict)

for thz in LstThz2:

            cle = (Nodes[thz['Domaine']], Nodes[thz['Section']])
            if cle in Links.keys():
                 Links [cle] +=1
            else:
                Links [cle] =SeuilNoeud
            cle = (Nodes[thz['Section']], Nodes[thz['DiscipNorm']])
            if cle in Links.keys():
                 Links [cle] +=1
            else:
                Links [cle] =SeuilNoeud
            cle = (Nodes[thz['DiscipNorm']], Nodes[thz['IPC3']])
            if cle in Links.keys():
                 Links [cle] +=1
            else:
                Links [cle] =SeuilNoeud
            cle = (Nodes[thz['IPC3']], Nodes[thz['IPC7']])
            
            if thz['IPC7'] != thz['IPC3']:
                if cle in Links.keys():
                     Links [cle] +=1
                else:
                    Links [cle] = 1
                cle = (Nodes[thz['IPC7']], Nodes[thz['titre']])
                if cle in Links.keys():
                     Links [cle] +=1
                else:
                    Links [cle] =1
            else:
                cle = (Nodes[thz['IPC3']], Nodes[thz['titre']])
                if cle in Links.keys():
                     Links [cle] +=1
                else:
                     Links [cle] =1
            
      
           
IdxNoeuds = dict()
for noeud in Nodes.keys():
    IdxNoeuds[Nodes[noeud]] = noeud 
Graphdico = dict()

Graphdico ['nodes'] = []
for ind in range(max(IdxNoeuds.keys())+1):
    dicoTemp =dict()
    dicoTemp ['name'] = IdxNoeuds[ind]
    Graphdico ['nodes'].append( dicoTemp)
Graphdico ['links'] = []
for link in Links.keys():
    dicoTemp =dict()
    dicoTemp ['source'] = link [0]
    dicoTemp ['target'] = link [1]
    dicoTemp ['value'] = Links [link]
    Graphdico ['links'].append(dicoTemp)
    
toto = json.dumps(Graphdico, ensure_ascii=False, indent=1)
with open('GraphDisciplineCIBFiltres.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8')) 

toto = json.dumps(HierarchieJsonFin, ensure_ascii=False, indent=1)
#with open('HierarchieDisciplineCIBFiltres.js', 'wb') as ficRes:
#    ficRes.write(b"function getData() {    return "
#                 + toto.encode('utf8')+b" };")  
with open('HierarchieDisciplineCIBFiltres.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))      

#La version sélectionnnant les noeuds les + représentés 
    # SeuilNoeud
Graphdico2 = dict()

Graphdico2 ['nodes'] = []
Graphdico2 ['links'] = []
ExtractLinks = [link for link in Links.keys() if Links[link] >= SeuilNoeud]
ReIndex = dict()
cpt = 0
for ind1, ind2 in ExtractLinks:
    if not ind1 in ReIndex.keys():
        ReIndex [ind1] = cpt
        cpt+=1
    if not ind2 in ReIndex.keys():
        ReIndex [ind2] = cpt
        cpt+=1
NouveauxNoeuds = {ReIndex [ind] :IdxNoeuds[ind] for ind in ReIndex.keys()}
NouveauxLiens = {(ReIndex [ind1], ReIndex [ind2]) : Links[(ind1, ind2)] for ind1, ind2 in ExtractLinks}
#For link in ExtractLinks:
DejaVu = []    
for ind1, ind2 in NouveauxLiens:
    if ind1 not in DejaVu:
        dicoTemp =dict()
        dicoTemp ['name'] = NouveauxNoeuds[ind1]
        Graphdico2 ['nodes'].append( dicoTemp)
        DejaVu.append(ind1)
    if ind2 not in DejaVu:
        dicoTemp =dict()
        dicoTemp ['name'] = NouveauxNoeuds[ind2]
        Graphdico2 ['nodes'].append( dicoTemp)
        DejaVu.append(ind2)
    if ind1 in DejaVu and ind2 in DejaVu:
        dicoTemp =dict()
        dicoTemp ['source'] = ind1
        dicoTemp ['target'] = ind2
        dicoTemp ['value'] = NouveauxLiens [(ind1, ind2)]
        Graphdico2 ['links'].append(dicoTemp)


toto = json.dumps(Graphdico2, ensure_ascii=False, indent=1)
with open('GraphDisciplineCIBFiltresSeuilles'+str(SeuilNoeud)+'.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8')) 
    