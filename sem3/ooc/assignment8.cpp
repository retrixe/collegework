#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

class item {
	private:
	int item_code;
	string item_name;
	int item_quantity;
	int item_price;

	public:
	item() {
		item_code = -1;
		item_name = "N/A";
		item_quantity = -1;
		item_price = -1;
	}

	void accept() {
		cout << "Enter item code: ";
		cin >> item_code;
		cout << "Enter item name: ";
		cin >> item_name;
		cout << "Enter item quantity: ";
		cin >> item_quantity;
		cout << "Enter item price: ";
		cin >> item_price;
	}

	void display() {
		cout << "Item code: " << item_code << "\n";
		cout << "Item name: " << item_name << "\n";
		cout << "Item quantity: " << item_quantity << "\n";
		cout << "Item price: " << item_price << "\n";
	}

	int get_item_code() { return item_code; }

	string get_item_name() { return item_name; }

	int get_item_quantity() { return item_quantity; }

	int get_item_price() { return item_price; }

	void set_item_code(int code) { item_code = code; }

	void set_item_name(string name) { item_name = name; }

	void set_item_quantity(int quantity) { item_quantity = quantity; }

	void set_item_price(int price) { item_price = price; }
};

void bubble_sort(vector<item> &arr) {
	int n = arr.size();
	for (int i = 0; i < n - 1; i++) {
		for (int j = 0; j < n - i - 1; j++) {
			if (
				arr[j].get_item_code() > arr[j + 1].get_item_code() ||
				arr[j].get_item_name().compare(arr[j + 1].get_item_name()) < 0
			) {
				item temp = arr[j];
				arr[j] = arr[j + 1];
				arr[j + 1] = temp;
			}
		}
	}
}

int main() {
	vector<item> items;
	while (1) {
		cout << "====================\n"
			<< "1. Search for item\n"
			<< "2. Display all items\n"
			<< "3. Insert item\n"
			<< "4. Delete item\n"
			<< "5. Sort items\n"
			<< "6. Purchase\n"
			<< "0. Exit\n"
			<< "Enter choice: ";
		int choice;
		cin >> choice;
		cout << "====================\n";
		switch (choice) {
			case 0:
				return 0;
			case 1: {
				cout << "Enter item name or code: ";
				string input;
				cin >> input;
				auto item_ptr = find_if(items.begin(), items.end(), [input](item it) {
					return to_string(it.get_item_code()) == input
						|| it.get_item_name() == input;
				});
				if (item_ptr == items.end()) {
					cout << "Error: Item not found!\n";
					break;
				}
				item_ptr->display();
				break;
			}
			case 2: {
				cout << "============================================================\n"
					<< "Code\tName\tQuantity\tPrice\n"
					<< "============================================================\n";
				for (int i = 0; i < items.size(); i++) {
					cout << items[i].get_item_code() << "\t"
						<< items[i].get_item_name() << "\t"
						<< items[i].get_item_quantity() << "\t"
						<< items[i].get_item_price() << "\n";
				}
				break;
			}
			case 3: {
				item it;
				it.accept();
				items.push_back(it);
				break;
			}
			case 4: {
				cout << "Enter item name or code: ";
				string input;
				cin >> input;
				auto item_ptr = find_if(items.begin(), items.end(), [input](item it) {
					return to_string(it.get_item_code()) == input
						|| it.get_item_name() == input;
				});
				if (item_ptr == items.end()) {
					cout << "Error: Item not found!\n";
					break;
				}
				items.erase(item_ptr);
				cout << "Deleted successfully!\n";
				break;
			}
			case 5: {
				bubble_sort(items);
				cout << "Sorted on item code successfully!\n";
				break;
			}
			case 6: {
				cout << "Enter item name or code: ";
				string input;
				cin >> input;
				auto item_ptr = find_if(items.begin(), items.end(), [input](item it) {
					return to_string(it.get_item_code()) == input
						|| it.get_item_name() == input;
				});
				if (item_ptr == items.end()) {
					cout << "Error: Item not found!\n";
					break;
				}
				item_ptr->display();
				cout << "Enter quantity of items to buy: ";
				int qty;
				cin >> qty;
				if (qty > item_ptr->get_item_quantity()) {
					cout << "Error: Insufficient quantity!\n";
					break;
				}
				item_ptr->set_item_quantity(item_ptr->get_item_quantity() - qty);
				cout << "Purchased successfully!\n";
				break;
			}
			default:
				cout << "Error: Invalid choice!\n";
		}
	}
}

