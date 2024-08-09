#include <iostream>

using namespace std;

class Employee {
	protected:
	string Ename;
	int EmpID;

	public:
	Employee() {
		EmpID = -1;
		Ename = "";
	}

	Employee(string name, int id) {
		EmpID = id;
		Ename = name;
	}

	virtual void accept() {
		cout << "Enter employee name: ";
		cin >> Ename;
		cout << "Enter employee ID: ";
		cin >> EmpID;
	}

	virtual void display() {
		cout << "Employee name: " << Ename << "\n";
		cout << "Employee ID: " << EmpID << "\n";
	}

	virtual void earnings() = 0;
};

class SalariedEmployee : private Employee {
	private:
	double weeklysalary;

	public:
	SalariedEmployee() {
		weeklysalary = -1;
	}

	SalariedEmployee(string name, int id, double salary) {
		Ename = name;
		EmpID = id;
		weeklysalary = salary;
	}

	void accept() {
		Employee::accept();
		cout << "Enter weekly salary: ";
		cin >> weeklysalary;
	}

	void display() {
		Employee::display();
		earnings();
	}

	void earnings() {
		cout << "Weekly salary: " << weeklysalary << "\n";
	}
};

class CommissionEmployee : private Employee {
	private:
	double grossSales;
	double commissionRate;
	double commissionSalary;

	public:
	CommissionEmployee() {
		commissionSalary = -1;
		commissionRate = -1;
		grossSales = -1;
	}

	CommissionEmployee(string name, int id, double rate, double sales) {
		Ename = name;
		EmpID = id;
		commissionSalary = rate * sales;
		commissionRate = rate;
		grossSales = sales;
	}

	void accept() {
		Employee::accept();
		cout << "Enter commission rate: ";
		cin >> commissionRate;
		cout << "Enter gross sales: ";
		cin >> grossSales;
	}

	void display() {
		Employee::display();
		cout << "Commission rate: " << commissionRate << "\n";
		cout << "Gross sales: " << grossSales << "\n";
		earnings();
	}

	void earnings() {
		commissionSalary = commissionRate * grossSales;
		cout << "Commission salary: " << commissionSalary << "\n";
	}
};

class HourlyEmployee : private Employee {
	private:
	double wage;
	double hours;
	double hourlySalary;

	public:
	HourlyEmployee() {
		wage = -1;
		hours = -1;
		hourlySalary = -1;
	}

	HourlyEmployee(string name, int id, double w, double h) {
		Ename = name;
		EmpID = id;
		wage = w;
		hours = h;
		hourlySalary = w * h;
	}

	void accept() {
		Employee::accept();
		cout << "Enter wage: ";
		cin >> wage;
		cout << "Enter hours: ";
		cin >> hours;		
	}

	void display() {
		Employee::display();
		cout << "Wage: " << wage << "\n";
		cout << "Hours: " << hours << "\n";
		earnings();
	}

	void earnings() {
		if (hours < 40) {
			hourlySalary = hours * wage;
		} else {
			hourlySalary = (wage * 40) + ((hours - 40) * wage) * 1.5;
		}
		cout << "Hourly salary: " << hourlySalary << "\n";
	}
};

int main() {
	SalariedEmployee salaried1("A", 1, 100);
	salaried1.display();
	cout << "\n";
	CommissionEmployee comm1("B", 2, 100, 10);
	comm1.display();
	cout << "\n";
	HourlyEmployee hourly1("C", 3, 40, 10);
	hourly1.display();
	cout << "\n";

	SalariedEmployee salaried2;
	salaried2.accept();
	salaried2.display();
	cout << "\n";
	CommissionEmployee comm2;
	comm2.accept();
	comm2.display();
	cout << "\n";
	HourlyEmployee hourly2;
	hourly2.accept();
	hourly2.display();

	return 0;
}
