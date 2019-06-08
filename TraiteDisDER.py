# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 09:07:46 2019

@author: dreymond
"""
import json
from fuzzywuzzy import fuzz
from Utils import strip_accents, CheckList, InsereTermesDebut, Nettoie, Phrase_En_Mots, GetIPCDefinition, FiltreChamps

#import dico Ref
with open('DisciplinesCNU.csv', 'r', encoding='utf8') as fic:
    data = fic.readlines()
Domaines = dict()
Section = dict()
Hierar = dict()  
SousSection = dict() 
for lig in data:
    lig=lig.strip()
    col = lig.split(';')
    if col[0] in Domaines.keys():
        Domaines[col[0]].append(col[1]) # Domaines --> Section
       
        if col[1] in Section.keys():
            Section[col[1]].append([truc for truc in col[2:] if len(truc)>0])
        else:
            Section[col[1]] = [truc for truc in col[2:] if len(truc)>0]
    else:
        Domaines[col[0]]=[col[1]]
        if col[1] in Section.keys():
            Section[col[1]].append(col[2:])
        else:
            Section[col[1]] = [truc for truc in col[2:] if len(truc)>0]
    if '-' in col[1]:
        sousec= col[1].split('-')
        if sousec[0] in SousSection.keys():
            SousSection[sousec[0]].append(col[1])
        else:
            SousSection[sousec[0]] = [col[1]]
            
            
 
Discip = dict()
for dom in Domaines:
    if dom not in Hierar.keys():
        Hierar[dom] = dict()
    for sec in Domaines[dom]:
        if sec not in Hierar[dom].keys():
            Hierar[dom][sec] = []
        for terme in [mot for mot in Section[sec] if len(mot)>0]:
            if terme not in Hierar[dom][sec]:
                Hierar[dom][sec].append(terme)
            if terme not in Discip.keys():
                Discip[terme] = (dom, sec)
            else:
                print ("wtf") # si on passe là on n'a pas une correspondance unique pour un terme
                
with open('DonneesTheseEtendues.json', 'r') as ficSrc:
    LstThz = json.load (ficSrc)

def MatchSection(ch):
   #                           sum([fuzz.ratio( Nettoie(x, True), Nettoie(mot, True)) for mot in Section[cle]])/len( Section[cle]) for cle in Section.keys()
#                           sum([fuzz.token_set_ratio( x, mot) for mot in Section[cle]])/len( Section[cle])+\
#                           sum([fuzz.token_set_ratio( Nettoie(x, True), Nettoie(mot, True)) for mot in Section[cle]])/len( Section[cle])+\
#                           
    distFonct = lambda x: { cle: sum([fuzz.partial_ratio( Nettoie(x, True), Nettoie(mot, True)) for mot in Section[cle]]) for cle in Section.keys()}
    distRef = distFonct(ch)
    LstCandidat = [cle for cle, val in distRef.items() if val == max(distRef .values())]
    if len(LstCandidat) ==1:
        if isinstance(Section[LstCandidat[0]], list):
            disc = Discip [ Section[LstCandidat[0]][0]]
        else:
            disc = Discip [ Section[LstCandidat[0]]]
        return (disc[0], disc[1], LstCandidat[0])
    elif len(LstCandidat) ==0:
        print ('aille ', ch)
    else:
        return ('Autres', '1000', ch)
#        print (LstCandidat[0] + '--> ', ch)

        return LstCandidat[0]
for thz in LstThz:
    Classe = MatchSection(thz['discipline'])
    print (thz['discipline'] + ' --> '+ str(Classe))
    thz['Domaine'] = Classe[0]
    thz['Section'] = Classe[1]
    thz['DiscipNorm'] = Classe[2]