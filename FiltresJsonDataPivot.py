# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
from Utils import strip_accents, CheckList
with open('DonneesThese3.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
# La liste des champs récupérés sur la base des thèses
ChampsInitiaux = ['id', 'dateInsert', 'dateMaj', 'status', 'accessible', 'titre', 
                  'auteurPpn', 'auteur', 'etabSoutenance', 'etabSoutenancePpn', 
                  'dateSoutenance', 'discipline', 'num', 'langueThese', 'personne', 
                  'ppn', 'oaiSetSpec', 'directeurThesePpn', 'directeurTheseNP', 
                  'directeurThese', 'etablissement', 'abstract', 'Date', 'langue', 'CatIPC']
ChampsDataTable = ['id', 'dateInsert', 'dateMaj', 'status', 'accessible', 'titre', 
                   'auteurPpn', 'auteur', 'etabSoutenance', 'etabSoutenancePpn', 
                   'dateSoutenance', 'discipline', 'num', 'langueThese', 'personne', 
                   'ppn', 'oaiSetSpec', 'directeurThesePpn', 'directeurTheseNP', 
                   'directeurThese', 'etablissement', 'abstract', 'Date', 'langue', 
                   'IPC1', 'ScoreIPC1','IPC2', 'ScoreIPC2','IPC3', 'ScoreIPC3',
                    'IPC4', 'ScoreIPC4','IPC5', 'ScoreIPC5']
    
#champs pour pivot
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre', 'Domaine']

#champs conservés pour les exports visualisation hiérarchique
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
cpt=0
cptFini=0

#integration de la hiérarchie des disciplines
DomaineDisciplines = dict() # Dico[Domaine] = "Discipline" <-- contient toutes les variantes lexicales du jeu de données
SousDiscipline = dict() # SousDiscipline [discipline] = Domaine, avec discipline dans DicoDisciplines.keys()
#SousSousDiscipline = dict() 

#Récuparation des hiérarchies
with open('HierarchieDisciplineComplet.json', 'r', encoding='utf8') as ficSrc:
    DicoDisciplines = json.load (ficSrc)
for dico in DicoDisciplines['children']:
#    if isinstance(dico, dict):
        domaine = dico['name']
        
        for dicoN2 in dico['children']:
            if 'children' in dicoN2.keys():
                if 'name' in dicoN2.keys():
                    soudis = dicoN2['name']
                    SousDiscipline[soudis]= (domaine, soudis)
                    for dicoN3 in dicoN2['children']:
                        SousSousdis = dicoN3['name'] 
                        if SousSousdis not in SousDiscipline.keys():
                            SousDiscipline[SousSousdis] = (domaine, soudis)
                        else:
                            if SousDiscipline[SousSousdis] != (domaine, soudis):
                                pass
                                print ('arg')
                elif len(dicoN2['children']) >0:
                    print("arg3")
                else:
                    pass
                
            elif domaine == 'Autres':
                SousDiscipline[dicoN2['name']] = (domaine,dicoN2['name'])
            else:
                print ("?")
    #    else:
#        print()
        
#
indesirables = ['', u'', None, False, [], ' ', "?"]


print (cpt)
print (cptFini)
lstDis = [truc['discipline'] for truc in LstThz]
lstDis = [truc for truc in lstDis if strip_accents(truc.lower()).strip() not in SousDiscipline.keys() ]

evites = 0
LstThz3 = [thz for thz in LstThz if 'CatIPC' in thz.keys()]
for Thz in LstThz:
    Thz2 = dict()
    #toto = Thz.keys()
    try:
        Thz2['SousDiscipline']=SousDiscipline[Thz['discipline']]
    except:
        Thz2['SousDiscipline']='Autres' # çà devrait jamais arriver :-/
        
    for cle in Thz.keys():
        if cle == 'CatIPC': 
                indx =0
                for num in Thz[cle].keys():
                    indx +=1
                    Thz2['IPC'+str(indx)] = Thz[cle][num][0]
                    Thz2['Score'+'IPC'+str(indx)] = Thz[cle][num][1]
        else:
                Thz2[cle] = Thz[cle]
    lstMq = [cle for cle in ChampsDataTable if cle not in  Thz2.keys()]
    for cle in lstMq:
            Thz2  [cle] = ""
    LstThz2.append(Thz2)


#Champs Datatable
# =============================================================================
#  ['id', 'dateInsert', 'dateMaj', 'status', 'accessible', 'titre', 
#                   'auteurPpn', 'auteur', 'etabSoutenance', 'etabSoutenancePpn', 
#                   'dateSoutenance', 'discipline', 'num', 'langueThese', 'personne', 
#                   'ppn', 'oaiSetSpec', 'directeurThesePpn', 'directeurTheseNP', 
#                   'directeurThese', 'etablissement', 'abstract', 'Date', 'langue', 
#                   'IPC1', 'ScoreIPC1','IPC2', 'ScoreIPC2','IPC3', 'ScoreIPC3',
#                    'IPC4', 'ScoreIPC4','IPC5', 'ScoreIPC5']
# =============================================================================

#ChampsDataTable = ChampsInitiaux
#ChampsDataTable.remove("CatIPC") 
#for champs in LstThz2[0].keys():
#    if champs not in ChampsInitiaux:
#        ChampsDataTable.append(champs)
#with open('tempo.html', 'w') as fic:
#    for ch in ChampsInitiaux:
#        fic.write('<th style="width: 2%;">' + ch +'</th>\n')
        
with codecs.open('DataThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz2))        
LstThz2 =[]        
for Thz in LstThz3:
    Thz2 = dict()
    
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
    if 'IPC3' in Thz2.keys() and len(Thz2['IPC3']) >0 and Thz2['discipline'] != '?':
        LstThz2.append(Thz2)
    else:
        evites += 1
print ('Theses ignorées', evites)
with codecs.open('PivotThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz2))
