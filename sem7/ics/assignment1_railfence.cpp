#include <iostream>
#include <string>
using namespace std;

int main() {
    string text;
    int key;

    cout<<"Enter text: ";
    getline(cin, text);

    cout<<"Enter key: ";
    cin>>key;
    if(key<2) {
        cout<<"Key must be at least 2.";
        return 0;
    }

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

    return 0;
}
