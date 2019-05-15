# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
import copy
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

# insertion des mots "préférentiels" au début 
# pour éviter que par ex. Science des aliments ne se retrouve en 
#Attention à ce qu'ils soient dans le dictionnaire d'initialisation
#Mettre les termes en minuscule correctement accentués
if FichierInitial!='disciplinesInit.csv':
    Prefered = ['géoscience', 'écologie', 'biologie', 'écosystème', 'biologique', 'agriculture', 'agronomique', 'aliment']
    def InsereTermesDebut(Liste, ListeTerme):
        for mot in ListeTerme:
            Liste.insert(0, mot)
            Liste.insert(0, strip_accents(mot))
        return Liste
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
                           Candidat[SousDiscipline[disc]].append(dis)
                           Candidat[SousDiscipline[disc]].append(strip_accents(dis))
                           Candidat[SousDiscipline[disc]].append(dis.lower())
                           Candidat[SousDiscipline[disc]].append(strip_accents(dis.lower()))
                           Candidat2[SousDiscipline[disc]].append(dis.title().replace(' ', ''))
                           Match.append((dis,disc))
                           compteMatch += 1
                           break                       
        else:
            if dis in SousDiscipline.keys():
                Candidat2[SousDiscipline[dis]].append(dis)
            elif dis.lower() in SousDiscipline.keys():
                Candidat2[SousDiscipline[dis.lower() ]].append(dis.lower()) 
            else:
                Candidat2[SousDiscipline[dis.lower().strip() ]].append(dis.lower().strip())
            compteMatch += 1
            Ok+=1

    if compteMatch==0:
        NotVus.append(dis)
Candidat["autre"] = []
for dis in NotVus:
      Candidat["autre"].append(dis)

print('Après traitement...')      

with codecs.open("DisciplineEtendu3.csv", 'w', 'utf8') as ficRes:
    for domaine in Candidat.keys():
        lstSousDis=list(set(Candidat[domaine]))
        lstSousDis.sort()
        ficRes.write(domaine+';')
        for disc in lstSousDis:
            ficRes.write(disc+';')
        ficRes.write('\n')
        print (domaine, ' --> ', len(lstSousDis))
        
#creation d'un export Json
HierarchieJson= dict()
HierarchieJson['name'] = 'Disciplines'
HierarchieJson['children'] = []

for dis in Candidat.keys():
    dicoTemp = dict()
    dicoTemp['name'] = dis
    dicoTemp['children'] = list(set(Candidat[dis]))
    HierarchieJson['children'].append(dicoTemp)
toto = json.dumps(HierarchieJson, ensure_ascii=False, indent=1)
with open('HierarchieDiscipline.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8')) 

HierarchieJson2= dict()
HierarchieJson2['name'] = 'Disciplines'
HierarchieJson2['children'] = []

for dis in Candidat2.keys():
    dicoTemp = dict()
    dicoTemp['name'] = dis
    dicoTemp['children'] = list(set(Candidat2[dis]))
    HierarchieJson2['children'].append(dicoTemp)
toto = json.dumps(HierarchieJson2, ensure_ascii=False, indent=1)
with open('HierarchieDiscipline2.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8')) 