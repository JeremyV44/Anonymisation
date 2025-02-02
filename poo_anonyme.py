from logging.config import fileConfig
import os
from typing import Any
import numpy as np
from dtaidistance import dtw
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import matplotlib
matplotlib.use('Agg')
import time
import sys
import seaborn as sns
# **************************
# DataProcessor Class
# **************************

class DataProcessor:
    def __init__(self, dossier_anonyme, dossier_data, num_patients, num_samples):
        self.dossier_anonyme = dossier_anonyme
        self.dossier_data = dossier_data
        self.num_patients = int(num_patients)
        self.num_samples = int(num_samples)

    def load_patients_data(self, patient_id, is_anonymous=True):
        # Load patient data from the specified folder and file
        dossier = self.dossier_anonyme if is_anonymous else self.dossier_data
        fichier = os.path.join(dossier, f"{patient_id}_anonyme.csv" if is_anonymous else f"{patient_id}_series.txt")

        if os.path.exists(fichier):
            return pd.read_csv(fichier, sep=',').reset_index(drop=True)
        else:
            print(f"Le fichier anonyme correspondant à {patient_id} n'a pas été trouvé. Ignoré.")
            return None

    def calculate_dtw(self, series1, series2):
        # Calculate Dynamic Time Warping distance between two time series
        series1 = series1.astype(np.float64)
        series2 = series2.astype(np.float64)

        return dtw.distance_fast(np.asarray(series1), np.asarray(series2))

# **************************
# AnalysisGenerator Class
# **************************

