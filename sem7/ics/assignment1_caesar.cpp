#include <iostream>
#include <string>
using namespace std;

int main() {
    string text;
    int key, op;

    cout<<"1. Encrypt\n2. Decrypt\nEnter operation: ";
    cin>>op;
    cin.ignore();

    cout<<"Enter text: ";
    getline(cin, text);

    cout<<"Enter key: ";
    cin>>key;
    if(key<0) {
        cout<<"Key must be a non-negative integer.";
        return 0;
    }

    if(op==1) {
        for(int i=0;i<text.length();i++) {
            if(text[i]>='A'&&text[i]<='Z')
                text[i]=(text[i]-'A'+key)%26+'A';
            else if(text[i]>='a'&&text[i]<='z')
                text[i]=(text[i]-'a'+key)%26+'a';
        }
        cout<<"Encrypted Text: "<<text;
    }
    else if(op==2) {
        for(int i=0;i<text.length();i++) {
            if(text[i]>='A'&&text[i]<='Z')
                text[i]=(text[i]-'A'-key+26)%26+'A';
            else if(text[i]>='a'&&text[i]<='z')
                text[i]=(text[i]-'a'-key+26)%26+'a';
        }
        cout<<"Decrypted Text: "<<text;
    }
    else
        cout<<"Invalid Operation";

    return 0;
}
