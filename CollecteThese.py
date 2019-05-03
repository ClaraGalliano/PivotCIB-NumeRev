# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 09:57:51 2016

@author: dreymond
"""

import requests
import time

Res = ''
for param in range(1, 3000, 1000):
    url='http://www.theses.fr/?q=%22Econometrie%22&start='+str(param)+'&format=csv'
    page = requests.get(url)
    time.sleep(4)
    Res+= page.text.replace('\n\n', '\n')

with open('ScrapThese4.csv', 'w') as ficRes:
    ficRes.write(Res)
    