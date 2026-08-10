#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool isPrime(int n) {
    if(n < 2)
        return false;
    for(int i = 2; i*i <= n; i++)
        if(n % i == 0)
            return false;
    return true;
}

int gcd(int a, int b) {
    while(b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int modInverse(int e, int phi) {
    int a = e, b = phi;
    int x0 = 1, x1 = 0;
    while(b != 0) {
        int q = a / b;
        int t = a - q*b;
        a = b;
        b = t;
        t = x0 - q*x1;
        x0 = x1;
        x1 = t;
    }
    if(x0 < 0)
        x0 += phi;
    return x0;
}

int modPow(int base, int exp, int mod) {
    int result = 1;
    base = base % mod;
    while(exp > 0) {
        if(exp % 2 == 1)
            result = result * base % mod;
        base = base * base % mod;
        exp = exp / 2;
    }
    return result;
}

int main() {
    int p, q;

    cout << "Enter prime number p: ";
    cin >> p;
    if(!isPrime(p)) {
        cout << "p is not a prime number" << endl;
        return 0;
    }

    cout << "Enter prime number q: ";
    cin >> q;
    if(!isPrime(q)) {
        cout << "q is not a prime number" << endl;
        return 0;
    }

    if(p == q) {
        cout << "p and q must be different primes" << endl;
        return 0;
    }

    int n = p * q;
    int phi = (p-1) * (q-1);

    if(n < 128) {
        cout << "n = p*q must be at least 128 to encrypt text" << endl;
        return 0;
    }

    int e = 2;
    while(gcd(e, phi) != 1)
        e++;

    int d = modInverse(e, phi);

    cout << "\nn = " << n << endl;
    cout << "phi(n) = " << phi << endl;
    cout << "Public Key (e, n) = (" << e << ", " << n << ")" << endl;
    cout << "Private Key (d, n) = (" << d << ", " << n << ")" << endl;

    cin.ignore();
    string message;
    cout << "\nEnter message: ";
    getline(cin, message);

    vector<int> cipher;
    cout << "\nEncrypted Text: ";
    for(size_t i = 0; i < message.length(); i++) {
        int m = (unsigned char)message[i];
        if(m >= n) {
            cout << "\nCharacter value " << m << " is too large for n = " << n << endl;
            return 0;
        }
        cipher.push_back(modPow(m, e, n));
        cout << cipher[i] << " ";
    }
    cout << endl;

    string decrypted = "";
    for(size_t i = 0; i < cipher.size(); i++)
        decrypted += char(modPow(cipher[i], d, n));

    cout << "Decrypted Text: " << decrypted << endl;

    return 0;
}
