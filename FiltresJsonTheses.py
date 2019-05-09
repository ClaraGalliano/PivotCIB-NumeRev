# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:35:57 2019

@author: dreymond
"""
import json
import codecs
with open('DonneesThese2.json', 'r', encoding='utf8') as ficSrc:
    donnees = json.load (ficSrc)
    
LstThz = donnees
LstThz2 = []
ChampsInitiaux = ['Id','discipline','Date','Langue','titre','Résumé','IPC1','ScoreIPC1','IPC2','ScoreIPC2','IPC3','ScoreIPC3','IPC4','ScoreIPC4','IPC5','ScoreIPC5']
ChampsEpures = ['discipline','Date','Langue','CatIPC', 'titre']
ChampsNouveau  = ['discipline','Date','score','IPC3','IPC7', 'IPC11', 'titre']
cpt=0
cptFini=0

print (cpt)
print (cptFini)
with codecs.open('DataThese.json', 'w', 'utf8') as ficRes:
    ficRes.write(json.dumps(LstThz))
evites = 0
LstThz3 = [thz for thz in LstThz if 'CatIPC' in thz.keys()]
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

LstIpc3 = [thz['IPC3'] for thz in LstThz2]
LstIpc7 = [thz['IPC7'] for thz in LstThz2]
LstIpc11 = [thz['IPC11'] for thz in LstThz2]

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
#for thz in LstThz2:
#    #le bout des feuilles
#    feuilles['name'] = thz['titre'].title().replace(' ', '')
#    feuilles['value'] = int(thz['IPC11'][1])
##    if thz['IPC11'][0] in NiveauIPC11.keys():
##        NiveauIPC11[thz['IPC11'][0]].append(feuilles)
##    else:
##        NiveauIPC11[thz['IPC11'][0]] =  []
##        NiveauIPC11[thz['IPC11'][0]].append(feuilles)
##    if thz['IPC7'][0] in NiveauIPC7.keys():
##        NiveauIPC7[thz['IPC7'][0]].append(thz['IPC7'])
##    else:
##        NiveauIPC7[thz['IPC7'][0]] =  []
##        NiveauIPC7[thz['IPC7'][0]].append(thz['IPC7'])
##    if thz['IPC3'][0][0:4] in NiveauIPC3.keys():
##        NiveauIPC3[thz['IPC3'][0][0:4]].append(thz['IPC3'][0][0:4])
##    else:
##        NiveauIPC3[thz['IPC3'][0][0:4]] =  []
##        NiveauIPC3[thz['IPC3'][0][0:4]].append(thz['IPC3'][0][0:4])      
#    if thz['discipline'] in Discipline.keys():
#        Discipline [thz['discipline']].append(thz['IPC3'][0][0:4])
#    else:
#        Discipline [thz['discipline']] =  []
#        Discipline [thz['discipline']].append(thz['IPC3'][0][0:4]) # Niveau 1
#    if thz['discipline'] not in Niveau2.keys():
#        Niveau2[thz['discipline']] = [thz['IPC3']]
#    else:
#        Niveau2[thz['discipline']].append(thz['IPC3'])
#    if thz['discipline'] not in Niveau3.keys():
#        Niveau3[thz['discipline']] = dict()
#        Niveau3[thz['discipline']][thz['IPC3']] =[thz['IPC7']]
#    else:
#        #if thz['IPC7'] not in Niveau3[thz['discipline'][thz['IPC3']]:
#        Niveau3[thz['discipline']][thz['IPC3']].append(['IPC7'])
#    if thz['discipline'] not in Niveau4.keys():
#        Niveau4[thz['discipline']] = dict()
#        Niveau4[thz['discipline']][thz['IPC3']] =dict()
#        Niveau4[thz['discipline']][thz['IPC3']][thz['IPC7']] = [thz['IPC11']]
#    elif thz['IPC3'] in Niveau4[thz['discipline']].keys():
#        if thz['IPC7'] in Niveau4[thz['discipline']][thz['IPC3']].keys():
#            Niveau4[thz['discipline']][thz['IPC3']][thz['IPC7']].append(thz['IPC11'])
#        else:
#            Niveau4[thz['discipline']][thz['IPC3']][thz['IPC7']] = 
#            Niveau4[thz['discipline']][thz['IPC3']][thz['IPC7']] 
            
        #if thz['IPC7'] not in Niveau3[thz['discipline'][thz['IPC3']]:
        
for thz in LstThz2[0:100]:
    #le bout des feuilles
    feuilles = dict()
    feuilles['name'] = thz['titre']#.title().replace(' ', '')
    feuilles['size'] = int(thz['score'])
    thz['discipline'] = thz['discipline'].title().replace(' ', '')
    if thz['discipline'] not in Hierarchie.keys():
        Hierarchie[thz['discipline']] = dict()
        Hierarchie[thz['discipline']][thz['IPC3']] = dict()
        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = dict()
        if len(thz['IPC11']) > len(thz['IPC7']):
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
        else:
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles]
        #Hierarchie[thz['discipline']][thz['IPC3']] =
    elif thz['IPC3'] not in Hierarchie[thz['discipline']].keys():
        Hierarchie[thz['discipline']][thz['IPC3']] = dict()
        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = dict()
        if len(thz['IPC11']) > len(thz['IPC7']):
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
        else:
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles]
    elif thz['IPC7'] not in Hierarchie[thz['discipline']][thz['IPC3']].keys():
        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = dict()
        if len(thz['IPC11']) > len(thz['IPC7']):
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
        else:
            Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [feuilles]
    elif thz['IPC11'] not in Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']].keys() and len(thz['IPC11']) > len(thz['IPC7']):    
        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
    else:
        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']].append(feuilles)
#        
#        
#        Hierarchie[thz['discipline']].append(thz['IPC3'])
#    if thz['IPC3'] not in Hierarchie[thz['discipline']].keys():
#        Hierarchie[thz['discipline']] = dict()
#        Hierarchie[thz['discipline']][thz['IPC3']] =[thz['IPC7']]
#    else:
#        #if thz['IPC7'] not in Niveau3[thz['discipline'][thz['IPC3']]:
#        Hierarchie[thz['discipline']][thz['IPC3']].append(thz['IPC7'])
#    if thz['IPC7'] not in Hierarchie[thz['discipline']][thz['IPC3']].keys():
#        Hierarchie[thz['discipline']][thz['IPC3']] = dict()
#        Hierarchie[thz['discipline']][thz['IPC3']] =dict()
#        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']] = [thz['IPC11']]
#    else:
#        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']].append[thz['IPC11']]
#    if thz['IPC11'] not in Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']].keys():
#        #Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [dict()]
#        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']] = [feuilles]
#      
#    else:
#        Hierarchie[thz['discipline']][thz['IPC3']][thz['IPC7']][thz['IPC11']].append(feuilles)

HierarchieJson = dict()

HierarchieJson ['children'] = []

def RenvoiListeEntree(Hier):
    if isinstance(Hier, dict):
        Name = list(Hier.keys())
        Child = []
        for cle in Hier.keys():
            if isinstance(Hier[cle], dict):
                Child.append(RenvoiListeEntree(Hier[cle]))
                #return {"Name": Name, "Children" : Child}
            else:   
                Child.append(str(Hier[cle]))
        return {"Name": Name, "Children" : Child}
    else:
        return Hier
    
def RenvoiListeEntree3(Hier):
    if isinstance(Hier, dict):
        #Name = list(Hier.keys())
        if 'name' in Hier.keys():
#            on doit être sur les feuilles
            return Hier
        else:
            Renvoi = []
            for cle in Hier.keys():
                dico = dict()
                Child = []
                dico["name"] = cle
                if isinstance(Hier[cle], dict):
                    
                    Child.append(RenvoiListeEntree3(Hier[cle]))
                    #return {"Name": Name, "Children" : Child}
                elif isinstance(Hier[cle], list):
                    if len(Hier[cle])>1:
                        dico = dict()
                        Child = []
                        for dic in Hier[cle]:
                            Child.append(RenvoiListeEntree3(dic))
                        dico['children'] = Child
#                        else:
#                            dico['children'] = Child [0]
                        #dico['size'] = len(Hier[cle])
                        
#                        dico['size'] = len(Hier[cle])
                        Renvoi.append(dico)
                        return Renvoi
                    else:
                        return Hier[cle][0]
                if len(Child)>1:
                    dico['children'] = Child
                else:
                    dico['children'] = Child [0]
#                dico['children'] = Child
#                dico['size'] = len(Hier[cle]) 
                Renvoi.append(dico)
            return Renvoi
    elif isinstance(Hier, list):
        if len(Hier)>1:
            dico = dict()
            Child = []
            for dic in Hier:
                Child.append(RenvoiListeEntree3(dic))
            if len(Child)>1:
                dico['children'] = Child
            else:
                dico['children'] = Child [0]
            
            Renvoi.append(dico)
            return Renvoi
        else:
            return RenvoiListeEntree3(Hier)
    else:
        return Hier # on devrait jamais être là
    
    
def RenvoiListeEntree4(Hier):
    if isinstance(Hier, dict):
        #Name = list(Hier.keys())
        if 'name' in Hier.keys():
#            Hier['size'] = Hier['size']
            return Hier
        else:
            Renvoi = []
            for cle in Hier.keys():
                dico = dict()
                Child = []
                dico["name"] = cle
                if isinstance(Hier[cle], dict):
                    
                    Child.append(RenvoiListeEntree4(Hier[cle]))
                    #return {"Name": Name, "Children" : Child}
                elif isinstance(Hier[cle], list):
                    if len(Hier[cle])>1:
                        dico = dict()
                        Child = []
                        for dic in Hier[cle]:
                            Child.append(RenvoiListeEntree4(dic))
                        if len(Child)>1:
                            dico['children'] = Child
                        else:
                            dico['children'] = Child [0]

                        Renvoi.append(dico)
                        
                    else:
                        Child =  RenvoiListeEntree4(Hier[cle][0])
                        if isinstance(Child, list):
                            if len(Child)>1:
                                dico['children'] = Child
                            else:
                                dico['children'] = Child [0]
                        elif 'name' in Child.keys():
                            dico = Child
                        
                else:
                    print('?()')
                
#                dico['children'] = Child
#                dico['size'] = len(Hier[cle]) 

            return Renvoi
    else:
        return Hier # on devrait jamais être là
    
HierarchieJson["children"] = RenvoiListeEntree4(Hierarchie)
HierarchieJson ['name'] = "Eau"
toto = json.dumps(HierarchieJson, ensure_ascii=False, indent=2)
with open('DonneesHierarchieDiscipline.js', 'wb') as ficRes:
    ficRes.write(b"function getData() {    return "
                 + toto.encode('utf8')+b" };")  
#     
#for dis in Hierarchie.keys():
#    Niveau1 = dict()
#    Niveau1['name']= dis
#    for ipc3 in Hierarchie[dis].keys():
#        if 'children' in Niveau1.keys():
#            Niveau1["children"].append(ipc3) 
#        else:
#            Niveau1["children"] = []
#            Niveau1["children"].append(ipc3) 
#    if 'children' in Hierarchie.keys():
#        HierarchieJson['children'].append(Niveau1) 
#    else:
#        HierarchieJson['children'] = []
#        HierarchieJson['children'].append(Niveau1) 
