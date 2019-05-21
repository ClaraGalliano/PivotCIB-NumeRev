# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:18:08 2019

@author: dreymond
"""

import json
import codecs
import copy
import re
from Utils import strip_accents, CheckList, InsereTermesDebut, Nettoie, Phrase_En_Mots
import nltk
import pandas as pd 
stopwords = nltk.corpus.stopwords.words('french')
from fuzzywuzzy import fuzz


with open('DonneesThese3.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
FichierInitial = 'disciplinesInit3.csv'
cpt=0
cptFini=0

indesirables = ['', u'', None, False, [], ' ', "?"]
DicoDisciplines=dict()
SousDiscipline = dict()
with codecs.open(FichierInitial, 'r', 'utf8') as ficDisc:
    disc = ficDisc.readlines()
for lig in disc:
    col = lig.split(";")
    SousDis = list(set([dis.strip() for dis in col[1:]]))
    SousDisLow =[]
    for soudis in SousDis:
        SousDisLow.append(soudis.strip())
        SousDisLow.append(soudis.strip().lower())
        SousDisLow.append(strip_accents(soudis.strip().lower()))
        SousDisLow.append(strip_accents(soudis.strip()))
    SousDis += list(set(SousDisLow))
    if '' in SousDis:
        SousDis.remove('')
    DicoDisciplines[col[0]] = list(set(SousDis))
    #tri par taille pour algo de matching
    DicoDisciplines[col[0]].sort(key=lambda item: (len(item), item), reverse= True)
    #DicoDisciplines[col[0].lower()] = SousDis 
    for sousdis in SousDis:
        SousDiscipline[sousdis] = col[0]
        
    print(col[0], ' --> ', len(DicoDisciplines[col[0]] ))
LstDisc = list(set([thz["discipline"] for thz in LstThz if 'CatIPC' in thz.keys()]))
print ("nb de disciplines", len(LstDisc))
#toto = list(filter(lambda x: x not in [' ', None], SousDiscisp))
#Rangement de départ

if FichierInitial != 'disciplinesInit.csv':
    Prefered = ['géoscience', 'écologie', 'biologie', 'écosystème', 'biologique', 'agriculture', 'agronomique', 'aliment',
                'agroalimentaire']

Ok= 0
NotVus = []
SousDiscisp = list(set(SousDiscipline.keys()))
if '' in SousDiscisp:
    SousDiscisp.remove('')
# tri par ordre inverse de taille (donner préférence aux unités lexicales longues)
SousDiscisp .sort(key=lambda item: (len(item), item), reverse= True)
LstDisc .sort(key=lambda item: (len(item), item), reverse= True)

SousDiscisp = InsereTermesDebut(SousDiscisp, Prefered)

Match = []    
Candidat = copy.copy(DicoDisciplines)
Candidat2 = dict() #version érpurés ne contiendra pas les doublons de l'échantillon
for cle in DicoDisciplines.keys():
    Candidat[cle] = []
   # Candidat2[cle] = []
for dis in LstDisc:
    compteMatch = 0

    if len(dis)>1:
        if dis not in SousDiscisp and dis.lower() not in SousDiscisp and dis.lower().strip() not in SousDiscisp:
            for disc in SousDiscisp:
                if len(disc)>1:
                    if disc in dis.lower() or strip_accents(disc) in dis.lower():
                        Others = [[].extend(Candidat[dom]) for dom in Candidat.keys() if dom !=SousDiscipline[disc]]
                        if dis not in Others and dis.lower() not in Others and \
                        strip_accents(dis) not in Others and strip_accents(dis.lower()) not in Others: 
                           Candidat[SousDiscipline[disc]].append(dis)
                           Candidat[SousDiscipline[disc]].append(strip_accents(dis))
                           Candidat[SousDiscipline[disc]].append(dis.lower())
                           Candidat[SousDiscipline[disc]].append(strip_accents(dis.lower()))
                          # Candidat2[SousDiscipline[disc]].append(dis)
                         
                           Match.append((dis,disc))
                           compteMatch += 1
                           break 
                        else:
                           print ("inconsistance")
                    else:
                        print ()
        else:
            if dis in SousDiscipline.keys():
                Candidat[SousDiscipline[dis]].append(dis)
                Candidat[SousDiscipline[dis]].append(dis.lower())
                Candidat[SousDiscipline[dis]].append(strip_accents(dis))
                Candidat[SousDiscipline[dis]].append(dis.lower().strip())
                Candidat[SousDiscipline[dis]].append(strip_accents(dis.lower()))
                #Candidat2[SousDiscipline[dis]].append(strip_accents(dis.lower()))
                
               
                
            elif dis.lower() in SousDiscipline.keys():
                #Candidat2[SousDiscipline[dis.lower() ]].append(dis.lower())
                Candidat[SousDiscipline[dis.lower()]].append(dis)
                Candidat[SousDiscipline[dis.lower()]].append(dis.lower())
                Candidat[SousDiscipline[dis.lower()]].append(strip_accents(dis))
                Candidat[SousDiscipline[dis.lower()]].append(dis.lower().strip())
                Candidat[SousDiscipline[dis.lower()]].append(strip_accents(dis.lower()))

                           
            else:
                Candidat[SousDiscipline[dis.lower().strip()]].append(strip_accents(dis))
                Candidat[SousDiscipline[dis.lower().strip()]].append(dis)
                Candidat[SousDiscipline[dis.lower().strip()]].append(dis.lower())
                Candidat[SousDiscipline[dis.lower().strip()]].append(strip_accents(dis))
                Candidat[SousDiscipline[dis.lower().strip()]].append(dis.lower().strip())
                Candidat[SousDiscipline[dis.lower().strip()]].append(strip_accents(dis.lower()))
                #Candidat2[SousDiscipline[dis.lower().strip()]].append(dis.lower().strip())

            compteMatch += 1
            Ok+=1

    if compteMatch==0:
        NotVus.append(dis)
Candidat["Autres"] = []
Candidat2['Autres'] = []
for dis in NotVus:
      Candidat["Autres"].append(dis)
      Candidat2['Autres'].append(dis)
print('Après traitement...')      

xdist = lambda x: { idx: fuzz.token_set_ratio( x, y.values[0] ) for (idx, y) in df2.iterrows( ) }
OrdreDisciplines = ['TerreUniversMatiere', 'VIE', 'SHS', 'TechnoScienceAppli', 'FORMELLES', 'TRANSVERSE']
Disciplines= []
SousDiscipline = dict()
for dis in OrdreDisciplines:
    domaine = dis
    compt=0
    Candidat[domaine].sort(key=lambda item: (item, len(item)))
    docs = Candidat[domaine]#[0:100]+Candidat[domaine][len(Candidat[domaine])-151:]
    #docs.sort(key=lambda item: (item, len(item)))
  #  DocMots = [[mot for  mot in re.split('\W+', phrase) if mot not in stopwords] for phrase in docs]
#    DocMots = [mot for phrase in docs for mot in re.split('\W+', phrase) if mot not in stopwords ]
    docs2 = list(set([' '.join(chaine) for chaine in Phrase_En_Mots(docs)]))
#♥    df= pd.DataFrame(docs) # les chaines originales
    df2 = pd.DataFrame(docs2[0:75] + docs2[len(docs2)-75):]) # la version plus propre
    MatriceDistance = pd.DataFrame( { idx: xdist( x.values[0]) for ( idx, x ) in  df2.iterrows( ) } )
    MatriceDistance.sort_values(by=list(MatriceDistance.index), axis='columns', inplace=True, ascending=False)
    MatriceDistance.sort_values(by=list(MatriceDistance.index), axis='index', inplace=True, ascending=False)
    #Themes= ExtraitThemes(lda,  count_vectorizer, 2)
    #for ( idx, x ) in  MatriceDistance.iterrows():
    while MatriceDistance.sum().sum() >0:
        lst = []
        NonTraites = [indice for indice in MatriceDistance.index if indice not in lst]

        for ( idx, x ) in  MatriceDistance.iterrows():
            if idx not in NonTraites:
                for idy, y in x.iteritems():
                    if y>70:
                        lst.append(idy)
                
                Cand = df2.loc[lst]
                if not Cand.empty:
                    LstCandidat = [Cand.values[can][0] for can in Cand if Cand.values[can][0] in  DicoDisciplines[domaine]]
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
    #                    
    #                 #   MatriceDistance.drop(index=ind, axis=0, inplace=True)
#                for idxCol in lst:
#                    if idxCol in MatriceDistance.columns: #+1 in ind or not ?
#                        MatriceDistance.loc[:, idxCol] =0
                        #MatriceDistance.drop(MatriceDistance.columns[idxCol], axis=1, inplace=True )
        #Ici toutes les lignes au dessus du seuil ont été matchées.
        # Reste le reste
        
#            else:
#                SousDomaine = Nettoie(df.loc[idx].values[0].strip(), False)
#                Disciplines.append(SousDomaine)
#                SousDiscipline [df.loc[idx].values[0].strip()] = (domaine, SousDomaine)
#                MatriceDistance.loc[idx, : ] =0
#           
    #MatriceDistance.loc[(MatriceDistance[:] > 0)] & (df['column_name'] <= B)]
#    for (idx, x ) in  MatriceDistance.iterrows():
#        if sum(x)>0:
#            
#            if df.loc[idx].values[0].strip() not in SousDiscipline.keys() and Nettoie(df.loc[idx].values[0].strip(), False) not in SousDiscipline.keys():
#                SousDomaine =Nettoie(df.loc[idx].values[0].strip(), False)
#                SousDiscipline [x.value[0]] = (domaine, SousDomaine)
#                Disciplines.append(SousDomaine)
#            else:
#                pass
#        else:
#            pass
#Vus = []
#for chaine in SousDiscipline.keys():
#    domaine = SousDiscipline[chaine][0]
#    dis = SousDiscipline[chaine][1]
#    if dis not in Vus:
#        Vus.append(dis)
#        if len(chaine)>3 or chaine=='art':
#            DisMulTerm = [dis for dis in Disciplines if len(dis.split())>1]
#            DisMulTerm.sort(key=lambda item: (len(item), item), reverse= True)
#            if len(DisMulTerm)>0:
#                SousDiscipline[chaine] = (domaine, DisMulTerm[0])
#                LstCopains = [chain for chain in SousDiscipline.keys() if chain != chaine and SousDiscipline[chain][1]==dis]
#                Disciplines.remove(dis)
#                for ch in LstCopains:
#                    Vus.append(SousDiscipline[ch][1])
#                    SousDiscipline[ch] = (domaine, DisMulTerm[0])
#    else:
#        pass
Toto = [thz['discipline'] for thz in LstThz if thz['discipline'] not in SousDiscipline.keys()]

for dis in Toto:
    SousDiscipline[dis] = ('Autres', dis.lower())
    
print (len(Toto))
toto = json.dumps(SousDiscipline)
with open('HierarchieDisciplineComplet3.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))
    
HierarchieJson = dict()
HierarchieJsonSimple = dict()
for discip in SousDiscipline.keys():
    if len(discip)>2:
        dicipNettoyee= Nettoie(discip, False)
    else:
        dicipNettoyee=discip
    domaine = SousDiscipline [discip] [0]
    sousdomaine = SousDiscipline [discip] [1]
    if domaine in HierarchieJsonSimple.keys():
        if sousdomaine in HierarchieJsonSimple [domaine].keys():
            if dicipNettoyee not in HierarchieJsonSimple [domaine] [sousdomaine]:
                    HierarchieJsonSimple [domaine] [sousdomaine].append(dicipNettoyee)
            else:
                    pass                
        else:
            
            HierarchieJsonSimple [domaine] [sousdomaine] = []
            HierarchieJsonSimple [domaine] [sousdomaine].append(dicipNettoyee)
    else:
        HierarchieJsonSimple [domaine] = dict()
        HierarchieJsonSimple [domaine] [sousdomaine] = []
        HierarchieJsonSimple [domaine] [sousdomaine].append(dicipNettoyee)
    if domaine in HierarchieJson.keys():
        if sousdomaine in HierarchieJson [domaine].keys():
            HierarchieJson [domaine] [sousdomaine].append(discip)
        else:
            HierarchieJson [domaine] [sousdomaine] = []
            HierarchieJson [domaine] [sousdomaine].append(discip)
    else:
        HierarchieJson [domaine] = dict()
        HierarchieJson [domaine] [sousdomaine] = []
        HierarchieJson [domaine] [sousdomaine].append(discip)
        

toto = json.dumps(HierarchieJson)
with open('HierarchieDisciplineCompletbis3.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))

toto = json.dumps(HierarchieJsonSimple)
with open('HierarchieDisciplineSimplifie23.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))
