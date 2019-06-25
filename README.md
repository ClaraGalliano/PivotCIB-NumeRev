# ProjetNumeRev
Faire dialoguer les disciplines via l'indexation des connaissances : thèse en ligne, réservoir et P2N

**Objectif** : tester l'utilisation de la classification internationnale des brevets comme pivot de lecture de l'interdisciplinarité
**Sous objectif** : proposer des instruments de lecture et d'exploration des données collectées

Le lecteur trouvera dans ce dépôt les différents outils utilisés pour notre présentation (https://www.youtube.com/watch?v=-WHoTXw6Two) au colloque Numerev (http://numerev.com/programme-colloque-numerev.html).
Ci après quelques éléments complémentaires.
L'ensemble des scripts sont sous python 3, developpés à l'aide de la suite Anaconda3.

## Script de collecte de données bibliométrique de la base des thèses françaises (these.fr)
 **CollecteThese.py** pas très élégant mais efficace. Il suffit d'adapter la ligne 12 valeur de 'requete' à vos besoins. Respectueux de robots.txt ne pas changer la valeur du time.sleep.
 La ligne 13 correspond au nom de fichier dans lequel seront écrites les données. 
 
## Script de préparation des données bibliométriques récoltées.
 S'appuie sur un fichier JSON préparé par le script précédent. Va récupérer si possible le résumé des thèses collectées par le script précédent. L'abstract est alors catégorisé par IPCCat 
 (https://www.wipo.int/classifications/ipc/ipccat?&hierarchiclevel=).
 Une série de CIB (https://www.wipo.int/classifications/ipc/ipcpub/?lang=fr&menulang=fr) et de scores de classement sont ajoutées aux données bibliographiques de la thèse. 
 Le fichier produit (ligne 20) contient les données bibliographiques augmentées de ces deux éléments (résumé et liste CIB)

## Script de "Nettoyage des disciplines"
Les données ont nécessité la mise en place d'un nettoyage du champ "disciplines" tant la variété au plan lexical sctrict était importante (3307 disciplines différentes pour 16790 thèses). 
Sans prétention le script TraiteDisicipline.py s'appuie sur un dictionnaire créé (le 08/06/2019) à partir de la description des sections disciplinaires du site du CNU (http://www.cpcnu.fr/listes-des-sections-cnu). 
Le dictionnaire utilisé est au format csv selon la nomenclature (Domaine;Numéro de section;[liste lexicale;]) cf. 'DisciplinesCNU.csv).
Le script utilise une distance de Levenshtein améliorée pour pouvoir rapprocher indifféremment les tailles de chaines et les positions de mots au mieux aux entrées du dictionnaire. Cf. fonction MatchSection.
Le script a été lancé plusieurs fois et le dictionnaire récursivement adapté en rajoutant des termes pour qu'ils soient associés à la "bonne" section (Note le but était de réduire la variété des données pour faciliter la lecture.
Nous avons créé un domaine transverse et des numéros associés à ce domaine pour séparer ce que nous ne pouvions classer... 
Les auteurs ne s'engagent en rien sur la position éventuelle d'une (ou plusieurs) "sous"-discipline(s) dans une section erronée, ni sur les horribles choix potentiels que nous avons du faire pour les besoins de la lecture ! 
Reste aussi que l'algorithme de classement et de rapprochement des unités lexicales est performable.
Le script construit un fichier JSON reprennant les données bibliographiques de thèse précédentes et rajoute, pour chaque thèse, les champs :
1. "domaine" : le domaine disciplinaire (DEG, SCIENCES, LSH1,2, Pharmacie; Transverse)
2. "section" : le numéro de section CNU (1 à 77 + quelques entrées au dessus de 100)
3. "DiscipNorm" : la discipline "normalisée", première entrée dans le dictionnaire csv après le numéro de section. 

# Filtrage et préparation des données
Les scripts suivants préparent les données pour les visualisations (cf. infra)
1. FiltresJsonDataPivot.py
Export des données pour datable et pivotable. 
2. FiltreJson

# L'exploration des résultats

Afin d'accompagner l'exploration des paradigmes proposés, nous proposons différentes interfaces d'exploration situées dans le répertoire **Visualisations**. 
Les outils d'explorations incluent :
1. Un type tableur (cf. https://datatables.net/)
2. Un tableur pour croisement de données et visualisations sur champs prédeterminés et modifiables (https://pivottable.js.org/examples/)
3. Un ensemble de visualisations fondées sur les Data-Driven Documents [D3.js ](https://d3js.org/). Les visualisations sont construites selon le paradigme des "observables", une forme de Notebook 
(inexploitée dans notre cas @Gérald, il s'agit ici de générateurs de Notebook réutilisables dans d'autres contexte ou simplement en étude de cas issues de these.fr) qui sépare la construction
de la vue (fichier HTML) qui inmporte un fichier javascript 'runtime.js' pour lire le js correspondant à la visualisation correspondante (répertoire Visualisations/@d3/). 
Ce dernier importe le fichier JSON au format compatible pour cette visualisation (répertoire '/Visusalisation/JSON'



 
 