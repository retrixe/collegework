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

	void display() {
		cout << "Mobile no: " << mobileNo << endl;
		cout << "Name: " << name << endl;
		cout << "Bill amount: " << billAmount << endl;
	}
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

	void quickSort(int low, int high);
	int partition(int low, int high);

	void linearSearch(long int mobileNo) {
		for (int i = 0; i < n; i++) {
			if (users[i].mobileNo == mobileNo) {
				users[i].display();
				return;
			}
		}
		cout << "No user with this mobile no found!" << endl;
	}

	void binarySearchNonRecursive(long int mobileNo, int low, int high) {
		while (low <= high) {
			int mid = (low + high) / 2;
			if (users[mid].mobileNo == mobileNo) {
				users[mid].display();
				return;
			} else if (mobileNo > users[mid].mobileNo) {
				high = mid - 1;
			} else {
				low = mid + 1;
			}
		}
		cout << "No user with this mobile no found!" << endl;
	}

	void binarySearchRecursive(long int mobileNo, int low, int high) {
		if (low <= high) {
			int mid = (low + high) / 2;
			if (users[mid].mobileNo == mobileNo) {
				users[mid].display();
			} else if (mobileNo > users[mid].mobileNo) {
				binarySearchRecursive(mobileNo, low, mid - 1);
			} else {
				binarySearchRecursive(mobileNo, mid + 1, high);
			}
			return;
		}
		cout << "No result found!" << endl;
	}

	void binarySearchRecursive(long int mobileNo) {
		binarySearchRecursive(mobileNo, 0, n);
	}
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
		users[i].display();
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

		if (j + 1 <= n && users[j + 1].billAmount > users[j].billAmount) {
			j = j + 1;
		}

		if (users[i].billAmount >= users[j].billAmount) {
			break;
		} else {
			User temp = users[i];
			users[i] = users[j];
			users[j] = temp;
			i = j;
		}
	}
}

void Records::quickSort(int low, int high) {
	if (low < high) {
		int pivot = partition(low, high);
		quickSort(low, pivot - 1);
		quickSort(pivot + 1, high);
	}
}

int Records::partition(int low, int high) {
	auto x = users[high];
	int i = low - 1;
	for (int j = low; j < high; j++) {
		if (users[j].mobileNo >= x.mobileNo) {
			i++;
			swap(users[i], users[j]);
		}
	}
	swap(users[i + 1], users[high]);
	return i + 1;
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
		cout << "2. Heap sort by bill amount" << endl;
		cout << "3. Quick sort by mobile number" << endl;
		cout << "4. Linear search by mobile number" << endl;
		cout << "5. Recursive binary search by mobile number" << endl;
		cout << "6. Non-recursive binary search by mobile number" << endl;
		cout << "0. Exit" << endl;
		cout << "Enter option: ";
		cin >> option;
		if (option == 0) return 0;
		else if (option == 1) {
			records.display();
		} else if (option == 2) {
			records.heapSort();
			cout << "Heap sorted by bill amount!" << endl;
		} else if (option == 3) {
			records.quickSort(0, n - 1);
			cout << "Quick sorted by mobile number!" << endl;
		} else if (option >= 4 && option <= 6) {
			records.quickSort(0, n - 1);
			cout << "Enter mobile number: ";
			long int mobileNo;
			cin >> mobileNo;
			cout << "Result:" << endl;
			if (option == 4) records.linearSearch(mobileNo);
			else if (option == 5) records.binarySearchRecursive(mobileNo);
			else records.binarySearchNonRecursive(mobileNo, 0, n);
		} else {
			cout << "Invalid option selected!" << endl;
		}
	}

	return 0;
}
