import subprocess
import sys


if len(sys.argv) != 8:
    print("Usage: python launch.py <dossier_entree> <nombre_patients> <borne_min> <borne_max> <dossier_sortie> <fichier_parametres> <choix> (o si vous souhaitez réaliser les tests stats)")
    sys.exit(1)

input = sys.argv[1]
nb_patients = sys.argv[2]
borne_min = sys.argv[3]
borne_max = sys.argv[4]
output = sys.argv[5]
param = sys.argv[6]
choix = sys.argv[7]

if int(borne_min) > -4 or int(borne_max) < 4:
    print("Les bornes doivent être comprises entre -4 et 4")
    sys.exit(1)

# Path to the C++ program
chemin_programme_cpp = "anonym_meth/exe/programme_anonymisation"

# List of arguments to pass to the C++ program
arguments_cpp = [input,nb_patients,borne_min, borne_max, output]

# Run the C++ program
try:
    result = subprocess.run([chemin_programme_cpp] + arguments_cpp, check=True)
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution du programme C++ : {e}")

# Lunch the programm

if choix == "o":
    subprocess.run(["python3", "poo_anonyme.py",input, nb_patients, output, param])
else:
    sys.exit(1)
