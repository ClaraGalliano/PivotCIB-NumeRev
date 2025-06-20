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
                print ("wtf  ", terme) # si on passe là on n'a pas une correspondance unique pour un terme
                
with open('DonneesTheseEtendues.json', 'r') as ficSrc:
    LstThz = json.load (ficSrc)

def MatchSection(ch):
    #la fonction principale pour le rangement des disciplines
    if len(ch) <3: # si c'est tout petit hop dans la case je sais pas
        return ('Autres', '1000', ch)
    #une jolie fonction de distance lexicale : addition de distance de Leveinshtein caractère par caractère,puis l
    # même sur la chaine nettoyée de tout sauf lettre ANSI puis la 
    # même indépendante de la position de mots et la même partielle
    # çà matche bien sur le jeu de de données... plus c'est grand plus c'est proche... dist (X, X) = 400
    # biais potentiel : la chaine nettoyée qui est vide ou guère mieux...
    distFonct = lambda x: { cle: max([fuzz.ratio( x, mot) for mot in Section[cle]])+\
                           max([fuzz.ratio( Nettoie(x, True), Nettoie(mot, True)) for mot in Section[cle]])+
                           max([fuzz.token_set_ratio( Nettoie(x, True), Nettoie(mot, True)) for mot in Section[cle]])+\
                           max([fuzz.partial_ratio( Nettoie(x, True), Nettoie(mot, True)) for mot in Section[cle]]) for cle in Section.keys()
                           }
    distRef = distFonct(ch)
    # on prend le résultat qu maximise la fonction
    LstCandidat = [cle for cle, val in distRef.items() if val == max(distRef .values())]
    if len(LstCandidat) ==1: # un seul candidat
        if isinstance(Section[LstCandidat[0]], list):
            disc = Discip [ Section[LstCandidat[0]][0]]
            return (disc[0], disc[1], Section[LstCandidat[0]][0])
        else:
            disc = Discip [ Section[LstCandidat[0]]]
            return (disc[0], disc[1], Section[LstCandidat[0]])
    elif len(LstCandidat) ==0:
        print ('aille ', ch)
    else:
#        distFonct2 = lambda x: { cle: 100*x.count(mot) for mot in Section[cle] for cle in Section.keys()} 

        distFonct2 = lambda x: { cle: distRef [cle] + sum([x.count(mot) for mot in Section[cle]]) for cle in Section.keys()}
        distRef2 = distFonct2(ch)
        LstCandidat2 = [cle for cle, val in distRef2.items() if val == max(distRef2 .values())]
        if len(LstCandidat2) ==1:
            if isinstance(Section[LstCandidat2[0]], list):
                disc = Discip [ Section[LstCandidat2[0]][0]]
                return (disc[0], disc[1], Section[LstCandidat2[0]][0])
            else:
                disc = Discip [ Section[LstCandidat2[0]]]
                return (disc[0], disc[1], Section[LstCandidat2[0]])
        elif len(LstCandidat) ==0:
            print ('aille2 ', ch)
        else:
            print ('autres -->', ch)
            return ('Autres', '1000', ch)
        
       

for thz in LstThz:
    Classe = MatchSection(thz['discipline'])
#    print (thz['discipline'] + ' --> '+ str(Classe))
    thz['Domaine'] = Classe[0]
    thz['Section'] = Classe[1]
    thz['DiscipNorm'] = Classe[2]

toto = json.dumps(LstThz, ensure_ascii=False, indent=1)
#with open('HierarchieDisciplineCIBFiltres.js', 'wb') as ficRes:
#    ficRes.write(b"function getData() {    return "
#                 + toto.encode('utf8')+b" };")  
with open('DonneeThzEtendues.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))  

DomaineDis = dict()
for thz in LstThz:
    if thz['Domaine'] in DomaineDis.keys():
        if thz['Section'] in DomaineDis[thz['Domaine']].keys():
            if thz['DiscipNorm'] in DomaineDis[thz['Domaine']][thz['Section']].keys():
                DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']].append(thz['discipline'])
            else:
                DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']] = dict()
                DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']] = [thz['discipline']]
        else:
            DomaineDis[thz['Domaine']][thz['Section']]= dict()
            DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']] = dict()
            DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']] = [thz['discipline']]
    else:
        DomaineDis[thz['Domaine']] = dict()
        DomaineDis[thz['Domaine']][thz['Section']]= dict()
        DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']] = dict()
        DomaineDis[thz['Domaine']][thz['Section']][thz['DiscipNorm']] = [thz['discipline']]
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
with open('HierarchieDicipline.json', 'wb') as ficRes:
    ficRes.write(tutu.encode('utf8'))
    