class AnalysisGenerator:
    def __init__(self, data_processor, output_folder):
        self.data_processor = data_processor
        self.output_folder = output_folder

    def generate_physio_stats(self):
        # Generate statistics for physiological parameters
        param_physio = ['FC', 'PAS', 'PAM', 'PAD']
        stats = ["avg", "std", "med", "min", "max"]

        for physio in param_physio:
            for stat in stats:
                anonym_list, real_list = [], []

                for i in range(1, self.data_processor.num_patients + 1):
                    anonym = self.data_processor.load_patients_data(i)
                    real = self.data_processor.load_patients_data(i, False)
                    if anonym is not None:
                        anonym_list.append(self.calculate_statistics(anonym[physio], stat))
                    if real is not None:
                        real_list.append(self.calculate_statistics(real[physio], stat))

                df = pd.DataFrame({f"{stat}_anonyme": anonym_list,
                                   f"{stat}_real": real_list})
                output_file = f"stats/{stat}_value_meth_{physio}.csv"
                self.save_to_csv(output_file, df)

    def generate_dtw_analysis(self):
        # Generate analysis based on Dynamic Time Warping (DTW) distance
        min_dtwm_list = []

        for patient_id in range(1, self.data_processor.num_patients + 1):
            data_anonymous = self.data_processor.load_patients_data(patient_id)
            data_real = self.data_processor.load_patients_data(patient_id, False)

            if data_anonymous is not None and data_real is not None:
                dtw_univariate_list = []
                min_dtwm_temp = float('inf')

                for _ in range(self.data_processor.num_samples):
                    patient_real = data_real.sample()

                    dtw_univariate = []
                    for feature in ['FC', 'PAS', 'PAM', 'PAD']:
                        if feature in data_anonymous.columns and feature in patient_real.columns:
                            if not data_anonymous[feature].empty and not patient_real[feature].empty:
                                dtw_univariate.append(self.data_processor.calculate_dtw(
                                    data_anonymous[feature], patient_real[feature]))

                    dtw_m = np.mean(dtw_univariate)
                    dtw_univariate_list.append(dtw_m)

                    min_dtwm_temp = min(min_dtwm_temp, dtw_m)

                min_dtwm_list.append(min_dtwm_temp)

        if min_dtwm_list:
            mean_dtwm = np.mean(min_dtwm_list)
            std_dtwm = np.std(min_dtwm_list)

            min_dtwm_normalized = [(dtw_m - mean_dtwm) / std_dtwm for dtw_m in min_dtwm_list]

            self.save_to_csv('distri_dissim_norm_meth.csv', {'dissim_norm': min_dtwm_normalized})
            self.generate_boxplot('boxplot_meth.png', min_dtwm_normalized)

    def calculate_statistics(self, data, stat):
        # Calculate various statistics (e.g., average, standard deviation) for the given data
        if stat == "avg":
            return data.mean()
        elif stat == "std":
            return data.std()
        elif stat == "med":
            return data.median()
        elif stat == "min":
            return data.min()
        elif stat == "max":
            return data.max()
        else:
            raise Exception("Statistique non reconnue")

    def generate_boxplot(self, filename, data):
        # Generate a boxplot for the given data and save it to a file
        plt.figure(figsize=(8, 8))
        sns.boxplot(y=data, color='skyblue', width=0.3)
        plt.title('Distribution des distances normalisées', fontsize=16)
        plt.xlabel('Patients Anonymes', fontsize=14)
        plt.ylabel('DTWm_min Normalisée', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig(os.path.join(self.output_folder, filename), bbox_inches='tight')
        plt.close()

    def save_to_csv(self, filename, data):
        # Save data to a CSV file
        output_file = os.path.join(self.output_folder, filename)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        pd.DataFrame(data).to_csv(output_file, index=False)

# **************************
# StatisticsGenerator Class
# **************************

class StatisticsGenerator:
    def __init__(self, data_processor, output_folder):
        self.output_folder = output_folder
        self.data_processor = data_processor

    def load_stat_data(self, physio, stat, is_anonymous=True):
        # Load statistical data from a CSV file
        dossier = f"{self.output_folder}/stats"
        filename = os.path.join(dossier, f"{stat}_value_meth_{physio}.csv")

        if os.path.exists(filename):
            return pd.read_csv(filename, sep=',').reset_index(drop=True)
        else:
            return None

    def save_to_csv(self, filename, data, subdirectory="tests"):
        # Save data to a CSV file in the specified subdirectory
        output_file = os.path.join(self.output_folder, subdirectory, filename)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        pd.DataFrame(data).to_csv(output_file, index=False)

    def perform_statistical_tests(self, series1, series2):
        # Perform statistical tests (Kolmogorov-Smirnov, Mann-Whitney U, Euclidean distance)
        statKS, pvalKS = scipy.stats.ks_2samp(series1, series2)

        statWMW_p, pvalWMW_p = scipy.stats.mannwhitneyu(series1, series2, alternative='two-sided')

        statWMW_up, pvalWMW_up = scipy.stats.ranksums(series1, series2)

        dist_euclidean = np.sqrt(np.mean((series1 - series2) ** 2))

        return statKS, pvalKS, statWMW_p, pvalWMW_p, statWMW_up, pvalWMW_up, dist_euclidean

    def generate_statistical_tests(self):
        # Generate statistical tests for physiological parameters and statistics
        param_physio = ['FC', 'PAS', 'PAM', 'PAD']
        stats = ["avg", "std", "med", "min", "max"]

        for physio in param_physio:
            for stat in stats:
                data = self.load_stat_data(physio, stat)
                anonyme = data[f"{stat}_anonyme"]
                real = data[f"{stat}_real"]

                if anonyme is not None and real is not None:
                    statKS, pvalKS, statWMW_p, pvalWMW_p, statWMW_up, pvalWMW_up, dist_euclidean = self.perform_statistical_tests(anonyme, real)

                    output_data = pd.DataFrame({
                        'statKS': [statKS],
                        'pvalKS': [pvalKS],
                        'statWMW_p': [statWMW_p],
                        'pvalWMW_p': [pvalWMW_p],
                        'statWMW_up': [statWMW_up],
                        'pvalWMW_up': [pvalWMW_up],
                        f'dist_{stat}': [dist_euclidean],
                    })
                    output_file = f"tests_meth_{physio}_{stat}.csv"

                    self.save_to_csv(output_file, output_data)

# **************************
# Main Function
# **************************

def main():
    # Repertory of the data
    file = sys.argv[4]
    # Définir des valeurs par défaut
    dossier_data = sys.argv[1]
    dossier_anonyme = sys.argv[3]
    nb_patients = sys.argv[2]
    nb_samples = ""
    # Open the file and read the lines
    with open(file, 'r') as param_file:
        if os.path.exists(file):
            print(f"Le fichier {file} a été trouvé")
        else:
            raise Exception(f"Le fichier {file} n'a pas été trouvé")

        # Read the lines of the file
        lines = param_file.readlines()

    # Go through the lines and update the variables
    for line in lines:
        # Split the line into key and value
        new_line = line.split(':')
        key = new_line[0].strip()
        value = new_line[1].strip()

        # Update the variables
        if key == 'output_folder':
            output_folder = value + "_" + time.strftime("%Y_%m_%d")

        elif key == "nombre_samples":
            nb_samples = value
        else:
            raise Exception(f"Clé {key} non reconnue")

    # Create the output folder
    data_processor = DataProcessor(dossier_anonyme, dossier_data, nb_patients, nb_samples)
    analysis_generator = AnalysisGenerator(data_processor, output_folder)
    statistics_generator = StatisticsGenerator(data_processor, output_folder)

    # Generate the analysis
    analysis_generator.generate_dtw_analysis()
    analysis_generator.generate_physio_stats()

    # Perform statistical tests
    statistics_generator.generate_statistical_tests()

if __name__ == "__main__":
    main()
