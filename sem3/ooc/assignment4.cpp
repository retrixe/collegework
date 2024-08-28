#include <iostream>

using namespace std;

class Complex {
	private:
	int real;
	int imaginary;

	public:
	Complex(int real, int imaginary) : real(real), imaginary(imaginary) {}

	Complex() {}

	void setComplex() {
		cout << "Enter real part of complex number: ";
		cin >> real;
		cout << "Enter imaginary part of complex number: ";
		cin >> imaginary;
	}

	void printComplex() {
		cout << real << " + " << imaginary << "i\n";
	}

	Complex operator+(Complex other) {
		Complex temp(real + other.real, imaginary + other.imaginary);
		return temp;
	}

	Complex operator*(Complex other) {
		Complex temp(
			(real * other.real) - (imaginary * other.imaginary),
			(real * other.imaginary) + (imaginary * other.real)
		);
		return temp;
	}

	friend Complex operator-(Complex c1, Complex c2);

	friend Complex operator/(Complex c1, Complex c2);
};

Complex operator-(Complex c1, Complex c2) {
	Complex temp(c1.real - c2.real, c1.imaginary - c2.imaginary);
	return temp;
}

Complex operator/(Complex c1, Complex c2) {
	int real = (c1.real * c2.real) + (c1.imaginary * c2.imaginary);
	real /= (c2.real * c2.real) + (c2.imaginary * c2.imaginary);
	int imaginary = (c1.imaginary * c2.real) - (c1.real * c2.imaginary);
	imaginary /= (c2.real * c2.real) + (c2.imaginary * c2.imaginary);
	Complex temp(real, imaginary);
	return temp;
}

int main() {
	while (1) {
		int choice;
		cout << "===== Choices =====\n"
			<< "1. Addition\n"
			<< "2. Subtraction\n"
			<< "3. Multiplication\n"
			<< "4. Division\n"
			<< "0. Exit\n"
			<< "Select choice: ";
		cin >> choice;
		if (choice == 0) return 0;
		else if (choice > 4 || choice < 0) {
			cout << "Invalid option!\n";
			continue;
		}
		Complex c1, c2;
		cout << "===== Complex Number #1 =====\n";
		c1.setComplex();
		cout << "===== Complex Number #2 =====\n";
		c2.setComplex();
		cout << "===== Result =====\n";
		switch (choice) {
			case 1:
			(c1 + c2).printComplex();
			break;
			case 2:
			(c1 - c2).printComplex();
			break;
			case 3:
			(c1 * c2).printComplex();
			break;
			case 4:
			(c1 / c2).printComplex();
			break;
		}
	}
}
