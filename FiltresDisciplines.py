# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
import copy
from Utils import Nettoie
from fuzzywuzzy import fuzz

with open('DonneesThese3.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees

ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
FichierInitial = 'disciplinesInit3.csv'
cpt=0
cptFini=0
def strip_accents(text):

    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    import unicodedata
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

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
def CheckList(dico, indesir):
    if isinstance(dico, dict):
        CleASupprimer = [k for k, v in dico.items() if any([v is i for i in indesir])]
        if len(CleASupprimer)>0:
            return False
        else:
            return dico
    elif isinstance(dico, list):
        tempoList =[]
        for dic in dico:
            tempo = CheckList(dic, indesir)
            if tempo:
                tempoList.append(tempo)
        Liste = tempoList
    return Liste

LstDisc = list(set([thz["discipline"] for thz in LstThz if 'CatIPC' in thz.keys()]))
print ("nb de disciplines", len(LstDisc))
Ok= 0
NotVus = []
SousDiscisp = list(set(SousDiscipline.keys()))
if '' in SousDiscisp:
    SousDiscisp.remove('')
# tri par ordre inverse de taille (donner préférence aux unités lexicales longues)
SousDiscisp .sort(key=lambda item: (len(item), item), reverse= True)
LstDisc .sort(key=lambda item: (len(item), item), reverse= True)
def InsereTermesDebut(Liste, ListeTerme):
    for mot in ListeTerme:
        Liste.insert(0, mot)
        Liste.insert(0, strip_accents(mot))
    return Liste
# insertion des mots "préférentiels" au début 
# pour éviter que par ex. Science des aliments ne se retrouve en sciences
#Attention à ce qu'ils soient dans le dictionnaire d'initialisation
#Mettre les termes en minuscule correctement accentués
if FichierInitial!='disciplinesInit.csv':
    Prefered = ['géoscience', "biosciences", 'écologie', 'biologie', 'écosystème', 'biologique', 'agriculture', 'agronomique', 'agronomie', 'aliment',
                'agroalimentaire', "Science du vivant", "Sciences du vivant", "arts et sciences"]

    SousDiscisp = InsereTermesDebut(SousDiscisp, Prefered)

Match = []    
Candidat = copy.copy(DicoDisciplines)
Candidat2 = dict() #version érpurés ne contiendra que les doublons de l'échantillon
for cle in DicoDisciplines.keys():
    Candidat[cle] = []
    Candidat2[cle] = []
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
                           Candidat2[SousDiscipline[disc]].append(dis)
                         
                           Match.append((dis,disc))
                           compteMatch += 1
                           break 
                        else:
                           print ("inconsistance")
        else:
            if dis in SousDiscipline.keys():
                Candidat[SousDiscipline[dis]].append(dis)
                Candidat[SousDiscipline[dis]].append(dis.lower())
                Candidat[SousDiscipline[dis]].append(strip_accents(dis))
                Candidat[SousDiscipline[dis]].append(dis.lower().strip())
                Candidat[SousDiscipline[dis]].append(strip_accents(dis.lower()))
                Candidat2[SousDiscipline[dis]].append(strip_accents(dis.lower()))
                
               
                
            elif dis.lower() in SousDiscipline.keys():
                Candidat2[SousDiscipline[dis.lower() ]].append(dis.lower())
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
                Candidat2[SousDiscipline[dis.lower().strip()]].append(dis.lower().strip())

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

#with codecs.open("DisciplineEtendu3.csv", 'w', 'utf8') as ficRes:
#for domaine in Candidat.keys():
#    lstSousDis=list(set(Candidat[domaine]).union(set(Candidat2[domaine])))
#    lstSousDis.sort(key=lambda item: (len(item), item), reverse= True)
#    Candidat[domaine]= lstSousDis
#    print (domaine, ' --> ', len(lstSousDis))
#toto = json.dumps(Candidat, ensure_ascii=False, indent=1)
#with open('DisciplinesEtendues.json', 'wb') as ficRes:
#    ficRes.write(toto.encode('utf8')) 
#


#creation d'un export Json
HierarchieJson= dict()
HierarchieJson['name'] = 'Disciplines'
HierarchieJson['children'] = []

#for dis in Candidat.keys():
#    dicoTemp = dict()
#    dicoTemp['name'] = dis
#    dicoTemp['children'] = []
#    Candidat[dis]=list(set(Candidat[dis]).union(Candidat2[dis]))
#    Candidat[dis].sort(key=lambda item: (len(item), item), reverse= True)
#    for discip in Candidat[dis]:
#        tempo = dict()
#        tempo['name'] = discip
#        tempo['size'] = Candidat[dis].count(discip)
#        dicoTemp['children'].append(tempo)
#    HierarchieJson['children'].append(dicoTemp)
#toto = json.dumps(HierarchieJson, ensure_ascii=False, indent=1)
#with open('HierarchieDiscipline.json', 'wb') as ficRes:
#    ficRes.write(toto.encode('utf8')) 
#
#
#HierarchieJson2= dict()
#HierarchieJson2['name'] = 'Disciplines'
#HierarchieJson2['children'] = []
#
#print ('sans accents ni majuscules')
#
#for dis in Candidat2.keys():
#    dicoTemp = dict()
#    dicoTemp['name'] = dis
#    dicoTemp['children'] = []
#    Candidat2[dis]= [mot.lower() for mot in Candidat2[dis]] #elimination des casses différentes
#    Candidat2[dis]= [strip_accents(mot) for mot in Candidat2[dis]]#elimination des accents
#    Candidat2[dis]=list(set(Candidat2[dis]))
#    Candidat2[dis].sort()#(key=lambda item: (len(item), item), reverse= True)
#    print (dis, ' --> ', len(Candidat2[dis]))
#    for discip in Candidat2[dis]:
#        tempo = dict()
#        tempo['name'] = discip
#        tempo['size'] = Candidat2[dis].count(discip)
#        dicoTemp['children'].append(tempo)
#    HierarchieJson2['children'].append(dicoTemp)
#toto = json.dumps(HierarchieJson2, ensure_ascii=False, indent=1)
#with open('HierarchieDiscipline2.json', 'wb') as ficRes:
#    ficRes.write(toto.encode('utf8')) 
HierarchieJson3= dict()
SousDiscipline = dict()
HierarchieJson3['name'] = 'Disciplines'
HierarchieJson3['children'] = []
for dis in [ 'VIE','TerreUniversMatiere', 'SHS', 'TechnoScienceAppli', 'FORMELLES', 'TRANSVERSE', 'Autres']:
    dicoTemp = dict()
    dicoTemp['name'] = dis
    dicoTemp['children'] = []
    Candidat2[dis]= [mot.lower() for mot in Candidat2[dis]] #elimination des casses différentes
    Candidat2[dis]= [strip_accents(mot) for mot in Candidat2[dis]]#elimination des accents
    Candidat2[dis]=list(set(Candidat2[dis]))
    Candidat2[dis].sort()#(key=lambda item: (len(item), item), reverse= True)
    print (dis, ' --> ', len(Candidat2[dis]))
    for discip in Candidat2[dis]:
        tempo = dict()
        if len(discip.split())>0:
            tempo['children'] = []
            if dis != 'Autres':
                    tempo['name'] = Nettoie(discip.split()[0], False).strip()
            else:
                    tempo['name'] = discip.split()[0].strip()
            if len(discip.split()[0])>2:
                if dis != 'Autres':
                    tempo['name'] = Nettoie(discip.split()[0], False).strip()
                else:
                    tempo['name'] = discip.split()[0].strip()
                temporar = [terme for terme in Candidat2[dis] if Nettoie(terme, False).startswith(Nettoie(discip.split()[0], False))]
                if len(temporar)>1:
                    dicotemp=dict()
                    dicotemp['name']=Nettoie(discip.split()[0], False)
                    dicotemp['children'] = []
                    dicotemp['size']= len(temporar)
                    for term in temporar:
                        dicotemp2=dict()
                        dicotemp2['name']=term
                        dicotemp2['size']=temporar.count(term)
                        dicotemp['children'].append(dicotemp2)
                        Candidat2[dis].remove(term)
                        if term != Nettoie(discip.split()[0], False):
                            tempo['children'].append(dicotemp2)
                            SousDiscipline [term] = (dis, dicotemp['name'])#, tempo['name'] )
                            
                else:
                    tempo['children'].append({'name': Nettoie(discip, False), 'size':1})
                    SousDiscipline [Nettoie(discip, False)] = (dis, tempo['name'])#tempo['name'] )
        else:
            tempo['name'] = Nettoie(discip, False)
        #tempo['size'] = Candidat2[dis].count(discip)
            SousDiscipline [discip] = (dis, tempo['name'])
        dicoTemp['children'].append(tempo)
        
        
    HierarchieJson3['children'].append(dicoTemp)
toto = json.dumps(HierarchieJson3, ensure_ascii=False, indent=1)
with open('HierarchieDiscipline3.json', 'wb') as ficRes:
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

#Check et insertion dans liste de thèses
ChDisciplines= SousDiscipline.keys()
SousDom = [souDom for dom in HierarchieJson.keys() for souDom in HierarchieJson [dom]]
xdist = lambda x: { val: fuzz.token_set_ratio( x, val ) for val in ChDisciplines if val != x}
with open('DonneesThese3.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
cpt = 0
LstThz = donnees
for thz in LstThz:
    if thz['discipline'] not in SousDiscipline.keys() or Nettoie(thz['discipline'], False).strip() not in SousDiscipline.keys():
        cpt +=1
        if Nettoie(thz['discipline'], False) not in SousDom:
            
            if Nettoie(thz['discipline'], True).strip() not in SousDiscipline.keys():
                Check = xdist(Nettoie(thz['discipline'], True).strip())
                Candidat1 = [truc for truc in Check.keys() if Check[truc] == max(Check.values()) ]
                Candidat1.sort(key=len, reverse = True)
                Check2 = xdist(thz['discipline'])
                Candidat2 = [truc for truc in Check2.keys() if Check2[truc] == max(Check2.values()) ]
                Candidat2.sort(key=len, reverse = True)
                CandidatFinal = [Candidat1[0], Candidat2[0]]
                CandidatFinal.sort(key=len, reverse = True)
                thz['Domaine'] = SousDiscipline [CandidatFinal[0]][0]
                thz['SousDomaine'] = SousDiscipline [CandidatFinal[0]][1]
            else:
                thz['Domaine'] = SousDiscipline [Nettoie(thz['discipline'], True).strip()][0]
                thz['SousDomaine'] = SousDiscipline [Nettoie(thz['discipline'], True).strip()][1]

        else:
            thz['Domaine'] = [dom for dom in HierarchieJson.keys() if Nettoie(thz['discipline'], False) in HierarchieJson[dom]][0]
            thz['SousDomaine'] = Nettoie(thz['discipline'], False)
           # thz['SousSousDomaine'] = Nettoie(thz['discipline'], False)
    elif thz['discipline'] in SousDiscipline.keys():
         thz['Domaine'] = SousDiscipline [thz['discipline']][0]
         thz['SousDomaine'] = SousDiscipline [thz['discipline']][1]

    else:
         thz['Domaine'] = SousDiscipline [Nettoie(thz['discipline'], True).strip()][0]
         thz['SousDomaine'] = SousDiscipline [Nettoie(thz['discipline'], True).strip()][1]
            
    #print (cpt)
for thz in LstThz:
    if 'Domaine' not in thz.keys():
        print ("ARG")
toto = json.dumps( LstThz )      
with open('DonneesTheseEtendues.json', 'wb') as ficSrc:
    donnees = ficSrc.write (toto.encode('utf8'))

LstThz2 = [thz for thz in LstThz if len(thz['titre'])!=0 and len(thz['discipline'])!=0]
toto = json.dumps( LstThz2 )      
with open('DonneesTheseEtenduesFiltrees.json', 'wb') as ficSrc:
    donnees = ficSrc.write (toto.encode('utf8'))        