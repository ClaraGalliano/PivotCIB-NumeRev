# -*- coding: utf-8 -*-
"""
Created on Sat May  4 09:19:35 2019

@author: dreymond
"""

def IPCCategorizer(texte, langue):
    import requests
    import xmltodict
    from requests.utils import requote_uri
    import time
#    version="20190101" #valid scheme version
    language=langue # or fr, es, de, ru
    number="5" #from 1 to 5
    level= "subgroup" # or class, subclass, maingroup
    # The API service of IPC cat
    
    urlDer = "https://www.wipo.int/classifications/ipc/ipccat?&hierarchiclevel="+level.upper()+"&lang="+language +\
    "&numberofpredictions="+number+"&text="+texte.lower().replace("\n", " ")
    urlDer = requote_uri(urlDer)
    time.sleep(3)
    try:
        req=requests.get(urlDer)
        if req.ok:
            return xmltodict.parse(req.text)
        else:
            pass
    except:
        print("pb")
    return None
    
def IPCExtractPredictions(Predic, seuil):
    Predict = [] # Les prédiction d'IPC dont le score dépasse le seuil
    if 'predictions' in Predic.keys():
        if "msg" in Predic['predictions'].keys():
            if Predic['predictions']['msg'] == 'ok':
                for predic in Predic['predictions']['prediction']:
                    if int(predic["score"]) > seuil:
                        Predict.append(predic)
                    else:
                        pass
            else:
                return None
        else:
            return None
    else:
        return None
    return Predict