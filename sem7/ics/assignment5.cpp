#include<iostream>
using namespace std;

long long power(long long a,long long b,long long p){
    long long result=1;
    for(int i=0;i<b;i++)
        result=(result*a)%p;
    return result;
}

int main(){
    long long p,g,a,b,A,B,KA,KB;
    cout<<"Enter prime number p: ";
    cin>>p;
    cout<<"Enter primitive root g: ";
    cin>>g;
    cout<<"Enter private key of Alice: ";
    cin>>a;
    cout<<"Enter private key of Bob: ";
    cin>>b;

    A=power(g,a,p);
    B=power(g,b,p);

    cout<<"Alice's public key: "<<A<<endl;
    cout<<"Bob's public key: "<<B<<endl;

    KA=power(B,a,p);
    KB=power(A,b,p);

    cout<<"Alice's shared secret key: "<<KA<<endl;
    cout<<"Bob's shared secret key: "<<KB<<endl;

    if(KA==KB)
        cout<<"Key exchange successful"<<endl;
    else
        cout<<"Key exchange failed"<<endl;

    return 0;
}