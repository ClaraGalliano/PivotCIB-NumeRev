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

RepertoireDestination ="./Visualisations/JSON/"
seuilScore = 1200

Titres = True #présence des titres dans les graphes (à n'utiliser qu'après avoir beaucoup seuillé ^_^)

IPCDef = GetIPCDefinition()
for Titres in [True, False]:
    for seuilScore in [0, 600, 800, 1000, 1200]: #étapes arbitraires 
        FichierJsonGrapheSeuille = 'GraphDisciplineCIB-' + str(seuilScore)+Titres*'Titre'
        FichierJsonHierarchie = "HierarchieDiscipline-" + str(seuilScore)+Titres*'Titre'
        FichierJsonJoli = "GraphDisciplineCIBJolis-" + str(seuilScore)+Titres*'Titre'
        LstThz2 = []
        evites = 0 # compteur des entrées ignorée (consistance ou seuillage)
        for Thz in LstThz:
            Thz2 = dict()
            for cle in Thz.keys():
                Ok=False
                if cle in ChampsEpures:
                    if cle == 'CatIPC': 
                        if "1" in Thz[cle].keys(): # sélection meilleur résultat de classement 
                            #hiérarchisation
                            
                            Thz2['IPC3'] = Thz[cle]["1"][0][0:4]
                            Thz2['IPC7'] = Thz[cle]["1"][0][0:7]
                            Thz2['IPC11'] = Thz[cle]["1"][0]
                            Thz2['score'] = Thz[cle]["1"][1]
        
                        else:
                            pass
                    else:
                        Thz2[cle] = Thz[cle]
            if 'score' not in Thz2.keys():
                Thz2["score"] = 0
        
            if int(Thz2["score"]) > seuilScore:
                    LstThz2.append(Thz2)
            else:
                    evites += 1
        print ("Seuil de score IPCCat ", seuilScore)
        print ("Nombre d'entrées ignorées (données de thèses non consistantes ou score < seuilScore) : ", evites)
        print ("nombre d'entrée de thèses traitées présentes dans les fichiers JSON pour visualisation :", len(LstThz2))
        
        

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
        
        
        #création des hierarchies au format sunburst et autres
        HierarchieJsonFin = dict()
        HierarchieJsonFin['name'] ="Eau"
        
        HierarchieJsonFin ['children'] = []
        
        HierarchieJsonFin ['size'] = len(IPC7IPC3DiscipSectionDom.keys())
        for dom in IPC7IPC3DiscipSectionDom.keys():
            HierarchieJsonFinDom = dict()
            HierarchieJsonFinDom['name'] = dom
            HierarchieJsonFinDom['children'] = []
            HierarchieJsonFinDom['size'] = len(IPC7IPC3DiscipSectionDom[dom].keys())
            for section in IPC7IPC3DiscipSectionDom[dom].keys():
                tempoDict=dict()
                tempoDict['name'] = section
                tempoDict['children'] = []
                tempoDict['size'] = len(IPC7IPC3DiscipSectionDom[dom][section].keys())
                for discip in IPC7IPC3DiscipSectionDom[dom][section].keys():
                    tempoDiscipDict=dict()
                    tempoDiscipDict['name'] = discip
                    tempoDiscipDict['children'] = []
                    tempoDiscipDict['size'] = len(IPC7IPC3DiscipSectionDom[dom][section][discip].keys())
                    for IPC3 in IPC7IPC3DiscipSectionDom[dom][section][discip].keys():
                        tempotempoDict=dict()
                        tempotempoDict['name'] = IPC3             
                        tempotempoDict['size'] = len(IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3].keys())
                        tempotempoDict['children'] = []  
                        if Titres:
                            for IPC7 in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3].keys():
                                tempotempotempoDict=dict()
                                tempotempotempoDict['name'] = IPC7 
                                tempotempotempoDict['children'] = []
                                for titre in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7]:
                                    TitretempotempotempoDict =dict()
                                    TitretempotempotempoDict['name'] = titre
                                    TitretempotempotempoDict['size'] = 1
                                    tempotempotempoDict['children'].append(TitretempotempotempoDict)
                                tempotempoDict['children'].append(tempotempotempoDict)
                        else:
                            for IPC7 in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3].keys():
                                tempotempotempoDict=dict()
                                tempotempotempoDict['name'] = IPC7 
                                tempotempotempoDict['size'] = len(IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3][IPC7])
                                tempotempoDict['children'].append(tempotempotempoDict)
                            tempotempoDict['size'] = len([IPC7 for IPC7 in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3].keys()])
                        if len(tempotempoDict['children']) ==0:
                                tempotempoDict.pop('children')
                        tempoDiscipDict['children'].append(tempotempoDict)
                    tempoDict['children'].append(tempoDiscipDict)
                HierarchieJsonFinDom['children'].append(tempoDict)
                
            HierarchieJsonFin['children'].append(HierarchieJsonFinDom)
        DumpHierarchie = json.dumps(HierarchieJsonFin, ensure_ascii=False, indent=1)
        with open(RepertoireDestination+FichierJsonHierarchie +'.json', 'wb') as ficRes:
            ficRes.write(DumpHierarchie.encode('utf8'))    
        
        print(" Fichier de Hierachie ", FichierJsonHierarchie +'.json correctement écrit' )                     
        #" création des graphes et des index de noeuds
            
        Nodes = dict()
        Links = dict()
        DejaVu = []
        compteNoeud = 0
        
        for dom in IPC7IPC3DiscipSectionDom.keys():
            
            if dom not in DejaVu:
                Nodes [dom] = compteNoeud
                compteNoeud +=1 
                DejaVu.append(dom)
            for section in IPC7IPC3DiscipSectionDom[dom].keys():
                
                if section not in DejaVu:
                    Nodes [section] = compteNoeud
                    compteNoeud +=1
                    DejaVu.append(section)
                
                for discip in IPC7IPC3DiscipSectionDom[dom][section].keys():
        
                    if discip not in DejaVu:
                        Nodes [discip] = compteNoeud
                        compteNoeud +=1
                        DejaVu.append(discip)
                    
                    
                    for IPC3 in IPC7IPC3DiscipSectionDom[dom][section][discip].keys():
                        if IPC3 not in DejaVu:
                            Nodes [IPC3] = compteNoeud
                            compteNoeud +=1
                            DejaVu.append(IPC3)
                        
                        for IPC7 in IPC7IPC3DiscipSectionDom[dom][section][discip][IPC3].keys():
        
                            if IPC7 not in DejaVu:
                                Nodes [IPC7] = compteNoeud
                                DejaVu.append(IPC7)
                                compteNoeud +=1
        
        
                            if Titres:    
        
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
        
        
        
        for thz in LstThz2:
            if int(thz['score']) >seuilScore:
                cle = (Nodes[thz['Domaine']], Nodes[thz['Section']])
                if cle in Links.keys():
                     Links [cle] +=1
                else:
                    Links [cle] = 1
                cle = (Nodes[thz['Section']], Nodes[thz['DiscipNorm']])
                if cle in Links.keys():
                     Links [cle] +=1
                else:
                    Links [cle] = 1
                cle = (Nodes[thz['DiscipNorm']], Nodes[thz['IPC3']])
                if cle in Links.keys():
                     Links [cle] +=1
                else:
                    Links [cle] = 1
                cle = (Nodes[thz['IPC3']], Nodes[thz['IPC7']])
                if Titres:
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
                else:
                    cle = (Nodes[thz['IPC3']], Nodes[thz['IPC7']])
                    if thz['IPC7'] != thz['IPC3']:
                        if cle in Links.keys():
                             Links [cle] +=1
                        else:
                            Links [cle] = 1
                    
              
                   
        IdxNoeuds = dict()
        for noeud in Nodes.keys():
            IdxNoeuds[Nodes[noeud]] = noeud 
            # le code ci dessous ne fonctionne pas (ou mal) car les neouds sont
            # numérotés selon leur nombre de départ et peuvent suivant les paramètres 
            # de seuillage êtres amenés à disparaitre
