#include <iostream>
#include <string>
using namespace std;

int main() {
    int choice;

    cout<<"1. Caesar Cipher\n2. Rail Fence Cipher\nEnter your choice: ";
    cin>>choice;
    cin.ignore();

    switch(choice) {
        case 1: {
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

            break;
        }

        case 2: {
            string text;
            int key;
            if(key)
            cout<<"Enter text: ";
            getline(cin, text);
            if(key<0) {
                cout<<"Key must be a non-negative integer.";
                return 0;
            }

            cout<<"Enter key: ";
            cin>>key;

            cout<<"Encrypted Text: ";

            for(int row=0;row<key;row++) {
                int index=row;
                bool down=true;

                while(index<text.length()) {
                    cout<<text[index];

                    if(row==0||row==key-1)
                        index+=2*(key-1);
                    else {
                        if(down)
                            index+=2*(key-row-1);
                        else
                            index+=2*row;
                        down=!down;
                    }
                }
            }

            break;
        }

        default:
            cout<<"Invalid Choice";
    }

    return 0;
}