import subprocess
import sys

input = "data"
nb_patients = "50"
borne_min = "-6"
borne_max = "6"
output = "gener_simulated_data_meth"
param = "parametres.txt"
choix = "o"

# Chemin vers votre programme C++
chemin_programme_cpp = "../anonym_meth/exe/programme_anonymisation"

# Liste des arguments que vous souhaitez passer
arguments_cpp = [input,nb_patients,borne_min, borne_max, output]

# Utilisation de subprocess.run pour exécuter le programme C++
try:
    result = subprocess.run([chemin_programme_cpp] + arguments_cpp, check=True)
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution du programme C++ : {e}")

# Lancer le programme Python

subprocess.run(["python3", "../poo_anonyme.py",input, nb_patients, output, param])