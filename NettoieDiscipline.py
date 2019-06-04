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
        if col not in dicoRef.keys() and len(col)>1:
            dicoRef [col] = lig[0]
#            dicoRef [col.strip()] = lig[0]
#            dicoRef [col.strip().lower()] = lig[0]
#            dicoRef [strip_accents(col.strip())]  = lig[0]
            dicoRefNet [Nettoie(col, False)] = lig[0]
            
            
        else:
           if len(col.strip())>0:
               print ('alert', col)

# ablation des ots en trop, espace et tout le toutim         
Discip2 = list(set([' '.join(chaine) for chaine in Phrase_En_Mots(Discip) if len(chaine)>0]))

xdist = lambda x: { idx: fuzz.token_set_ratio( x, y.values[0] ) for (idx, y) in df2.iterrows( ) }
xdistRef = lambda x: { cle: fuzz.ratio( x, Nettoie(cle, False))  for cle in dicoRef.keys() }
OrdreDisciplines = ['TerreUniversMatiere', 'VIE', 'SHS', 'TechnoScienceAppli', 'FORMELLES', 'TRANSVERSE', 'Autres']
Disciplines= []
SousDiscipline = dict()

Calc = True
df2 = pd.DataFrame(Discip2) 
if Calc:
    MatriceDistance = pd.DataFrame( { idx: xdist( x.values[0]) for ( idx, x ) in  df2.iterrows( ) } )
    MatriceDistance.to_pickle('dist2.pkl')
else:
    #chargement mémoire disque
    MatriceDistance = pd.DataFrame(pd.read_pickle("dist2.pkl"))
    # j'avais pas viré le mot vide :-(). Dinc on vire la ligne colonne associée
    MatriceDistance.drop(index=0, inplace=True)
    MatriceDistance.drop(columns=0, inplace=True)
    #on reindexe
    MatriceDistance.reset_index(drop=True, inplace=True)
    #idem pour les colonnes
    MatriceDistance.set_axis(labels=MatriceDistance.index, axis=1, inplace = True)
    

LstRef = list(dicoRef.keys())
LstRef.sort(key=lambda item: (len(item), item), reverse = True)

#Ponderation par les termes du dico de référence
if Calc:

    for ( idx, x ) in  df2.iterrows():
        if x.values[0] not in LstRef:
            
            DistRef = xdistRef(Nettoie(x.values[0], False))
            Max = max(DistRef.values())
            test = [cle for cle in DistRef.keys() if DistRef[cle] == Max]
            
            if len(test) ==1 and Max == 100:
                #LE cas cool
                ind = [idex for ( idex, y ) in  df2.iterrows() if y.values[0] == test[0] or Nettoie(y.values[0], False) == Nettoie(test[0], False)]
                if len(ind) >0:
                    MatriceDistance.loc[idx,ind[0]] += 100
                else:
                    pass
            else:
                for mot in test:
                    ind = [idex for ( idex, y ) in  df2.iterrows() if y.values[0] == mot or Nettoie(y.values[0], False) == Nettoie(mot, False)]
                    if len(ind) >0:
                        MatriceDistance.loc[idx,ind[0]] += 100
                    else:
                        pass
            
        else:
            
            MatriceDistance.loc[ idx, idx] += 100
    MatriceDistance.to_pickle('distPonderee.pkl')
    
else:
    MatriceDistance = pd.DataFrame(pd.read_pickle("distPonderee.pkl"))      
#MatriceDistance.sort_values(by=list(MatriceDistance.index), axis='columns', inplace=True, ascending=False)
#MatriceDistance.sort_values(by=list(MatriceDistance.index), axis='index', inplace=True, ascending=False)        

