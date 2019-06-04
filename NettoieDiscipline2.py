# -*- coding: utf-8 -*-
"""
Created on Mon May 27 08:34:00 2019

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
FichierInitial = 'disciplinesInitBis.csv'

with open(FichierInitial, "r", encoding = 'utf8') as FicRef:
    dataRef = FicRef.readlines()

dicoRef = dict()
dicoRefNet = dict()
for lig in dataRef:
    lig = lig.strip().split(';')
    for col in lig [1:]:
        if col.title() not in dicoRef.keys() and len(col)>1:
            dicoRef [col.title()] = lig[0]
#            dicoRef [col.strip()] = lig[0]
#            dicoRef [col.strip().lower()] = lig[0]
#            dicoRef [strip_accents(col.strip())]  = lig[0]
            if len(Nettoie(col, False))>1:
                dicoRefNet [Nettoie(col, False)] = lig[0]
            else:
                dicoRefNet [col] = lig[0]
            
            
        else:
           if len(col.strip())>0:
               print ('alert', col)

# ablation des ots en trop, espace et tout le toutim         
Discip2 = list(set([' '.join(chaine) for chaine in Phrase_En_Mots(Discip) if len(chaine)>0]))
xdistRef2 = lambda x: { cle: fuzz.token_set_ratio( x, cle)  for cle in dicoRef.keys() }
xdistRef1 = lambda x: { cle: fuzz.ratio( x, cle)  for cle in dicoRef.keys() }
xdist = lambda x: { idx: fuzz.token_set_ratio( x, y.values[0] ) for (idx, y) in df2.iterrows( ) }
xdistRef = lambda x: { cle: fuzz.ratio( x, Nettoie(cle, False))  for cle in dicoRef.keys() }
OrdreDisciplines = ['TerreUniversMatiere', 'VIE', 'SHS', 'TechnoScienceAppli', 'FORMELLES', 'TRANSVERSE', 'Autres']
Domaine= dict()
Disciplines = dict()
SousDiscipline = dict()
df2 = pd.DataFrame(Discip)

for (idx, x) in df2.iterrows():
    if len(x.values[0]) >1:
        dist = xdistRef1(x.values[0])
        LstCandidat = [cle for cle, val in dist.items() if val == max(dist.values())]
        if len( LstCandidat) ==1:
            if dicoRef[LstCandidat[0]] in Domaine.keys():
                if LstCandidat[0] in Domaine[dicoRef[LstCandidat[0]]].keys():
                    Domaine[dicoRef[LstCandidat[0]]][LstCandidat[0]].append(x.values[0])
                else:
                    Domaine[dicoRef[LstCandidat[0]]][LstCandidat[0]] = [x.values[0]]
            else:
                Domaine[dicoRef[LstCandidat[0]]] = dict()
                Domaine[dicoRef[LstCandidat[0]]][LstCandidat[0]] = [x.values[0]]
        elif len( LstCandidat) >1:
            dist2 = xdistRef2(x.values[0])
            LstCandidat2 = [cle for cle, val in dist2.items() if val == max(dist2.values())]
            LstCandidat2.sort(key=lambda item: (item, len(item)))
            TestRef=[truc for truc in LstCandidat2 if truc in x.values[0]]
            if len(TestRef)>0:
                TestRef.sort(key=lambda item: (item, len(item)))
                LstCandidat2 = TestRef
            if LstCandidat2[0] == "Sciences" and len(LstCandidat2) >1:    
                 LstCandidat2[0] =  LstCandidat2[1] 
            if dicoRef[LstCandidat2[0]] in Domaine.keys():
                if LstCandidat2[0] in Domaine[dicoRef[LstCandidat2[0]]].keys():
                    Domaine[dicoRef[LstCandidat2[0]]][LstCandidat2[0]].append(x.values[0])
                else:
                    Domaine[dicoRef[LstCandidat2[0]]][LstCandidat2[0]] = [x.values[0]]
            else:
                Domaine[dicoRef[LstCandidat2[0]]] = dict()
                Domaine[dicoRef[LstCandidat2[0]]][LstCandidat2[0]] = [x.values[0]]
            print ( LstCandidat2, ' <-- ', x.values[0])
        else:
            print (x.values[0])