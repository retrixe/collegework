#include <iostream>
using namespace std;

/* corrections applied to each process: from real-time row corrRow,
   the clock value is row + corrOffset (so later ticks carry it forward) */
int corrCount[100], corrRow[100][100], corrOffset[100][100];

int offsetAt(int p,int t){
    int off=0;
    for(int k=0;k<corrCount[p];k++)
        if(corrRow[p][k]<=t) off=corrOffset[p][k];
    return off;
}

int clockAt(int p,int t){
    return t+offsetAt(p,t);
}

int main(){
    int n;
    cout<<"Enter the number of processes: ";
    cin>>n;

    int clock[100],clockRate[100];

    for(int i=1;i<=n;i++){
        clock[i]=0;
        corrCount[i]=0;
        cout<<"Enter clock rate of P"<<i<<": ";
        cin>>clockRate[i];
    }

    cout<<"\n===== CLOCK BEFORE SENDING MESSAGES =====\n\n";

    for(int i=1;i<=n;i++){
        cout<<"P"<<i<<": ";

        for(int t=0;t<=60;t+=clockRate[i]){
            cout<<t;

            if(t+clockRate[i]<=60)
                cout<<" -> ";
        }

        cout<<endl;
    }

    int messages;
    cout<<"\nEnter the number of messages: ";
    cin>>messages;

    int sender[100],receiver[100],sendTime[100],receiveTime[100];

    for(int i=1;i<=messages;i++){
        cout<<"\nMessage M"<<i<<":\n";

        cout<<"Enter sender process: P";
        cin>>sender[i];

        cout<<"Enter receiver process: P";
        cin>>receiver[i];

        cout<<"Enter time at which message is sent: ";
        cin>>sendTime[i];

        cout<<"Enter time at which message is received: ";
        cin>>receiveTime[i];

        /* actual clock values, including corrections from earlier messages */
        int sendClock=clockAt(sender[i],sendTime[i]);
        int recvClock=clockAt(receiver[i],receiveTime[i]);

        cout<<"\n===== M"<<i<<" =====\n";

        cout<<"P"<<sender[i]<<" sends M"<<i
            <<" at time "<<sendClock<<endl;

        cout<<"P"<<receiver[i]<<" receives M"<<i
            <<" at time "<<recvClock<<endl;

        clock[sender[i]]=sendClock;

        if(sendClock<recvClock){
            clock[receiver[i]]=recvClock;
            cout<<"Sender time < Receiver time -> No clock adjustment"<<endl;
        }
        else{
            clock[receiver[i]]=sendClock+1;

            /* from the receive row onward, clock = row + offset */
            int p=receiver[i];
            corrRow[p][corrCount[p]]=receiveTime[i];
            corrOffset[p][corrCount[p]]=sendClock+1-receiveTime[i];
            corrCount[p]++;

            cout<<"Sender time >= Receiver time -> Clock adjusted"<<endl;
            cout<<"P"<<receiver[i]<<" clock adjusted to "
                <<clock[receiver[i]]<<endl;
        }

        cout<<"\nMessage Diagram:\n\n";

        for(int j=1;j<=n;j++){
            cout<<"P"<<j;
            if(j<n)
                cout<<"          ";
        }
        cout<<endl;

        for(int j=1;j<=n;j++){
            cout<<"|";
            if(j<n)
                cout<<"          ";
        }
        cout<<endl;

        for(int t=0;t<=60;t++){

            bool show=false;

            for(int j=1;j<=n;j++)
                if(t%clockRate[j]==0)
                    show=true;

            if(t==sendTime[i] || t==receiveTime[i])
                show=true;

            if(!show)
                continue;

            for(int j=1;j<=n;j++){

                bool printed=false;

                if((j==sender[i] && t==sendTime[i]) ||
                   (j==receiver[i] && t==receiveTime[i]) ||
                   t%clockRate[j]==0){
                    cout<<clockAt(j,t);
                    printed=true;
                }

                if(!printed)
                    cout<<" ";

                if(j<n)
                    cout<<"          ";
            }

            cout<<endl;

            if(t==sendTime[i]){
                if(sender[i]<receiver[i])
                    cout<<"|-------- M"<<i<<" -------->";
                else
                    cout<<"<-------- M"<<i<<" --------|";

                cout<<endl;
            }

            for(int j=1;j<=n;j++){
                cout<<"|";
                if(j<n)
                    cout<<"          ";
            }

            cout<<endl;
        }

        cout<<"Send time    = "<<sendClock<<endl;
        cout<<"Receive time = "<<clock[receiver[i]]<<endl;

        cout<<"\nClocks after M"<<i<<":\n";

        for(int j=1;j<=n;j++)
            cout<<"P"<<j<<" = "<<clock[j]<<endl;
    }

    cout<<"\n===== FINAL CLOCK VALUES =====\n";

    for(int i=1;i<=n;i++)
        cout<<"P"<<i<<" = "<<clock[i]<<endl;

    return 0;
}
