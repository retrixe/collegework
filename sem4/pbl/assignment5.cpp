#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#include <bits/ostream.tcc>

using namespace std;

#define MAX 10

class Student {
public:
    int roll_no;
    string name;
    int marks;

    Student(int roll_no, string name, int marks) {
        this->roll_no = roll_no;
        this->name = std::move(name);
        this->marks = marks;
    }

    Student(const Student& other) {
        this->roll_no = other.roll_no;
        this->name = other.name;
        this->marks = other.marks;
    }

    [[nodiscard]] string to_string() const {
        stringstream ss;
        ss << this->roll_no << "," << this->name << "," << this->marks;
        return ss.str();
    }

    static Student from_string(const string& str) {
        string to_parse = str;
        int roll_no = stoi(to_parse.substr(0, to_parse.find(',')));
        to_parse.erase(0, to_parse.find(',') + 1);
        string name = to_parse.substr(0, to_parse.find(','));
        to_parse.erase(0, to_parse.find(',') + 1);
        int marks = stoi(to_parse.substr(0, to_parse.find(',')));
        return {roll_no, name, marks};
    }
};

class StudentHashTable {
    vector<Student*> students;

public:
    StudentHashTable() {
        this->students.resize(MAX);
    }

    ~StudentHashTable() {
        for (auto student : this->students) {
            delete student;
        }
    }

    int add(const Student& student, bool hash_replace) {
        auto* new_student = new Student(student);
        int hash_value = hash(new_student->roll_no);
        if (this->students[hash_value] == nullptr) {
            this->students[hash_value] = new_student;
            return hash_value;
        }
        auto temp = new_student;
        if (hash_replace && hash(this->students[hash_value]->roll_no) != hash_value) {
            temp = this->students[hash_value];
            this->students[hash_value] = new_student;
        }
        for (int i = (hash_value + 1) % MAX; i != hash_value; i = (i + 1) % MAX) {
            if (this->students[i] == nullptr) {
                this->students[i] = temp;
                return i;
            }
        }
        return -1;
    }

    bool remove(int roll_no) {
        int student = find_student(roll_no);
        bool exists = student != -1;
        if (exists) {
            delete this->students[student];
            this->students[student] = nullptr;
            save_to_file();
        }
        return exists;
    }

    [[nodiscard]] int find_student(int roll_no) const {
        int hash_value = hash(roll_no);
        if (this->students[hash_value] != nullptr && this->students[hash_value]->roll_no == roll_no) {
            return hash_value;
        }
        for (int i = (hash_value + 1) % MAX; i != hash_value; i = (i + 1) % MAX) {
            if (this->students[i] != nullptr && this->students[i]->roll_no == roll_no) {
                return i;
            }
        }
        return -1;
    }

    [[nodiscard]] Student* get_student(int roll_no) const {
        int position = find_student(roll_no);
        if (position == -1) {
            throw out_of_range("student does not exist");
        }
        return this->students[position];
    }

    [[nodiscard]] string to_string() const {
        stringstream ss;
        for (auto* student : this->students) {
            if (student != nullptr) {
                ss << student->to_string();
            }
            ss << endl;
        }
        return ss.str();
    }

    void save_to_file() const {
        ofstream database_file("database.txt");
        database_file << to_string();
        database_file.close();
    }

    void load_from_string(const string& str) {
        string to_parse = str;
        while (!to_parse.empty()) {
            auto index = to_parse.find('\n');
            if (index == string::npos) {
                index = to_parse.length();
            }
            string student = to_parse.substr(0, index);
            to_parse.erase(0, to_parse.find('\n') + 1);
            if (!student.empty()) {
                add(Student::from_string(student), true);
            }
        }
    }

    void load_from_file() {
        ifstream database_file("database.txt");
        if (database_file.fail())
            return;
        stringstream contents;
        contents << database_file.rdbuf();
        database_file.close();
        load_from_string(contents.str());
    }

    [[nodiscard]] vector<Student> get_all_students() const {
        vector<Student> students;
        for (auto* student : this->students) {
            if (student != nullptr) {
                students.push_back(*student);
            }
        }
        return students;
    }

    static int hash(int roll_no) {
        return roll_no % MAX;
    }
};

int main() {
    StudentHashTable table;
    table.load_from_file();
    while (true) {
        cout << "==========\n"
                "1. Display all students\n"
                "2. Add student\n"
                "3. Find student\n"
                "4. Remove student\n"
                "5. Change student marks\n"
                "0. Quit\n"
                "Enter choice: ";
        int choice;
        cin >> choice;
        if (choice == 0) break;

        int roll_no = 0;
        string name;

        switch (choice) {
            case 1:
                for (const auto& student : table.get_all_students()) {
                    cout << student.to_string() << endl;
                }
            break;
            case 2:
                cout << "Enter roll no: ";
                cin >> roll_no;
                cout << "Enter name: ";
                cin >> name;
                table.add(Student(roll_no, name, -1), true);
                table.save_to_file();
            break;
            case 3:
                cout << "Enter roll no: ";
                cin >> roll_no;
                try {
                    const auto student = table.get_student(roll_no);
                    cout << student->to_string() << endl;
                } catch (out_of_range& e) {
                    cout << e.what() << endl;
                }
            break;
            case 4:
                cout << "Enter roll no: ";
                cin >> roll_no;
                if (table.remove(roll_no)) {
                    cout << "Removed successfully!" << endl;
                } else {
                    cout << "No record formed." << endl;
                }
            break;
            case 5:
                cout << "Enter roll no: ";
                cin >> roll_no;
                try {
                    auto student = table.get_student(roll_no);
                    cout << "Enter student marks: ";
                    cin >> student->marks;
                    table.save_to_file();
                } catch (out_of_range& e) {
                    cout << e.what() << endl;
                }
            break;
            default:
                cout << "Invalid choice!\n";
        }
    }
    return 0;
}
