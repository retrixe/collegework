#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>
#include <cstdlib>
#include <cstring>
using namespace std;

uint64_t timeSinceEpochMillisec() {
  return chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now().time_since_epoch()).count();
}

char randomChar() {
    return rand();
}

class Benchmark {
public:
    virtual double run() = 0; 
    virtual void display() = 0;
};

class CPUStPerformance : public Benchmark {
private:
    size_t file_size = 1024 * 1024 * 100;
    size_t block_size = 1024 * 1024 * 4;
    string filename = "file1.txt";

public:
    double run() override {
        char* buffer = new char[file_size];
        for (size_t i = 0; i < file_size; ++i) {
            buffer[i] = randomChar(); 
        }
        ofstream file(filename);
        for (size_t i = 0; i < file_size; i += block_size) {
            file.write(buffer + (i * sizeof(char)), block_size);
        }
        file.close();
        delete[] buffer;

        int retCode;
        uint64_t start = timeSinceEpochMillisec();
        retCode = system("clang++ -o temp.out miniproject.cpp");
        if (retCode != 0) return -1;
        retCode = system("g++ -o temp.out miniproject.cpp");
        if (retCode != 0) return -1;
        retCode = system("rm temp.out");
        if (retCode != 0) return -1;
        retCode = system(("zstd -3 -k --force -T1 " + filename).c_str());
        if (retCode != 0) return -1;
        retCode = system(("zstd -5 -k --force -T1 " + filename).c_str());
        if (retCode != 0) return -1;
        retCode = system(("xz -k -T1 " + filename).c_str());
        if (retCode != 0) return -1;
        retCode = system(("rm " + filename + ".xz").c_str());
        if (retCode != 0) return -1;
        retCode = system(("rm " + filename + ".zst").c_str());
        if (retCode != 0) return -1;
        retCode = system(("rm " + filename).c_str());
        if (retCode != 0) return -1;
        uint64_t end = timeSinceEpochMillisec();
        return (10000.0 / double(end - start)) * 1000.0;
    }

    void display() override {
        double result = run();
        if (result == -1) {
            cout << "An error occurred during benchmark execution!\n";
            return;
        }
        cout << "Benchmark Score: " << result << "\n";
    }
};

class CPUMtPerformance : public Benchmark {
private:
    size_t file_size = 1024 * 1024 * 100;
    size_t block_size = 1024 * 1024 * 4;
    string filename = "file1.txt";

public:
    double run() override {
        char* buffer = new char[file_size];
        for (size_t i = 0; i < file_size; ++i) {
            buffer[i] = randomChar(); 
        }
        ofstream file(filename);
        for (size_t i = 0; i < file_size; i += block_size) {
            file.write(buffer + (i * sizeof(char)), block_size);
        }
        file.close();
        delete[] buffer;

        int retCode;
        uint64_t start = timeSinceEpochMillisec();
        retCode = system("clang++ -o temp.out miniproject.cpp");
        if (retCode != 0) return -1;
        retCode = system("g++ -o temp.out miniproject.cpp");
        if (retCode != 0) return -1;
        retCode = system("rm temp.out");
        if (retCode != 0) return -1;
        retCode = system(("zstd -3 -k --force " + filename).c_str());
        if (retCode != 0) return -1;
        retCode = system(("zstd -5 -k --force " + filename).c_str());
        if (retCode != 0) return -1;
        retCode = system(("xz -k " + filename).c_str());
        if (retCode != 0) return -1;
        retCode = system(("rm " + filename + ".xz").c_str());
        if (retCode != 0) return -1;
        retCode = system(("rm " + filename + ".zst").c_str());
        if (retCode != 0) return -1;
        retCode = system(("rm " + filename).c_str());
        if (retCode != 0) return -1;
        uint64_t end = timeSinceEpochMillisec();
        return (10000.0 / double(end - start)) * 1000.0;
    }

    void display() override {
        double result = run();
        if (result == -1) {
            cout << "An error occurred during benchmark execution!\n";
            return;
        }
        cout << "Benchmark Score: " << result << "\n";
    }
};

