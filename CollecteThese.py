# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 09:57:51 2016

@author: dreymond
"""

import requests
import time
import json

requete='eau'
fichierRes = 'ListeThese.json'
Res = ''
time.sleep(3)
param = 0
url = "http://theses.fr/fr/?q=&zone1=abstracts&val1="+requete+"&op1=AND&zone2=auteurs&val2=&op2=AND&zone3=etabSoutenances&val3=&op3=AND&zone4=dateSoutenance&val4a=&val4b=&start="+str(param)+"&format=json"
page = requests.get(url)

if page.ok:
    reponse = page.json()
    if reponse['response']['numFound']>1000:
        docs = reponse['response']['docs']
        for param in range(10, reponse['response']['numFound'], 10):
            url = "http://theses.fr/fr/?q=&zone1=abstracts&val1="+requete+"&op1=AND&zone2=auteurs&val2=&op2=AND&zone3=etabSoutenances&val3=&op3=AND&zone4=dateSoutenance&val4a=&val4b=&start="+str(param)+"&format=json"
            page = requests.get(url)
            if page.ok:
                reponse = page.json()
                docs.extend(reponse['response']['docs'])
            else:
                print ('pas bon là')
            time.sleep(3)
else:
    print ("vous devriez changer la requête")

with open(fichierRes, 'w') as ficRes:
    json.dump(docs, ficRes)
