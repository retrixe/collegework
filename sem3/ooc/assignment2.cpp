#include <iostream>
#include <cstring>

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

  Student() {
    count++;
    cout << "Default constructor invoked, total students: " << count << "\n";
  }

  Student(
    string name1,
    int rollNo1,
    int classNo1,
    int division1,
    const char* dob1,
    long aadhaarNo1,
    const char* bloodGroup1,
    long telephoneNo1,
    string address1,
    int subjectCount1,
    int marks1[10]
  ) {
    count++;
    cout << "Parameterised constructor invoked, total students: " << count << "\n";
    name = name1;
    rollNo = rollNo1;
    classNo = classNo1;
    division = division1;
    strcpy(dob, dob1);
    aadhaarNo = aadhaarNo1;
    strcpy(bloodGroup, bloodGroup1);
    telephoneNo = telephoneNo1;
    address = address1;
    subjectCount = subjectCount1;
    memcpy(marks, marks1, 10);
  }

  Student(Student &s) {
    count++;
    cout << "Copy constructor invoked, total students: " << count << "\n";
    name = s.name;
    rollNo = s.rollNo;
    classNo = s.classNo;
    division = s.division;
    strcpy(dob, s.dob);
    aadhaarNo = s.aadhaarNo;
    strcpy(bloodGroup, s.bloodGroup);
    telephoneNo = s.telephoneNo;
    address = s.address;
    subjectCount = s.subjectCount;
    memcpy(marks, s.marks, 10);
  }

  ~Student() {
    count--;
    cout << "Destructor invoked, total students: " << count << "\n";
  }

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
  int studentCount;
  cout << "Enter number of students: ";
  cin >> studentCount;

  // Default constructors invoked
  Student students[studentCount];
  for (int i = 0; i < studentCount; i++) {
    cout << "===== Enter student " << i + 1 << " details =====\n";
    students[i].getData();
  }

  cout << "---------------------- Student Information ----------------------\n";
  for (int i = 0; i < Student::count; i++) {
    cout << "===== Student " << i + 1 << " Details =====\n";
    Student::displayData(students[i]);
    displayPercentage(students[i]);
  }

  // Parameterised constructor invoked
  Student student1(
    "Test",
    4,
    12,
    4,
    "02/02/2004",
    123412341234,
    "O-",
    1234567890,
    "14B Street",
    2,
    new int[10]{70, 90}
  );
  cout << "===== Parameterised Student Details =====\n";
  Student::displayData(student1);
  displayPercentage(student1);

  // Copy constructor invoked
  Student student2(student1);
  cout << "===== Copied Student Details =====\n";
  Student::displayData(student2);
  displayPercentage(student2);

  // Destructors invoked
  return 0;
}