class SSDPerformance : public Benchmark {
private:
    size_t file_size = 1024 * 1024 * 100;
    size_t block_size = 1024 * 1024 * 4;
    string filename = "file1.txt";
    char* buffer;

    double writeSpeed() {
        buffer = new char[file_size];
        for (size_t i = 0; i < file_size; ++i) {
            buffer[i] = randomChar(); 
        }

        uint64_t start = timeSinceEpochMillisec();
        ofstream file(filename);
        for (size_t i = 0; i < file_size; i += block_size) {
            file.write(buffer + (i * sizeof(char)), block_size);
        }
        file.close();
        uint64_t end = timeSinceEpochMillisec();

        delete[] buffer;
        double total_time = double(end - start) / 1000;
        return file_size / (1024 * 1024) / total_time;
    }

    double readSpeed() {
        buffer = new char[file_size];
        uint64_t start = timeSinceEpochMillisec();
        ifstream file(filename); 
        for (size_t i = 0; i < file_size; i += block_size) {
            file.read(buffer + (i * sizeof(char)), block_size);
        }
        file.close();
        uint64_t end = timeSinceEpochMillisec();
        delete[] buffer;
        double total_time = double(end - start) / 1000;
        return file_size / (1024 * 1024) / total_time;
    }

public:
    SSDPerformance() {
        srand(static_cast<unsigned int>(time(nullptr))); 
    }

    double run() override {
        double writeSpeed1 = writeSpeed();
        double readSpeed1 = readSpeed();
        system(("rm " + filename).c_str());
        double avgspeed = (writeSpeed1 + readSpeed1) / 2;
        cout << "Write Speed: " << writeSpeed1 << " MB/s\n";
        cout << "Read Speed: " << readSpeed1 << " MB/s\n";
        cout << "Average Speed: " << avgspeed << " MB/s\n";  
        return avgspeed; 
    }

    void display() override {
        run(); 
    }
};

class RAMPerformance : public Benchmark {
private:
    size_t memory_size = 1024 * 1024 * 100;
    size_t block_size = 1024 * 1024; 
    char* buf1;
    char* buf2;

    double speed() {
        buf1 = new char[memory_size];
        buf2 = new char[memory_size];
        for (size_t i = 0; i < memory_size; ++i) {
            buf1[i] = randomChar(); 
        }
        uint64_t start = timeSinceEpochMillisec();
        for (size_t i = 0; i < memory_size; i += block_size) {
            memcpy(buf2 + (sizeof(char) * i), buf1 + (sizeof(char) * i), block_size);
        }
        uint64_t end = timeSinceEpochMillisec();
        double total_time = double(end - start) / 1000;
        return memory_size / (1024 * 1024) / total_time;
    }

public:
    RAMPerformance() {
        srand(static_cast<unsigned int>(time(nullptr))); 
    }

    double run() override {
        double avgspeed = speed();
        cout << "Average RAM Speed: " << avgspeed << " MB/s\n";  
        return avgspeed; 
    }

    void display() override {
        run(); 
    }
};

int main() {
    cout << "====== Benchmark Suite ======\n";
    CPUStPerformance cpuStPerformance;
    CPUMtPerformance cpuMtPerformance;
    SSDPerformance ssdPerformance;
    RAMPerformance ramPerformance;

    while (true) {
        cout << "Choose a benchmark you want to check:\n";
        cout << "1. Single-threaded CPU Performance\n";
        cout << "2. Multi-threaded CPU Performance\n";
        cout << "3. SSD Performance\n";
        cout << "4. RAM Performance\n";
        cout << "5. Exit\n";
        cout << "Enter your choice (1-5): ";

        int choice;
        cin >> choice;
        switch (choice) {
            case 1:
                cpuStPerformance.display();
                break;
            case 2:
                cpuMtPerformance.display();
                break;
            case 3:
                ssdPerformance.display();
                break;
            case 4:
                ramPerformance.display();
                break;
            case 5:
                cout << "Exiting program.\n";
                return 0;
            default:
                cout << "INVALID CHOICE!\n";
                cout << "Please re-enter your choice.\n";
                break;
        }
    }
    return 0;
}

