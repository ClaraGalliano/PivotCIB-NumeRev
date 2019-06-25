# Utilisation de la classification internationnale des brevets comme pivot de lecture de l'interdisciplinarité
# Instruments de lecture

Le lecteur trouvera dans ce dépôt les différents outils utilisés pour notre présentation (https://www.youtube.com/watch?v=-WHoTXw6Two) au colloque Numerev (http://numerev.com/programme-colloque-numerev.html).
Ci après quelques éléments complémentaires.
L'ensemble des scripts sont sous python 3, developpés à l'aide de la suite Anaconda3.

## Script de collecte de données bibliométrique de la base des thèses françaises (these.fr)
 **CollecteThese.py** pas très élégant mais efficace. Il suffit d'adapter la ligne 12 valeur de 'requete' à vos besoins. Respectueux de robots.txt ne pas changer la valeur du time.sleep.
 La ligne 13 correspond au nom de fichier dans lequel seront écrites les données. 
 
## Script de préparation des données bibliométriques récoltées.
 S'appuie sur un fichier JSON préparé par le script précédent. Va récupérer si possible le résumé des thèses collectées par le script précédent. L'abstract est alors catégorisé par IPCCat 5https://www.wipo.int/classifications/ipc/ipccat?&hierarchiclevel=).
 Une série de CIB (https://www.wipo.int/classifications/ipc/ipcpub/?lang=fr&menulang=fr) et de scores de classement sont ajoutées aux données bibliographiques de la thèse. 
 Le fichier produit (ligne 20) contient les données bibliographiques augmentées de ces deux éléments (résumé et liste CIB)

# L'exploration des résultats
Afin d'accompagner l'exploration des paradigmes proposés, nous proposons différentes interfaces d'exploration situées dans le répertoire **Visualisations**. Les scripts suivant préparent les données
 
 