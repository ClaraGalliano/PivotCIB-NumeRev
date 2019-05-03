# -*- coding: utf-8 -*-

"""
Created on Tue Feb 02 13:36:47 2016

@author: dreymond
"""

import cPickle as pickle
import codecs
import sys
reload (sys)
sys.setdefaultencoding("utf8")

these = dict()
RESUME = """"""
try:
    with open("DonneesThez4.pkl", "r") as DoneFic:
        while 1:
            try:
                temp = pickle.load(DoneFic)
                if temp[1]['resume'] not in RESUME:
                    these [temp[0]] = temp [1]
                    RESUME+= these [temp[0]]['resume']
            except EOFError:
                break
except:
    pass

print str(len(these.keys())), ' thess chargees',

with codecs.open("TheseComIramuteq4.txt", "w", 'utf-8') as ficRes:
    for IdThese in these.keys():
        if  these [IdThese]['resume'].count("Information non disponible")==0 and these [IdThese]['resume'].count(u"Pas de résumé en français")==0 and these [IdThese]['resume'].count(u"Pas de résumé")==0:
            these [IdThese]['resume'] = these [IdThese]['resume'].replace('’', "'")
            these [IdThese]['resume'] = these [IdThese]['resume'].replace('#', "")
            these [IdThese]['resume'] = these [IdThese]['resume'].replace(u' »', '"')
            these [IdThese]['resume'] = these [IdThese]['resume'].replace(u'« ', '"')
            these [IdThese]['resume'] = these [IdThese]['resume'].replace('<span property="dc:description" xml:lang="fr">', '')
            these [IdThese]['resume'] = these [IdThese]['resume'].replace('&', '')
            these [IdThese]['resume'] = these [IdThese]['resume'].replace(u'’', "'")
            these [IdThese]['resume'] = these [IdThese]['resume'].replace(u"``", "'")
            these [IdThese]['resume'] = these [IdThese]['resume'].replace(u"''", "'")
            these [IdThese]['resume'] = these [IdThese]['resume'].replace(u"©", "")
            Entete = '**** *Auteur_'+ ''.join(these[IdThese]['Auteur'].split(' '))
            try:
                Entete += ' *Date_'+these[IdThese]['DateS'][6:]
            except:
                Entete += ' *Date_EnCours'
            if isinstance(these [IdThese]['DirecteurThese'], list):
                for dire in these [IdThese]['DirecteurThese']:
                    Entete2 = Entete+' *Dir_'+''.join(dire.split(' '))
                    #copying for as many dire in direction research
                    Entete2 += ' \n'
                     
                    ficRes.write(Entete2)
                    ficRes.write(these [IdThese]['resume'])
                    ficRes.write(' \n')
                    ficRes.write(' \n')
            else:            
                Entete += ' *Dir_'+''.join(these [IdThese]['DirecteurThese'].split(' '))
                Entete += ' \n'
                ficRes.write(Entete)
                ficRes.write(these [IdThese]['resume'])
                ficRes.write(' \n')
                ficRes.write(' \n')


