#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <sstream>
using namespace std;

struct MNTEntry{
    string name;
    int mdtIndex;
};

vector<string> tokenize(string line){
    vector<string> tokens;
    string temp="";
    for(size_t i=0;i<=line.length();i++){
        if(i==line.length()||line[i]==' '||line[i]==','||line[i]=='\t'||line[i]=='\r'){
            if(temp!=""){
                tokens.push_back(temp);
                temp="";
            }
        }else temp+=line[i];
    }
    return tokens;
}

int main(){
    ifstream fmnt("mnt.txt"),fmdt("mdt.txt"),fint("intermediate.txt");
    if(!fmnt||!fmdt||!fint){
        cout<<"Cannot open mnt.txt / mdt.txt / intermediate.txt\n";
        return 0;
    }

    vector<MNTEntry> mnt;
    string line;
    while(getline(fmnt,line)){
        vector<string> t=tokenize(line);
        if(t.size()>=3)
            mnt.push_back({t[1],stoi(t[2])});
    }

    vector<string> mdt;
    while(getline(fmdt,line))
        if(line.size()) mdt.push_back(line);

    vector<string> expanded;

    while(getline(fint,line)){
        if(line.size()==0) continue;
        vector<string> tokens=tokenize(line);
        if(tokens.empty()) continue;

        int m=-1;
        for(size_t i=0;i<mnt.size();i++)
            if(mnt[i].name==tokens[0]) m=i;

        if(m==-1){
            expanded.push_back(line);
            continue;
        }

        vector<string> ala;
        for(size_t i=1;i<tokens.size();i++)
            ala.push_back(tokens[i]);

        cout<<"\nExpanding call: "<<line<<"\n";
        cout<<left<<setw(8)<<"Index"<<"Actual Argument (ALA)"<<endl;
        for(size_t i=0;i<ala.size();i++)
            cout<<left<<setw(8)<<i+1<<ala[i]<<endl;

        for(size_t i=mnt[m].mdtIndex;i<mdt.size();i++){
            string stmt=mdt[i];
            if(tokenize(stmt)[0]=="MEND")
                break;
            for(int k=(int)ala.size();k>=1;k--){
                string marker="#"+to_string(k);
                size_t pos;
                while((pos=stmt.find(marker))!=string::npos)
                    stmt=stmt.substr(0,pos)+ala[k-1]+stmt.substr(pos+marker.length());
            }
            expanded.push_back("+ "+stmt);
        }
    }

    cout<<"\n======= EXPANDED SOURCE =======\n";
    for(string s:expanded)
        cout<<s<<endl;

    ofstream f("expanded.txt");
    for(string s:expanded)
        f<<s<<"\n";
    f.close();

    cout<<"\nexpanded.txt generated\n";

    return 0;
}
