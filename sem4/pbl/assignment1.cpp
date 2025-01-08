#include <string>
#include <iostream>

using namespace std;

class User {
	private:
	long int mobileNo;
	string name;
	long int billAmount;

	public:
	User() {
		mobileNo = 0;
		name = "";
		billAmount = 0;
	}

	friend class Records;
};

#define MAX 100

class Records {
	private:
	int n;
	User users[MAX];

	public:
	Records(int n) {
		this->n = n;
	}

	void accept();

	void display();

	void heapSort();
	void adjust(int n, int i);
};

void Records::accept() {
	for (int i = 0; i < n; i++) {
		cout << "===== User #" << i + 1 << " =====" << endl;
		cout << "Enter mobile no: ";
		cin >> users[i].mobileNo;
		cout << "Enter name: ";
		cin >> users[i].name;
		cout << "Enter bill amount: ";
		cin >> users[i].billAmount;
	}
}

void Records::display() {
	for (int i = 0; i < n; i++) {
		cout << "===== User #" << i + 1 << " =====" << endl;
		cout << "Mobile no: " << users[i].mobileNo << endl;
		cout << "Name: " << users[i].name << endl;
		cout << "Bill amount: " << users[i].billAmount << endl;
	}
}

void Records::heapSort() {
	int n = this->n;
	for (int i = (n / 2) - 1; i >= 0; i--) {
		adjust(n - 1, i);
	}
	while (n > 0) {
		User t = users[0];
		users[0] = users[n - 1];
		users[n - 1] = t;
		n--;
		adjust(n - 1, 0);
	}
}

void Records::adjust(int n, int i) {
	while (2 * i + 1 <= n) {
		int j = 2 * i + 1;

		if (j + 1 <= n && users[j + 1].mobileNo > users[j].mobileNo) {
			j = j + 1;
		}

		if (users[i].mobileNo >= users[j].mobileNo) break;
		else {
			User temp = users[i];
			users[i] = users[j];
			users[j] = temp;
			i = j;
		}
	}
}

int main() {
	int n;
	cout << "Enter number of users to accept: " << endl;
	cin >> n;

	Records records(n);
	records.accept();

	while (1) {
		int option;
		cout << "===== Options =====" << endl;
		cout << "1. Display" << endl;
		cout << "2. Heap sort" << endl;
		cout << "0. Exit" << endl;
		cout << "Enter option: ";
		cin >> option;
		if (option == 0) return 0;
		else if (option == 1) {
			records.display();
		} else if (option == 2) {
			records.heapSort();
			cout << "Heap sorted by mobile number!" << endl;
		} else {
			cout << "Invalid option selected!" << endl;
		}
	}

	return 0;
}
