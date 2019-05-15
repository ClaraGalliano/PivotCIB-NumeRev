# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
with open('DonneesThese3.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
ChampsNouveau.sort()
cpt=0
cptFini=0


indesirables = ['', u'', None, False, [], ' ', "?"]
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

print (cpt)
print (cptFini)

evites = 0
LstThz3 = [thz for thz in LstThz if 'CatIPC' in thz.keys() and 'discipline' in thz.keys()]

with codecs.open('DisciplineEtendu2.csv', 'r', 'utf8') as ficDisc:
    disc = ficDisc.readlines()
DicoDisciplines = dict()
SousDiscipline = dict()
for lig in disc:
    col = lig.split(";")
    SousDis = [dis.strip() for dis in col[1:]]
    SousDisLow =[]
    for soudis in SousDis:
        SousDisLow.append(soudis.strip())
        SousDisLow.append(soudis.strip().lower())
        SousDisLow.append(strip_accents(soudis.strip().lower()))
        
    SousDis += SousDisLow
    SousDis = list(set(SousDis))
    if '' in SousDis:
        SousDis.remove('')
    DicoDisciplines[col[0]] = SousDis
    DicoDisciplines[col[0]].sort(reverse=True)
    for sousdis in SousDis:
        SousDiscipline[sousdis] = col[0]

for Thz in LstThz3:
    Thz2 = dict()
    if Thz["discipline"].lower() in SousDiscipline.keys() or Thz["discipline"].strip().lower()  in SousDiscipline.keys():
        try:
            Thz["discipline"]= SousDiscipline[Thz["discipline"].lower() ]
        except:
            Thz["discipline"]= SousDiscipline[Thz["discipline"].strip().lower() ]
    else:
        print ('bug -->', Thz["discipline"].lower() )
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

LstIpc3 = [thz['IPC3'] for thz in LstThz2]
LstIpc7 = [thz['IPC7'] for thz in LstThz2]
LstIpc11 = [thz['IPC11'] for thz in LstThz2]
LstDiscipl = [thz['discipline'] for thz in LstThz2]
LstIpc3 = list(set(LstIpc3))
LstIpc7 = list(set(LstIpc7))
LstIpc11 = list(set(LstIpc11))

Discipline = dict()
NiveauIPC11 = dict()
NiveauIPC7 = dict()
NiveauIPC3 = dict()
Hierarchie = dict()
Niveau2 = dict()
Niveau3 = dict()
Niveau4 = dict()
feuilles = dict()

LstThz2 = CheckList(LstThz2, indesirables)
inconsistants =0
for thz in LstThz2[:100]:
    if len(thz.keys()) == len(ChampsNouveau):
        #le bout des feuilles
        feuilles = dict()
        feuilles['name'] = thz['titre'].split('[') [0] # n'a ton pas idée de mettre des crochets dans un titre de thèse ....replace('[', '')
        feuilles['size'] = int(thz['score'])
        thz['discipline'] = thz['discipline'].title().replace(' ', '')
        if thz['discipline'] not in Hierarchie.keys():
            Hierarchie[thz['discipline']] = dict()
            Hierarchie[thz['discipline']][thz['IPC3']] = dict()
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles] #dict()
    #        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
                    #Hierarchie[thz['discipline']][thz['IPC3']] =
        elif thz['IPC3'] not in Hierarchie[thz['discipline']].keys():
            Hierarchie[thz['discipline']][thz['IPC3']] = dict()
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles]#dict()
    #        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
    #        else:
    #            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles]
        elif thz['IPC7'] not in Hierarchie[thz['discipline']][thz['IPC3']].keys():
            #Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [] #dict()
    #        if len(thz['IPC11']) > len(thz['IPC7']):
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles]
        
        else:
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']].append(feuilles)
    else:
        inconsistants +=1
print ("entrées supprimées", inconsistants)
#        

HierarchieJson = dict()

HierarchieJson ['children'] = []

def HierarchiseD3 (Hier):
    if isinstance(Hier, dict):
        if 'name' in Hier.keys():
            if isinstance(Hier['name'], list):
                Hier['name'] = Hier['name'][0]
            return [Hier]
        else:
            Renvoi = []
            for cle in Hier.keys():
                if cle == "F03B001":
                    print()
                dico = dict()
                Child = []
                dico["name"] = cle[0:20]
                if isinstance(Hier[cle], dict):
                    Child.append(HierarchiseD3(Hier[cle]))
                    
                elif isinstance(Hier[cle], list):
                    for dic in Hier[cle]:
                        Child.append(HierarchiseD3(dic))     
                else:
                    print ('wtf')
                if isinstance(Child, list):
                    if len(Child)>1 and isinstance(Child[0], dict):
                        dico['children'] = Child
                    elif len(Child)>1 and not isinstance(Child[0], dict):
                        Child = [temp[0] for temp in Child]
                        dico['children'] = Child
                    else:
                        dico['children'] = Child[0]
                    
                Renvoi.append(dico)
                
            return Renvoi
    elif isinstance(Hier, list):
        Renvoi = []
        for dic in Hier:
            if isinstance(dic, dict):
                Child.append(HierarchiseD3(dic))
            elif isinstance(dic, list):
                for lstdic in dic:
                    Child.append(lstdic)
            else:
                print ('wtf')
        Renvoi.append(Child)
        dico['children'] = Renvoi
        return dico
    else:
        print ('wtf2')
                                     
                      
HierarchieJson["children"] = HierarchiseD3(Hierarchie)
HierarchieJson ['name'] = "Eau"
toto = json.dumps(HierarchieJson, ensure_ascii=False, indent=1)
with open('DonneesHierarchieDiscipline.js', 'wb') as ficRes:
    ficRes.write(b"function getData() {    return "
                 + toto.encode('utf8')+b" };")  
with open('DonneesHierarchieDiscipline.json', 'wb') as ficRes:
    ficRes.write(toto.encode('utf8'))      

