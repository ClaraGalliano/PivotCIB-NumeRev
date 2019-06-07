# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 07:47:37 2019

@author: dreymond
"""

import json
from Utils import strip_accents, CheckList, InsereTermesDebut, Nettoie, Phrase_En_Mots, GetIPCDefinition, FiltreChamps
import nltk
import pandas as pd 
stopwords = nltk.corpus.stopwords.words('french')
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.externals import joblib
with open('DonneesTheseEtendues.json', 'r') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees

ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre', 'Domaine', 'SousDomaine']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
evites = 0
seuilScore = -1

LstThz2 = FiltreChamps(LstThz, ChampsEpures, seuilScore  )

print()
Discip = list(set([thz ['discipline'] for thz in LstThz2]))

# chargement du dicto de référence
FichierInitial = 'DisciplinesInit.csv'

with open(FichierInitial, "r", encoding = 'utf8') as FicRef:
    dataRef = FicRef.readlines()

DomaineDis = dict()
DisSouDis =[]
DisDomaine = dict()
DicipInit = set()
for lig in dataRef:
    lig = lig.strip().split(';')
    
    if len(lig[0])>1:
        DicipInit.add(lig[1])
        DicipInit.add(Nettoie (lig[1], True))
        DicipInit.add(lig[2])
        DicipInit.add(Nettoie (lig[2], True))
        DisSouDis.append((lig[0], lig[1], lig[2]))
        if lig[2] not in DisDomaine.keys():
            if len(lig[2])>1:
                DisDomaine[lig[2]] =(lig[0], lig[1])
            else:
                pass
#                
        if lig[1] not in DisDomaine.keys():
            DisDomaine[lig[1]] =(lig[0], lig[1])
        else:
            pass

        if (lig[0], lig[1], lig[1]) not in DisSouDis:
            DisSouDis.append((lig[0], lig[1], lig[1]))
            
        if lig[0] not in DomaineDis.keys():
            DomaineDis [lig[0]] = dict()
            DomaineDis [lig[0]][lig[1]] =dict()
            if len(lig[2])>0:
                DomaineDis [lig[0]][lig[1]][lig[2]]=dict()
                if lig[1] not in DomaineDis [lig[0]][lig[1]].keys():
                    DomaineDis [lig[0]][lig[1]][lig[1]]=dict()

            elif lig[1] not in DomaineDis [lig[0]][lig[1]].keys():
                DomaineDis [lig[0]][lig[1]][lig[1]]=dict()
        elif lig[1] not in DomaineDis[lig[0]].keys():
            DomaineDis [lig[0]][lig[1]] =dict()
            if len(lig[2])>0:
                DomaineDis [lig[0]][lig[1]][lig[2]]=dict()
                
            elif lig[1] not in DomaineDis[lig[0]][lig[1]].keys():
                DomaineDis [lig[0]][lig[1]][lig[1]]=dict()
            else:
                pass
        elif len(lig[2])>0:
            if lig[2] not in DomaineDis[lig[0]][lig[1]].keys():
                DomaineDis [lig[0]][lig[1]][lig[2]]=dict()
            else:
                pass
        else:
            pass
    else:
        pass

def CheckDiscip4(ch, Domaines, SousDis ):
    chNet = Nettoie(ch, True)
    CleDis = list(Domaines.keys())
    CleDis.sort(key=lambda item: (len(item), item), reverse = True)
    TropBateaux = ['sciences', 'art', "science"]
    Bateaux = [truc for truc in CleDis if len(truc.split(' '))==1]
    Candidat = []
    if len(chNet)>2:
        if len(chNet.split(' ')) >1:
            for dis in CleDis:
                disNet =  Nettoie(dis, True)
                if len(dis.split(' '))>1:
                    
                    ratio = fuzz.token_set_ratio(chNet, disNet)
                    if ratio >50:
                        Candidat.append((dis, ratio))
                else:
                    if disNet in chNet:
                        if len(Candidat) == 0:
                            Candidat.append((dis, 100))
                        else:
                            if dis in [truc[0] for truc in Candidat]:
                                if dis not in TropBateaux:
                                    Candidat.append((dis, 200))
                            elif chNet in TropBateaux or ch in TropBateaux:
                                pass
                            elif dis not in TropBateaux:
                                    Candidat.append((dis, 200))
                               
            if len(Candidat) ==0:
                print ('azrd', ch)
                
        else:
            if chNet in Domaines.keys():
                return (Domaines[chNet][0], Domaines[chNet][1], chNet)
            else:
                for dis in CleDis:
                    disNet =  Nettoie(dis, True)
                    if len(dis.split(' '))>1:
                        if chNet in dis:
                            if chNet not in TropBateaux:
                                Candidat.append((dis, 100))
                            else:
                                pass
                    else:
                        ratio = fuzz.token_set_ratio(chNet, disNet)
                        if ratio >90:
                            Candidat.append((dis, ratio))
    else:
        for dis in CleDis:
            disNet =  Nettoie(dis, True)
            if len(dis.split(' '))>1:
                if chNet in dis:
                    if chNet not in TropBateaux:
                        Candidat.append((dis, 100))
                    else:
                        pass
            else:
                ratio = fuzz.token_set_ratio(chNet, disNet)
                if ratio >50:
                     Candidat.append(dis,ratio)
                if disNet in chNet:
                    if len(Candidat) == 0:
                        Candidat.append((dis, 100))
                    else:
                        if dis in [truc[0] for truc in Candidat]:
                            Candidat.append((dis, 200))
                        else:
                            pass
    if len(Candidat) ==0:
        return ('Autres', ch)
        
    else:
        Maxou = max([truc[1] for truc in Candidat])
        Restants = [truc for truc in Candidat if truc[1]== Maxou]
        if len(Restants) == 1:
            return (Domaines[Restants[0][0]][0], Domaines[Restants[0][0]][1], Restants[0][0])
        else:
            RestantsBis = [truc for truc in Restants if truc[0] not in TropBateaux]
            if len(RestantsBis) == 0:

                return (Domaines[Restants[0][0]][0], Domaines[Restants[0][0]][1],Restants[0][0])
            elif len(set(RestantsBis)) == 1:
                
                return (Domaines[RestantsBis[0][0]][0], Domaines[RestantsBis[0][0]][1],RestantsBis[0][0])
            else:
                RestantsTer = [truc for truc in RestantsBis if truc[0].lower() not in TropBateaux]
                if len(RestantsTer) ==1:
                    return (Domaines[RestantsTer[0][0]][0], Domaines[RestantsTer[0][0]][1],RestantsTer[0][0])
                else:
                    RestantsTer.sort(key=lambda item: (len(item), item))
                    return (Domaines[RestantsTer[0][0]][0], Domaines[RestantsTer[0][0]][1],RestantsTer[0][0])
                    #print ("aille arg")
                

cpt = 0                    
for chaine in Discip:
    Affect =  CheckDiscip4(chaine, DisDomaine, DisSouDis)
    if len(Affect)<3:
        cpt +=1
    else:
       pass
       
    if  Affect[0] == 'Autres':
        if Affect[0] in DomaineDis.keys():
            if Affect[1] not in DomaineDis['Autres'].keys():
                DomaineDis [Affect[0]][Affect[1]] = chaine
            else:
                cleProche = [truc for truc in DomaineDis['Autres'].keys() if fuzz.ratio(truc, Nettoie(chaine, True))>50]
                if len(cleProche)>1:
                    DomaineDis [Affect[0]][cleProche] = [chaine]
                else:
                    pass # or not ?
    elif Affect[2] in DomaineDis [Affect[0]][Affect[1]].keys():
             if isinstance(DomaineDis [Affect[0]][Affect[1]][Affect[2]], list):
                if chaine not in DomaineDis [Affect[0]][Affect[1]][Affect[2]]:
                    DomaineDis [Affect[0]][Affect[1]][Affect[2]].append(chaine)
                else:
                    pass
             else:
                DomaineDis [Affect[0]][Affect[1]][Affect[2]] = [chaine]
    else:
            DomaineDis [Affect[0]][Affect[1]][Affect[2]] = [chaine]

#export pour tidyTreeDiscipline
hier = dict()
hier ['name'] = "Disciplines et sous-disciplines"
hier ['children'] = [] 
for dom in DomaineDis.keys():
    tempoDict = dict()
    tempoDict ["name"] = dom
    tempoDict ["children"] = []
    for dis in DomaineDis[dom].keys():
        tempoDictDis = dict()
        tempoDictDis ["name"] = dis
        tempoDictDis ["children"] = []
        for sousdis in DomaineDis[dom][dis].keys():
            tempoDictsousDis = dict()
            tempoDictsousDis ["name"] = sousdis
            tempoDictsousDis ["children"] = []
            if isinstance(DomaineDis[dom][dis][sousdis], dict):
                for soussousdis in DomaineDis[dom][dis][sousdis].keys():
                    tempoDictsoussousDis = dict()
                    tempoDictsoussousDis ["name"] = soussousdis
                    tempoDictsoussousDis ["children"] = DomaineDis[dom][dis][sousdis][soussousdis]
                    tempoDictsousDis ["children"].append(tempoDictsoussousDis)
            else:
                for soussousdis in set(DomaineDis[dom][dis][sousdis]):
                    tempoDictsoussousDis = dict()
                    tempoDictsoussousDis ["name"] =soussousdis
                    tempoDictsoussousDis ["size"] = DomaineDis[dom][dis][sousdis].count(soussousdis)
                    tempoDictsousDis ["children"].append(tempoDictsoussousDis)
                
            tempoDictDis ["children"] .append(tempoDictsousDis)
        tempoDict ["children"].append(tempoDictDis)
    hier ['children'].append(tempoDict)
 
tutu = json.dumps(hier, ensure_ascii=False, indent=1)     
with open('HierarchieTest.json', 'wb') as ficRes:
    ficRes.write(tutu.encode('utf8'))
    