#        Graphdico = dict()
#        
#        Graphdico ['nodes'] = []
#        for ind in range(max(IdxNoeuds.keys())+1):
#            dicoTemp =dict()
#            dicoTemp ['name'] = IdxNoeuds[ind]
#            Graphdico ['nodes'].append( dicoTemp)
#        Graphdico ['links'] = []
#        for link in Links.keys():
#            dicoTemp =dict()
#            dicoTemp ['source'] = link [0]
#            dicoTemp ['target'] = link [1]
#            dicoTemp ['value'] = Links [link]
#            Graphdico ['links'].append(dicoTemp)
#            
#        DumpGraphdico = json.dumps(Graphdico, ensure_ascii=False, indent=1)
#        with open(FichierJsonGrapheSeuille +'.json', 'wb') as ficRes:
#            ficRes.write(DumpGraphdico.encode('utf8')) 
        
        #La version réindexant les noeuds  
        
        Graphdico2 = dict()
        
        Graphdico2 ['nodes'] = []
        Graphdico2 ['links'] = []
        ExtractLinks = [link for link in Links.keys()] # if Links[link] >= SeuilNoeud
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
        
        
        DumpGraphdico = json.dumps(Graphdico2, ensure_ascii=False, indent=1)
        with open(RepertoireDestination + FichierJsonJoli +'.json', 'wb') as ficRes:
            ficRes.write(DumpGraphdico.encode('utf8')) 
        print(" Fichier de Graphe ", FichierJsonJoli +'.json correctement écrit' )