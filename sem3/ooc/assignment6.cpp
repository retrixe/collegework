#include <iostream>
#include <fstream>
#include <cctype>
using namespace std;

class FileHandler {
	private:
	fstream file;
	string fileName;

	public:
	FileHandler(string name) : fileName(name) {}

	void writeToFile() {
		file.open(fileName, ios::out);
		if (!file) {
			cout << "Error opening file for writing!" << endl;
			return;
		}
		string content;
		cout << "Enter text to write to the file (" << fileName << "):" << endl;
		getline(cin, content);
		file << content;
		file.close();
	}

	void displayFile() {
		file.open(fileName, ios::in);
		if (!file) {
			cout << "Error opening file for reading!" << endl;
			return;
		}
		cout << "Contents of the file (" << fileName << "):" << endl;
		string line;
		while (getline(file, line)) {
			cout << line << endl;
		}
		file.close();
	}

	int countUppercase() {
		file.open(fileName, ios::in);
		if (!file) {
			cout << "Error opening file for reading!" << endl;
			return 0;
		}
		char ch;
		int count = 0;
		while (file.get(ch)) {
			if (isupper(ch)) count++;
		}
		file.close();
		return count;
	}

	int countLetters() {
		file.open(fileName, ios::in);
		if (!file) {
			cout << "Error opening file for reading!" << endl;
			return 0;
		}
		char ch;
		int count = 0;
		while (file.get(ch)) {
			if (isalpha(ch)) count++;
		}
		file.close();
		return count;
	}

	int countSpaces() {
		file.open(fileName, ios::in);
		if (!file) {
			cout << "Error opening file for reading!" << endl;
			return 0;
		}
		char ch;
		int count = 0;
		while (file.get(ch)) {
			if (isspace(ch)) count++;
		}
		file.close();
		return count;
	}

	int countVowels() {
		file.open(fileName, ios::in);
		if (!file) {
			cout << "Error opening file for reading!" << endl;
			return 0;
		}
		char ch;
		int count = 0;
		while (file.get(ch)) {
			ch = tolower(ch);
			if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
				count++;
			}
		}
		file.close();
		return count;
	}
};

int main() {
	FileHandler fileHandler("BOOK.txt");
	while (true) {
		cout << "----- Options -----\n"
			<< "1. Write line to file\n"
			<< "2. Display contents of file\n"
			<< "3. Display analysis of file (uppercase letters, letters, spaces, vowels)\n"
			<< "0. Exit\n"
			<< "Enter choice: ";
		int choice;
		cin >> choice; cin.ignore();
		switch (choice) {
			case 1: fileHandler.writeToFile(); break;
			case 2: fileHandler.displayFile(); break;
			case 3:
			cout << "Uppercase letters: " << fileHandler.countUppercase() << "\n";
			cout << "Letters: " << fileHandler.countLetters() << "\n";
			cout << "Spaces: " << fileHandler.countSpaces() << "\n";
			cout << "Vowels: " << fileHandler.countVowels() << "\n";
			break;
			case 0: return 0;
		}
	}
	return 0;
}
