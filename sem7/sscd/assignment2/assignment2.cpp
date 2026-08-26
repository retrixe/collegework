#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <map>
using namespace std;

map<int,int> loadTable(string filename){
    map<int,int> table;
    ifstream file(filename);
    if(!file){
        cout<<"Cannot open "<<filename<<"\n";
        return table;
    }
    int index,address;
    string name;
    while(file>>index>>name>>address)
        table[index]=address;
    return table;
}

int main(){
    map<int,int> symtab=loadTable("symbol.txt");
    map<int,int> littab=loadTable("littab.txt");

    ifstream file("file1.txt");
    if(!file){
        cout<<"Cannot open file1.txt\n";
        return 0;
    }

    cout<<"\n======= SYMBOL TABLE =======\n";
    cout<<left<<setw(10)<<"Index"<<setw(10)<<"Address"<<endl;
    for(auto &s:symtab)
        cout<<left<<setw(10)<<s.first<<setw(10)<<s.second<<endl;

    cout<<"\n======= LITERAL TABLE =======\n";
    cout<<left<<setw(10)<<"Index"<<setw(10)<<"Address"<<endl;
    for(auto &l:littab)
        cout<<left<<setw(10)<<l.first<<setw(10)<<l.second<<endl;

    cout<<"\n======= INTERMEDIATE CODE =======\n";
    vector<string> lines;
    string line;
    while(getline(file,line)){
        if(line.size()){
            cout<<line<<endl;
            lines.push_back(line);
        }
    }
    file.close();

    cout<<"\n======= MACHINE CODE =======\n";
    cout<<left<<setw(10)<<"LC"<<setw(10)<<"Opcode"<<setw(10)<<"Reg"<<setw(10)<<"Operand"<<endl;

    for(string line:lines){
        stringstream ss(line);
        vector<string> token;
        string t;
        while(ss>>t)
            token.push_back(t);

        if(token.empty()||!isdigit(token[0][0]))
            continue;

        string lc=token[0];
        string cls=token[1].substr(0,2);
        string code=token[1].substr(3);

        if(cls=="IS"){
            string reg=token[2];
            string operand="0";
            if(token.size()>3){
                string op=token[3];
                int idx=stoi(op.substr(2));
                if(op[0]=='S')
                    operand=to_string(symtab[idx]);
                else if(op[0]=='L')
                    operand=to_string(littab[idx]);
                else
                    operand=op.substr(2);
            }
            cout<<left<<setw(10)<<lc<<setw(10)<<stoi(code)<<setw(10)<<reg<<setw(10)<<operand<<endl;
        }
        else if(cls=="AD"){
            if(token.size()>2)
                cout<<left<<setw(10)<<lc<<setw(10)<<0<<setw(10)<<0<<setw(10)<<token[2]<<endl;
            else
                cout<<left<<setw(10)<<lc<<setw(10)<<0<<setw(10)<<0<<setw(10)<<0<<endl;
        }
        else if(cls=="DL"&&code=="1"){
            cout<<left<<setw(10)<<lc<<setw(10)<<0<<setw(10)<<0<<setw(10)<<token[2].substr(2)<<endl;
        }
    }

    return 0;
}
