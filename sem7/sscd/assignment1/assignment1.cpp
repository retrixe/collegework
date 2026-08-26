#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
using namespace std;

struct OPTAB{
    string opcode;
    string classType;
    int machineCode;
};

struct REGTAB{
    string regName;
    int regCode;
};

struct Symbol{
    string name;
    int address;
};

struct Literal{
    int value;
    int address;
};

OPTAB optab[]={
    {"START","AD",1},
    {"LTORG","AD",2},
    {"STOP","AD",3},
    {"ORIGIN","AD",4},
    {"EQU","AD",5},
    {"END","AD",6},
    {"MOVER","IS",1},
    {"MOVEM","IS",2},
    {"ADD","IS",3},
    {"BC","IS",4},
    {"SUB","IS",5},
    {"MULT","IS",6},
    {"DC","DL",1},
    {"DS","DL",2}
};

REGTAB regtab[]={
    {"AREG",1},
    {"BREG",2},
    {"CREG",3},
    {"DREG",4}
};

REGTAB condtab[]={
    {"LT",1},
    {"LE",2},
    {"EQ",3},
    {"GT",4},
    {"GE",5},
    {"ANY",6}
};

int searchOptab(string s){
    for(int i=0;i<14;i++)
        if(optab[i].opcode==s) return i;
    return -1;
}

int searchSymbol(vector<Symbol> &symtab,string s){
    for(int i=0;i<(int)symtab.size();i++)
        if(symtab[i].name==s) return i+1;
    return -1;
}

int getNumber(string s){
    string digits="";
    for(char c:s)
        if(c>='0'&&c<='9') digits+=c;
    return stoi(digits);
}

int evaluate(string expr,vector<Symbol> &symtab){
    int sign=1;
    size_t pos=expr.find('+');
    if(pos==string::npos){
        pos=expr.find('-');
        sign=-1;
    }
    if(pos==string::npos){
        if(expr[0]>='0'&&expr[0]<='9') return stoi(expr);
        int idx=searchSymbol(symtab,expr);
        return symtab[idx-1].address;
    }
    string base=expr.substr(0,pos);
    int offset=stoi(expr.substr(pos+1));
    int idx=searchSymbol(symtab,base);
    return symtab[idx-1].address+sign*offset;
}