while MatriceDistance.sum().sum() >0:
    lst = []
    NonTraites = [indice for indice in MatriceDistance.index if indice not in lst]

    for ( idx, x ) in  MatriceDistance.iterrows():
        if idx in NonTraites:
            for idy, y in x.iteritems():
                if y>=100:
                    lst.append(idy)
            
            Cand = df2.loc[lst]
            if not Cand.empty:
                LstCandidat = [Cand.values[can][0] for can in Cand if Cand.values[can][0] in  dicoRef.keys() or Nettoie(Cand.values[can][0], False) in dicoRefNet.keys()]
                LstCandidat.sort (key=len, reverse = True)
                
                if len(LstCandidat)<1:
                    SousDomaine = Nettoie(Cand.values[len(Cand)-1][0].strip(), False)
                    
                else:
                    SousDomaine = LstCandidat [0]
                Disciplines.append(SousDomaine)
                for discip in Cand.values:
                     
                    CheckDelta = [(soudom,fuzz.partial_ratio (SousDomaine, soudom))  for soudom in Disciplines if soudom != SousDomaine if fuzz.partial_ratio (SousDomaine, soudom) >80]
                    if len(CheckDelta)>0:
                        LstRatios = [ratio  for dom, ratio in CheckDelta]
                        
                        Best = [dom for dom, ratio in CheckDelta if ratio == max(LstRatios)]
                        if len (set(Best)) ==1:
                            if len(Best[0].split() )< len(SousDomaine.split()):
                                Disciplines.remove(SousDomaine)
                                TrucNettoyes =  [dicip for dicip in SousDiscipline.keys() if SousDiscipline[dicip][1] ==SousDomaine]
                                SousDomaine = Best[0]
                                for dis in TrucNettoyes:
                                
                                    TrucNettoyes [dis] = (domaine, SousDomaine)
                                SousDomaine = Best[0]
                                
                            else:
                                pass
                        else: # plisuers canddats...
                            Done = False
                            Best.sort(key=len)
                            for can in Best:
                                if len(can.split() )< len(SousDomaine.split()):
                                    Disciplines.remove(SousDomaine)
                                    TrucNettoyes =  [dicip for dicip in SousDiscipline.keys() if SousDiscipline[dicip][1] ==SousDomaine]
                                    SousDomaine = can
                                    for dis in TrucNettoyes:
                                        TrucNettoyes [dis] = (domaine, SousDomaine)
                                    
                                    Done = True
                            if not Done:
                                print (CheckDelta)

                        
                    SousDiscipline [discip[0]] = (domaine, SousDomaine)
                #SousDiscipline [SousDomaine] = (domaine, SousDomaine)
               # print (SousDomaine)
                for ind in lst:
                    #if ind in MatriceDistance.index: 
                        MatriceDistance.loc[ind,:]=0
                        MatriceDistance.loc[:, ind]=0
        else:
            pass
    IdxCandidatsReste =  [idx for ( idx, x ) in  MatriceDistance.iterrows() if x.sum()>0]
    CandidatsReste = df2.loc[IdxCandidatsReste]
    for discip in CandidatsReste.values: 
        SousDomaine = discip [0]
        CheckDelta = [(soudom,fuzz.partial_ratio (SousDomaine, soudom))  for soudom in Disciplines if soudom != SousDomaine if fuzz.partial_ratio (SousDomaine, soudom) >80]
        if len(CheckDelta)>0:
            LstRatios = [ratio  for dom, ratio in CheckDelta]
            Best = [dom for dom, ratio in CheckDelta if ratio == max(LstRatios)]
            if len (set(Best)) ==1:
                    if len(Best[0].split() )< len(SousDomaine.split()):
                        Disciplines.remove(SousDomaine)
                        TrucNettoyes =  [dicip for dicip in SousDiscipline.keys() if SousDiscipline[dicip][1] ==SousDomaine]
                        SousDomaine = Best[0]
                        for dis in TrucNettoyes:
                            TrucNettoyes [dis] = (domaine, SousDomaine)
                    else:
                        pass
            else: # plisuers canddats...
                print (CheckDelta)
                for best in Best:
                    if len(best[0].split() )< len(SousDomaine.split()):
                            Disciplines.remove(SousDomaine)
                            
                            #nettoyage des autres
                            TrucNettoyes =  [dicip for dicip in SousDiscipline.keys() if SousDiscipline[dicip][1] ==SousDomaine]
                            SousDomaine = best[0]
                            for dis in TrucNettoyes:
                                TrucNettoyes [dis] = (domaine, SousDomaine)
                                

                    else:
                        pass
            SousDiscipline [discip[0]] = (domaine, SousDomaine)
       
    for ind in CandidatsReste:
#                    if ind in MatriceDistance.index: 
                    MatriceDistance.loc[ind,:]=0
                    MatriceDistance.loc[:, ind]=0

#labels=list(range(num_clusters))
#Preclusters = km2.labels_.tolist()
 
#terms = vectorizer.get_feature_names()