#include <iostream>
#include <vector>

using namespace std;

template<typename T>
void bubble_sort(vector<T> &arr) {
	int n = arr.size();
	for (int i = 0; i < n - 1; i++) {
		for (int j = 0; j < n - i - 1; j++) {
			if (arr[j] > arr[j + 1]) {
				T temp = arr[j];
				arr[j] = arr[j + 1];
				arr[j + 1] = temp;
			}
		}
	}
}

int main() {
	int nInt;
	cout << "Enter number of integer elements: ";
	cin >> nInt;
	vector<int> arrInt(nInt);
	for (int i = 0; i < nInt; i++) {
		cout << "Enter integer element #" << i + 1 << ": ";
		cin >> arrInt[i];
	}
	bubble_sort(arrInt);
	cout << "===== Sorted Integer Array =====\n";
	for (int i = 0; i < nInt; i++) {
		cout << "Element #" << i + 1 << ": " << arrInt[i] << "\n";
	}

	int nFlt;
	cout << "Enter number of float elements: ";
	cin >> nFlt;
	vector<float> arrFlt(nFlt);
	for (int i = 0; i < nFlt; i++) {
		cout << "Enter float element #" << i + 1 << ": ";
		cin >> arrFlt[i];
	}
	bubble_sort(arrFlt);
	cout << "===== Sorted Float Array =====\n";
	for (int i = 0; i < nFlt; i++) {
		cout << "Element #" << i + 1 << ": " << arrFlt[i] << "\n";
	}
}

