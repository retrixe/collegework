#include <iostream>
#include <string>
using namespace std;

int P10[] = {3,5,2,7,4,10,1,9,8,6};
int P8[] = {6,3,7,4,8,5,10,9};
int IP[] = {2,6,3,1,4,8,5,7};
int IP_INV[] = {4,1,3,5,7,2,8,6};
int EP[] = {4,1,2,3,2,3,4,1};
int P4[] = {2,4,3,1};

int S0[4][4] = {
    {1,0,3,2},
    {3,2,1,0},
    {0,2,1,3},
    {3,1,3,2}
};

int S1[4][4] = {
    {0,1,2,3},
    {2,0,1,3},
    {3,0,1,0},
    {2,1,0,3}
};

bool isBinary(string s) {
    for(char c : s)
        if(c != '0' && c != '1')
            return false;
    return true;
}

string permute(string bits, int table[], int size) {
    string result = "";
    for(int i = 0; i < size; i++)
        result += bits[table[i]-1];
    return result;
}

string leftShift(string bits, int shifts) {
    while(shifts--)
        bits = bits.substr(1) + bits[0];
    return bits;
}

string XOR(string a, string b) {
    string result = "";
    for(int i = 0; i < a.length(); i++) {
        if(a[i] == b[i])
            result += '0';
        else
            result += '1';
    }
    return result;
}

string sbox(string input) {
    string left = input.substr(0,4);
    string right = input.substr(4,4);

    int row = (left[0]-'0')*2 + (left[3]-'0');
    int col = (left[1]-'0')*2 + (left[2]-'0');
    int val1 = S0[row][col];

    row = (right[0]-'0')*2 + (right[3]-'0');
    col = (right[1]-'0')*2 + (right[2]-'0');
    int val2 = S1[row][col];

    string out = "";
    out += char((val1/2)+'0');
    out += char((val1%2)+'0');
    out += char((val2/2)+'0');
    out += char((val2%2)+'0');

    return permute(out,P4,4);
}

string fk(string bits, string key) {
    string left = bits.substr(0,4);
    string right = bits.substr(4,4);

    string temp = permute(right,EP,8);
    temp = XOR(temp,key);
    temp = sbox(temp);

    left = XOR(left,temp);

    return left + right;
}

string SW(string bits) {
    return bits.substr(4,4) + bits.substr(0,4);
}

int main() {
    string key, plaintext;

    cout << "Enter 10-bit Key: ";
    cin >> key;

    if(key.length()>10 || key.length()<10) {
        cout << "Key is not of 10 bits" << endl;
        return 0;
    }

    if(!isBinary(key)) {
        cout << "Error: Key can only have 0 and 1." << endl;
        return 0;
    }

    cout << "Enter 8-bit Plaintext: ";
    cin >> plaintext;

    if(plaintext.length()>8 || plaintext.length()<8) {
        cout << "Plaintext is not of 8 bits" << endl;
        return 0;
    }

    if(!isBinary(plaintext)) {
        cout << "Error: Plaintext can only have 0 and 1." << endl;
        return 0;
    }

    string temp = permute(key,P10,10);

    string left = temp.substr(0,5);
    string right = temp.substr(5,5);

    left = leftShift(left,1);
    right = leftShift(right,1);

    string K1 = permute(left+right,P8,8);

    left = leftShift(left,2);
    right = leftShift(right,2);

    string K2 = permute(left+right,P8,8);

    cout << "\nGenerated Keys are: \n";
    cout << "K1 = " << K1 << endl;
    cout << "K2 = " << K2 << endl;

    temp = permute(plaintext,IP,8);
    temp = fk(temp,K1);
    temp = SW(temp);
    temp = fk(temp,K2);
    string cipher = permute(temp,IP_INV,8);

    cout << "\nCipher Text = " << cipher << endl;

    temp = permute(cipher,IP,8);
    temp = fk(temp,K2);
    temp = SW(temp);
    temp = fk(temp,K1);
    string plain = permute(temp,IP_INV,8);

    cout << "Decrypted Text = " << plain << endl;

    return 0;
}