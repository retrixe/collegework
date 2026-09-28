%{
#include <stdio.h>
%}

identifier                      [a-zA-Z_][a-zA-Z0-9_]*
datatypes                       int|char|float|double|void
keywords                        if|else|else\ if|for|while|return
whitespace                      [ \t\n]+

%%

"//".*                          { fprintf(yyout,"comment: %s\n", yytext); }

    /* ---- function and array rules: trailing context (name/lookahead) ---- */
    /* keyword rule first so "if (" is not taken as a function call */
(if|for|while|switch)/[ \t]*\(       { fprintf(yyout,"keyword: %s\n", yytext); }
{datatypes}[ \t]+{identifier}/[ \t]*\(   { fprintf(yyout,"function definition: %s\n", yytext); }
{identifier}/[ \t]*\(                { fprintf(yyout,"function call: %s\n", yytext); }
{datatypes}[ \t]+{identifier}/[ \t]*\[   { fprintf(yyout,"array declaration: %s\n", yytext); }
{identifier}/[ \t]*\[                { fprintf(yyout,"array: %s\n", yytext); }
    /* ---- end of function and array rules ---- */

{datatypes}                     { fprintf(yyout,"datatype: %s\n", yytext); }
{keywords}                      { fprintf(yyout,"keyword: %s\n", yytext); }
{identifier}                    { fprintf(yyout,"identifier: %s\n", yytext); }

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
    return 0;
}

int yywrap()
{
    return 1;
}
