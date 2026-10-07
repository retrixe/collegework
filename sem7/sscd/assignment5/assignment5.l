%{
#include <stdio.h>
#include <string.h>

char sym_name[100][32], sym_type[100][16], sym_kind[100][16];
int sym_count = 0;
char last_type[16] = "";   /* datatype seen just before an identifier */

void add_symbol(char *name, char *type, char *kind) {
    int i;
    for (i = 0; i < sym_count; i++)
        if (strcmp(sym_name[i], name) == 0) return;   /* already present */
    strcpy(sym_name[sym_count], name);
    strcpy(sym_type[sym_count], type);
    strcpy(sym_kind[sym_count], kind);
    sym_count++;
}

/* yytext is "type name" (function or array declaration) */
void add_declaration(char *text, char *kind) {
    char type[16], name[32];
    sscanf(text, "%s %s", type, name);
    add_symbol(name, type, kind);
}

void print_symbol_table(FILE *f) {
    int i;
    fprintf(f, "\nSYMBOL TABLE\n%-4s %-10s %-8s %s\n", "Sr", "Name", "Type", "Kind");
    for (i = 0; i < sym_count; i++)
        fprintf(f, "%-4d %-10s %-8s %s\n", i + 1, sym_name[i], sym_type[i], sym_kind[i]);
}
%}

identifier                      [a-zA-Z_][a-zA-Z0-9_]*
datatypes                       int|char|float|double|void
keywords                        if|else|else\ if|for|while|return
whitespace                      [ \t\n]+

%%

"//".*                          { fprintf(yyout,"comment: %s\n", yytext); }

{keywords}                      { fprintf(yyout,"keyword: %s\n", yytext); }
(if|for|while|switch)/{whitespace}*\(          { fprintf(yyout,"keyword: %s\n", yytext); }
{datatypes}{whitespace}{identifier}/{whitespace}*\(   { fprintf(yyout,"function definition: %s\n", yytext); add_declaration(yytext, "function"); }
{identifier}/{whitespace}*\(                   { fprintf(yyout,"function call: %s\n", yytext); }
{datatypes}{whitespace}{identifier}/{whitespace}*\[   { fprintf(yyout,"array declaration: %s\n", yytext); add_declaration(yytext, "array"); }
{identifier}/{whitespace}*\[                   { fprintf(yyout,"array: %s\n", yytext); }
{datatypes}                     { fprintf(yyout,"datatype: %s\n", yytext); strcpy(last_type, yytext); }
{identifier}                    { fprintf(yyout,"identifier: %s\n", yytext);
                                  if (last_type[0]) { add_symbol(yytext, last_type, "variable"); last_type[0] = 0; } }

[0-9]+\.[0-9]+                  { fprintf(yyout,"float number: %s\n", yytext); }
[0-9]+                          { fprintf(yyout,"integer: %s\n", yytext); }
\"[^\"]*\"                      { fprintf(yyout,"string: %s\n", yytext); }

"=="|"!="|"<="|">="|"&&"|"||"   { fprintf(yyout,"relational/logical operator: %s\n", yytext); }
[+\-*/%=<>]                     { fprintf(yyout,"operator: %s\n", yytext); }

[(){}\[\];,]                    { fprintf(yyout,"punctuation: %s\n", yytext); }


{whitespace}                    { }

%%

int main()
{
    yyin = fopen("input.txt","r");
    yyout = fopen("output.txt", "w");
    yylex();
    print_symbol_table(yyout);
    print_symbol_table(stdout);
    return 0;
}

int yywrap()
{
    return 1;
}
