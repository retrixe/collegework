#include <iostream>

using namespace std;

class Student {
  private:
  string name;
  int rollNo;
  int classNo;
  int division;
  char dob[10];
  long aadhaarNo;
  char bloodGroup[2];
  long telephoneNo;
  string address;
  int subjectCount;
  int marks[10];

  public:
  static int count;

  void getData() {
    cin.ignore();
    cout << "Enter name: ";
    getline(cin, name);
    cout << "Enter roll no: ";
    cin >> rollNo;
    cout << "Enter class: ";
    cin >> classNo;
    cout << "Enter division: ";
    cin >> division;
    cout << "Enter date of birth: ";
    cin >> dob;
    cout << "Enter aadhaar no: ";
    cin >> aadhaarNo;
    cout << "Enter blood group: ";
    cin >> bloodGroup;
    cout << "Enter telephone no: ";
    cin >> telephoneNo;
    cin.ignore();
    cout << "Enter address: ";
    getline(cin, address);
    cout << "Enter total num of subjects: ";
    cin >> subjectCount;
    for (int i = 1; i <= subjectCount; i++) {
      cout << "Enter marks for subject " << i << " (out of 100): ";
      cin >> marks[i - 1];
    }
  }

  void putData() {
    cout << "Name: " << name << "\n";
    cout << "Roll no: " << rollNo << "\n";
    cout << "Class: " << classNo << "\n";
    cout << "Division: " << division << "\n";
    cout << "Date of birth: " << dob << "\n";
    cout << "Aadhaar no: " << aadhaarNo << "\n";
    cout << "Blood group: " << bloodGroup << "\n";
    cout << "Telephone no: " << telephoneNo << "\n";
    cout << "Address: " << address << "\n";
    for (int i = 1; i <= subjectCount; i++) {
      cout << "Marks for subject " << i << ": " << marks[i - 1] << "\n";
    }
  }

  static void displayData(Student &student) {
    student.putData();
  }

  friend void displayPercentage(Student &student);
};

int Student::count = 0;

void displayPercentage(Student &student) {
  int total = 0;
  for (int i = 0; i < student.subjectCount; i++) {
    total += student.marks[i];
  }
  cout << "Total marks percentage: " << (total / student.subjectCount) << "\n";
}

int main() {
  cout << "Enter number of students: ";
  cin >> Student::count;

  Student students[Student::count];
  for (int i = 0; i < Student::count; i++) {
    cout << "===== Enter student " << i + 1 << " details =====\n";
    students[i].getData();
  }

  cout << "---------------------- Student Information ----------------------\n";

  for (int i = 0; i < Student::count; i++) {
    cout << "===== Student " << i + 1 << " Details =====\n";
    Student::displayData(students[i]);
    displayPercentage(students[i]);
  }
  return 0;
}
