# README

## DESCRIPTION

Anonymisation de séries temporelles multivariées, associées à des traces d’événements

Ce code permet d'anonymiser un jeu de données, en ajoutant des fluctuations, dans un intervalle désiré par l'utilisateur. De plus, des tests statistiques seront fournis afin d'évaluer la qualité de cette anonymisation par rapport au jeu de données initial.

## INSTALLATION

### Dépendance Python

Assurez-vous d'avoir Python et pip installés. Ensuite, exécutez la commande suivante pour installer les dépendances nécessaires:

```bash
pip install -r /tools/requirements.txt 


Il convient ensuite de compiler le programme C++. Pour ce faire, éxécutez les commandes suivantes :

cd anonym_meth

make

Ensuite retournez dans le répertoire courant :

cd ..
```

## UTILISATION

- Premièrement, dans votre fichier de paramètres vous devez renseigné deux paramètres comme ceci :

    - output_folder: <nom_du_fichier_de_sortie>
    - nombre_samples: <nombre_d'échantillons>

- Création d'un répertoire pour stocker les données anonymisées

- Lancement du script launch.py :
    - python3 launch.py <dossier_entrée> <nombre_patients> <borne_inférieure> <borne_supérieure> <dossier_sortie> <fichier_parametres> <choix>
        - <dossier_entree> : nom du fichier avec vos données brutes
        - <nombre_patients> : Le nombre de patients présents dans votre dossier d'entrée
        - <borne_inférieure> <borne_supérieure> : Intervalle dans lequel un pourcentage aléatoire sera séélectionné pour anonymiser les données. La borne inférieure doit être inférieure à -4 et la borne supérieure, au delà de 4.
        - <dossier_sortie> : nom du dossier ou seront stockés vos données anonymisées.
        - <fichier_parametres> : nom de votre fichier paramètres, qui se situe au même niveau que le programme
        - <choix> : Si vous souhaitez réalisez les test statistiques, mettez "o" sinon pour générer seulement les données anonymisées : "n".

### Exemple d'utilisation

python3 launch.py data 1000 -8 8 output parametres.txt o

## OUTPUT 

### stats

Dans ce dossier, vous obtiendrez les valeurs min, max, la moyenne, la variance et l'écart-type pour chaque paramètre physiologique, et ce, pour l'ensemble des patients.

### tests

Pour chacun des patients anonymes, un certain nombre de patients réels ont été sélectionnés de manière aléatoire (10 recommandés). Nous avons ensuite calculé la DTW univariée entre les patients anonymes et les patients réels pour chaque paramètre physiologique (FC, PAS, PAD, PAM). Ensuite, nous avons calculé la DTW multivariée (DTWm) comme la moyenne des 4 DTW univariées précédentes. Nous conservons la DTWm_min minimale sur les 10 patients réels. Nous avons calculé la moyenne (E) et l'écart type (S) sur toutes les DTWm_min, en normalisant chaque dissimilarité.
Ainsi, pour chaque paramètre physiologique, vous obtenez 5 fichiers, car vous obtenez également la distance selon le paramètre statistique.


### Répertoire courant

Un graphique montrant la distribution des données entre patient réels et anonymisés ainsi qu'un fichier csv, contenant les valeurs brutes.
