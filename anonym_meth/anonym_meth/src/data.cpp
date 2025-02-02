// **************************
// data.cpp
// **************************

#include "data.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <random>
#include <cstdlib>  // For atoi

using namespace std;

// **************************
// DataAnonymizer Class
// **************************

void DataAnonymizer::anonymizeData(TimeSeriesData& data) {
    // Anonymize time series data by applying perturbations
    uniform_real_distribution<> dis(minVal, maxVal);

    double perturbation = dis(gen);

    data.pas += data.pas * (perturbation / 100.0);
    data.pam += data.pam * (perturbation / 100.0);
    data.pad += data.pad * (perturbation / 100.0);

    if (data.fc < 60) {
        data.fc = 55;
    } else if (data.fc < 90) {
        data.fc = 80;
    } else {
        data.fc = 110;
    }
}

// **************************
// DataProcessor Class
// **************************

// Constructor with initialization list for DataProcessor
DataProcessor::DataProcessor(double minVal, double maxVal) : anonymizer(minVal, maxVal) {}

void DataProcessor::processFiles(const std::string& inputFolder, const std::string& outputFolder, double minVal, double maxVal, int nbPatients) {
    // Use initialization in the member initialization list to avoid assignment
    DataAnonymizer anonymizer(minVal, maxVal);

    for (int i = 1; i <= nbPatients; i++) {
        ifstream eventfile(inputFolder + "/" + std::to_string(i) + "_events.txt");
        ifstream timeSeriesFile(inputFolder + "/" + std::to_string(i) + "_series.txt");
        ofstream anonymecsv(outputFolder + "/" + std::to_string(i) + "_anonyme.csv");

        // Header for the anonymized CSV file
        anonymecsv << "Time" << "," << "FC" << "," << "PAS" << "," << "PAM" << "," << "PAD" << "," << "events" << std::endl;

        vector<EventData> eventsData;
        vector<TimeSeriesData> seriesData;
        string line;
        int lineCount = 0;
        string eventsValue = "NULL";

        // Read event data from file
        if (eventfile.is_open()) {
            while (getline(eventfile, line)) {
                lineCount++;
                if (lineCount >= 2) {
                    stringstream ss(line);
                    EventData data;
                    ss >> data.time;
                    char comma;
                    ss >> comma;
                    getline(ss, data.event);
                    eventsData.push_back(data);
                }
            }
            eventfile.close();
        } else {
            cout << "Unable to open events file" << std::endl;
        }

        // Read time series data from file, anonymize, and write to the anonymized CSV file
        if (timeSeriesFile.is_open()) {
            while (getline(timeSeriesFile, line)) {
                TimeSeriesData data;
                stringstream ss(line);
                char comma;

                ss >> data.time >> comma >> data.fc >> comma >> data.pas >> comma >> data.pam >> comma >> data.pad;
                if (data.time < 0) {
                    continue;
                }

                // Match events to time series data
                eventsValue = "NULL";
                if (!eventsData.empty()) {
                    for (const auto& event : eventsData) {
                        if (event.time == data.time) {
                            eventsValue = event.event;
                            break;
                        }
                    }
                }

                // Anonymize and write to CSV
                anonymizer.anonymizeData(data);

                anonymecsv << data.time << "," << data.fc << "," << data.pas << ","
                           << data.pam << "," << data.pad << "," << eventsValue << std::endl;
            }
            timeSeriesFile.close();
        } else {
            cout << "Unable to open time series file" << std::endl;
        }
    }
}

