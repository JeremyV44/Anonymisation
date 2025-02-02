#ifndef DATA_H
#define DATA_H

#include <string>
#include <vector>
#include <random>

// **************************
// EventData Class
// **************************

class EventData {
public:
    int time;
    std::string event;
};

// **************************
// TimeSeriesData Class
// **************************

class TimeSeriesData {
public:
    int time;
    double fc;
    double pas;
    double pam;
    double pad;
};

// **************************
// DataAnonymizer Class
// **************************

class DataAnonymizer {
public:
    // Constructor with initialization list for DataAnonymizer
    DataAnonymizer(double minVal, double maxVal) : gen(rd()), minVal(minVal), maxVal(maxVal) {}

    // Anonymize time series data
    void anonymizeData(TimeSeriesData& data);

private:
    std::random_device rd;
    std::default_random_engine gen;
    double minVal;
    double maxVal;
};

// **************************
// DataProcessor Class
// **************************

class DataProcessor {
public:
    // Constructor with initialization list for DataProcessor
    DataProcessor(double minVal, double maxVal);
    
    // Process input files and generate anonymized output
    void processFiles(const std::string& inputFolder, const std::string& outputFolder, double minVal, double maxVal, int nbPatients);

private:
    DataAnonymizer anonymizer;
};

#endif

