// **************************
// main.cpp
// **************************

#include "data.h"
#include <iostream>
#include <string>
#include <cstdlib>  // Added the <cstdlib> library
using namespace std;

int main(int argc, char* argv[]) {
    // Check the number of command-line arguments
    if (argc != 6) {
        cerr << "Usage: " << argv[0] << " <dossier_d_entree> <nb_patiens> <borne_min> <borne_max> <dossier_de_sortie>" << std::endl;
        return 1;
    }

    // Extract command-line arguments
    string inputFolder = argv[1];
    int nbPatients = atoi(argv[2]);
    string outputFolder = argv[5];  // Fixing the index
    double minVal = atof(argv[3]);
    double maxVal = atof(argv[4]);

    // Use the constructor of DataProcessor with minVal and maxVal values
    DataProcessor processor(minVal, maxVal);
    processor.processFiles(inputFolder, outputFolder, minVal, maxVal, nbPatients);

    return 0;
}

