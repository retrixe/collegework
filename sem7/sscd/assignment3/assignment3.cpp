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
    ifstream file("inputAssign3.txt");
    if(!file){
        cout<<"Cannot open inputAssign3.txt\n";
        return 0;
    }

    vector<string> mdt;
    vector<MNTEntry> mnt;
    vector<string> ala;
    vector<string> intermediate;

    string line;
    bool inDefinition=false;
    bool expectPrototype=false;

    cout<<"Input:\n";
    while(getline(file,line)){
        if(line.size()==0) continue;
        cout<<line<<endl;
        vector<string> tokens=tokenize(line);
        if(tokens.empty()) continue;

        if(tokens[0]=="MACRO"){
            inDefinition=true;
            expectPrototype=true;
        }
        else if(expectPrototype){
            mnt.push_back({tokens[0],(int)mdt.size()+1});
            ala.clear();
            for(size_t i=1;i<tokens.size();i++)
                ala.push_back(tokens[i]);
            mdt.push_back(line);
            expectPrototype=false;
        }
        else if(inDefinition){
            string stmt=line;
            for(size_t k=0;k<ala.size();k++){
                size_t pos;
                while((pos=stmt.find(ala[k]))!=string::npos)
                    stmt=stmt.substr(0,pos)+"#"+to_string(k+1)+stmt.substr(pos+ala[k].length());
            }
            mdt.push_back(stmt);
            if(tokens[0]=="MEND")
                inDefinition=false;
        }
        else{
            intermediate.push_back(line);
        }
    }
    file.close();

    cout<<"\n======= MNT =======\n";
    cout<<left<<setw(8)<<"Index"<<setw(12)<<"Macro Name"<<setw(10)<<"MDT Index"<<endl;
    for(size_t i=0;i<mnt.size();i++)
        cout<<left<<setw(8)<<i+1<<setw(12)<<mnt[i].name<<setw(10)<<mnt[i].mdtIndex<<endl;

    cout<<"\n======= MDT =======\n";
    cout<<left<<setw(8)<<"Index"<<"MDT Instruction"<<endl;
    for(size_t i=0;i<mdt.size();i++)
        cout<<left<<setw(8)<<i+1<<mdt[i]<<endl;

    cout<<"\n======= ALA =======\n";
    cout<<left<<setw(8)<<"Index"<<"Dummy Argument"<<endl;
    for(size_t i=0;i<ala.size();i++)
        cout<<left<<setw(8)<<i+1<<ala[i]<<endl;

    cout<<"\n======= INTERMEDIATE FILE =======\n";
    for(string s:intermediate)
        cout<<s<<endl;

    ofstream f1("mnt.txt");
    for(size_t i=0;i<mnt.size();i++)
        f1<<i+1<<" "<<mnt[i].name<<" "<<mnt[i].mdtIndex<<"\n";
    f1.close();

    ofstream f2("mdt.txt");
    for(size_t i=0;i<mdt.size();i++)
        f2<<mdt[i]<<"\n";
    f2.close();

    ofstream f3("ala.txt");
    for(size_t i=0;i<ala.size();i++)
        f3<<i+1<<" "<<ala[i]<<"\n";
    f3.close();

    ofstream f4("intermediate.txt");
    for(string s:intermediate)
        f4<<s<<"\n";
    f4.close();

    cout<<"\nmnt.txt, mdt.txt, ala.txt, intermediate.txt generated for Pass 2\n";

    return 0;
}
