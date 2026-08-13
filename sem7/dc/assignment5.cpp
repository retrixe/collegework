#include <iostream>
using namespace std;

int n;
bool alive[100];
bool participated[100];
int coordinator;

void election(int p) {
    participated[p]=true;
    cout<<"Process "<<p<<" has started election\n";

    for(int q=p+1;q<=n;q++)
        cout<<"message sent to "<<q<<"\n";

    bool gotReply=false;
    for(int q=p+1;q<=n;q++) {
        if(alive[q]) {
            cout<<"id : "<<q<<" replies ok\n";
            gotReply=true;
        }
    }

    if(!gotReply) {
        coordinator=p;
        cout<<"\nProcess "<<p<<" is coordinator now\n\n";
        for(int q=1;q<=n;q++)
            if(q!=p)
                cout<<"Coordinator message sent to Process "<<q<<"\n";
        return;
    }

    for(int q=p+1;q<=n;q++)
        if(alive[q]&&!participated[q])
            election(q);
}

int main() {
    cout<<"Enter number of processes: ";
    cin>>n;
    if(n<2||n>99) {
        cout<<"Number of processes must be between 2 and 99";
        return 0;
    }

    for(int i=1;i<=n;i++) {
        alive[i]=true;
        participated[i]=false;
    }
    // the highest process is the coordinator, and it has failed
    coordinator=n;
    cout<<"Process with id : "<<n<<" is coordinator.\n";
    alive[n]=false;
    cout<<"id : "<<n<<" is  failed\n";

    int initiator;
    cout<<"Enter id of the process that starts the election: ";
    cin>>initiator;
    if(initiator<1||initiator>n||!alive[initiator]) {
        cout<<"Initiator must be an alive process";
        return 0;
    }
    cout<<"id : "<<initiator<<" has started the election\n";

    election(initiator);

    return 0;
}
