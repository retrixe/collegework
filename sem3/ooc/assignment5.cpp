#include <iostream>
#include <fstream>

using namespace std;

class income_exception : public exception {
	public:
	virtual const char* what() const noexcept override {
		return "Income is out of range (50000 to 100000)!";
	}
};

class age_exception : public exception {
	public:
	virtual const char* what() const noexcept override {
		return "Age is out of range (18 to 55)!";
	}
};

class city_exception : public exception {
	public:
	virtual const char* what() const noexcept override {
		return "City is not 'Pune' or 'Mumbai'!";
	}
};

class room_type_exception : public exception {
	public:
	virtual const char* what() const noexcept override {
		return "Room type is not 'Deluxe' or 'Super Deluxe'!";
	}
};

class Hotel {
	private:
	string cust_name;
	int cust_id;
	int age;
	int income;
	string city;
	string room_type;

	public:
	Hotel() {
		cust_name = "John Doe";
		cust_id = 0;
		income = 60000;
		age = 18;
		city = "Pune";
		room_type = "Deluxe";
	}

	void display() {
		cout << "Name: " << cust_name << "\n"
			<< "ID: " << cust_id << "\n"
			<< "Income: " << income << "\n"
			<< "Age: " << age << "\n"
			<< "City: " << city << "\n"
			<< "Room type: " << room_type << "\n";
	}

	string getcust_name() {
		return cust_name;
	}

	int getcust_id() {
		return cust_id;
	}

	int getage() {
		return age;
	}

	int getincome() {
		return income;
	}

	string getcity() {
		return city;
	}

	string getroom_type() {
		return room_type;
	}

	void accept() {
		cout << "Enter name: ";
		cin >> cust_name;
		cout << "Enter ID: ";
		cin >> cust_id;
		cout << "Enter income: ";
		cin >> income;
		if (income < 50000 || income > 100000) throw income_exception();
		cout << "Enter age: ";
		cin >> age;
		if (age < 18 || age > 55) throw age_exception();
		cout << "Enter city: ";
		cin >> city;
		if (city != "Pune" && city != "Mumbai") throw city_exception();
		cout << "Enter room type: ";
		cin.ignore();
		getline(cin, room_type);
		if (room_type != "Deluxe" && room_type != "Super Deluxe") throw room_type_exception();
	}
};

int main() {
	Hotel customers[5];
	ofstream hotel_txt;
	hotel_txt.open("hotel.txt");

	// Accept all customers
	int i = 0;
	while (i < 5) {
		cout << "----- Customer #" << i + 1 << " -----\n";
		try {
			customers[i].accept();
			hotel_txt << customers[i].getcust_name() << "\n";
			hotel_txt << customers[i].getcust_id() << "\n";
			hotel_txt << customers[i].getincome() << "\n";
			hotel_txt << customers[i].getage() << "\n";
			hotel_txt << customers[i].getcity() << "\n";
			hotel_txt << customers[i].getroom_type() << "\n";
			hotel_txt << endl;
			i++;
		} catch (exception& e) {
			cout << "Error: " << e.what() << "\n";
		}
	}
	hotel_txt.close();

	// Display all customers
	i = 0;
	for (auto customer : customers) {
		cout << "----- Customer #" << ++i << " -----\n";
		customer.display();
	}
	return 0;
}