int main(){

    ifstream file("inputAssign1.txt");
    if(!file){
        cout<<"Cannot open inputAssign1.txt\n";
        return 0;
    }

    vector<string> lines;
    string line;

    cout<<"Input:\n";
    while(getline(file,line)){
        if(line.size()){
            cout<<line<<endl;
            lines.push_back(line);
        }
    }
    file.close();

    cout<<"\n======= OPTAB =======\n";
    cout<<left<<setw(10)<<"Opcode"<<setw(10)<<"Class"<<setw(10)<<"Code"<<endl;
    for(int i=0;i<14;i++)
        cout<<left<<setw(10)<<optab[i].opcode<<setw(10)<<optab[i].classType<<setw(10)<<optab[i].machineCode<<endl;

    cout<<"\n======= REGTAB =======\n";
    cout<<left<<setw(10)<<"Reg"<<setw(10)<<"Code"<<endl;
    for(int i=0;i<4;i++)
        cout<<left<<setw(10)<<regtab[i].regName<<setw(10)<<regtab[i].regCode<<endl;

    vector<Symbol> symtab;
    vector<Literal> littab;
    vector<int> pooltab;
    vector<string> ic;

    int LC=0;
    int poolStart=0;
    pooltab.push_back(1);

    cout<<"\n======= TOKEN TABLE =======\n";
    cout<<left<<setw(10)<<"Label"<<setw(10)<<"Opcode"<<setw(10)<<"Op1"<<setw(10)<<"Op2"<<endl;

    for(string line:lines){

        string token[4];
        int count=0;
        string temp="";

        for(size_t i=0;i<=line.length();i++){
            if(i==line.length()||line[i]==' '||line[i]==','||line[i]=='\t'||line[i]=='\r'){
                if(temp!=""){
                    token[count++]=temp;
                    temp="";
                }
            }else temp+=line[i];
        }

        string label="-",opcode="-",op1="-",op2="-";
        int pos=0;

        if(count>1&&searchOptab(token[0])==-1){
            label=token[0];
            pos=1;
        }
        opcode=token[pos];
        if(pos+1<count) op1=token[pos+1];
        if(pos+2<count) op2=token[pos+2];

        cout<<left<<setw(10)<<label<<setw(10)<<opcode<<setw(10)<<op1<<setw(10)<<op2<<endl;

        int opIdx=searchOptab(opcode);
        if(opIdx==-1) continue;
        string opClass=optab[opIdx].classType;
        int opCode=optab[opIdx].machineCode;

        if(label!="-"&&opcode!="EQU"&&opcode!="START"){
            int idx=searchSymbol(symtab,label);
            if(idx==-1)
                symtab.push_back({label,LC});
            else
                symtab[idx-1].address=LC;
        }

        if(opcode=="START"){
            LC=stoi(op1);
            ic.push_back("AD,01 C,"+op1);
        }
        else if(opcode=="ORIGIN"){
            LC=evaluate(op1,symtab);
            ic.push_back("AD,4 C,"+to_string(LC));
        }
        else if(opcode=="EQU"){
            int val=evaluate(op1,symtab);
            int idx=searchSymbol(symtab,label);
            if(idx==-1)
                symtab.push_back({label,val});
            else
                symtab[idx-1].address=val;
            ic.push_back("AD,5 C,"+to_string(val));
        }
        else if(opcode=="STOP"){
            ic.push_back(to_string(LC)+" AD,3");
            LC++;
        }
        else if(opcode=="LTORG"||opcode=="END"){
            string code=(opcode=="LTORG")?"AD,2":"AD,6";
            bool pending=false;
            for(int i=poolStart;i<(int)littab.size();i++){
                littab[i].address=LC;
                ic.push_back(to_string(LC)+" "+code+" "+to_string(littab[i].value));
                LC++;
                pending=true;
            }
            if(opcode=="END"&&!pending)
                ic.push_back("AD,6");
            if(opcode=="LTORG"){
                poolStart=littab.size();
                pooltab.push_back(poolStart+1);
            }
        }
        else if(opcode=="DC"){
            ic.push_back(to_string(LC)+" DL,1 C,"+to_string(getNumber(op1)));
            LC++;
        }
        else if(opcode=="DS"){
            ic.push_back(to_string(LC)+" DL,2 C,"+op1);
            LC+=stoi(op1);
        }
        else if(opClass=="IS"){
            int reg=0;
            REGTAB *tab=(opcode=="BC")?condtab:regtab;
            int tabSize=(opcode=="BC")?6:4;
            for(int i=0;i<tabSize;i++)
                if(tab[i].regName==op1) reg=tab[i].regCode;

            string operand;
            if(op2[0]=='='){
                int found=-1;
                for(int i=poolStart;i<(int)littab.size();i++)
                    if(littab[i].value==getNumber(op2)) found=i+1;
                if(found==-1){
                    littab.push_back({getNumber(op2),-1});
                    found=littab.size();
                }
                operand="L,"+to_string(found);
            }else{
                int idx=searchSymbol(symtab,op2);
                if(idx==-1){
                    symtab.push_back({op2,-1});
                    idx=symtab.size();
                }
                operand="S,"+to_string(idx);
            }

            ic.push_back(to_string(LC)+" IS,"+to_string(opCode)+" "+to_string(reg)+" "+operand);
            LC++;
        }
    }

    cout<<"\n======= SYMBOL TABLE =======\n";
    cout<<left<<setw(10)<<"Index"<<setw(10)<<"Symbol"<<setw(10)<<"Address"<<endl;
    for(int i=0;i<(int)symtab.size();i++)
        cout<<left<<setw(10)<<i+1<<setw(10)<<symtab[i].name<<setw(10)<<symtab[i].address<<endl;

    cout<<"\n======= LITERAL TABLE =======\n";
    cout<<left<<setw(10)<<"Index"<<setw(10)<<"Literal"<<setw(10)<<"Address"<<endl;
    for(int i=0;i<(int)littab.size();i++)
        cout<<left<<setw(10)<<i+1<<setw(10)<<littab[i].value<<setw(10)<<littab[i].address<<endl;

    cout<<"\n======= POOL TABLE =======\n";
    cout<<left<<setw(10)<<"Pool"<<setw(15)<<"LITTAB Index"<<endl;
    for(int i=0;i<(int)pooltab.size();i++)
        if(pooltab[i]<=(int)littab.size())
            cout<<left<<setw(10)<<i+1<<setw(15)<<pooltab[i]<<endl;

    cout<<"\n======= INTERMEDIATE CODE =======\n";
    for(string s:ic)
        cout<<s<<endl;

    ofstream f1("file1.txt");
    for(string s:ic)
        f1<<s<<"\n";
    f1.close();

    ofstream f2("symbol.txt");
    for(int i=0;i<(int)symtab.size();i++)
        f2<<i+1<<" "<<symtab[i].name<<" "<<symtab[i].address<<"\n";
    f2.close();

    ofstream f3("littab.txt");
    for(int i=0;i<(int)littab.size();i++)
        f3<<i+1<<" "<<littab[i].value<<" "<<littab[i].address<<"\n";
    f3.close();

    cout<<"\nfile1.txt, symbol.txt, littab.txt generated for Pass 2\n";

    return 0;
}
