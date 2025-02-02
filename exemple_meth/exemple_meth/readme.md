# README

## DESCRIPTION

Anonymisation de séries temporelles multivariées, associées à des traces d’événements

Ce code permet d'anonymiser un jeu de données, en ajoutant des fluctuations, dans un intervalle désiré par l'utilisateur. De plus, des tests statistiques seront fournis afin d'évaluer la qualité de cette anonymisation par rapport au jeu de données initial.

Ceci est un répertoire exemple, permettant de montrer l'efficacité du programme mais sur un petit jeu de données.

## INSTALLATION

### Dépendance Python

Assurez-vous d'avoir Python et pip installés. Ensuite, exécutez la commande suivante pour installer les dépendances nécessaires:

```bash
pip install -r ../tools/requirements.txt 


Il convient ensuite de compiler le programme C++. Pour ce faire, éxécutez les commandes suivantes :

cd ../anonym_meth

make

Ensuite retournez dans le répertoire courant :

cd ../exemple_meth
```

## UTILISATION

- Premièrement, dans votre fichier de paramètres vous devez renseigné deux paramètres comme ceci :

    - output_folder: <nom_du_fichier_de_sortie>
    - nombre_samples: <nombre_d'échantillons>

- Création d'un répertoire pour stocker les données anonymisées

- Lancement du script launch.py :
    - - python3 launch_toy_example.py
