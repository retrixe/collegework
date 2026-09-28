%{
#include <stdio.h>
%}

num     [0-9]+
negnum [-][0-9]+
floating_point [0-9]*\.[0-9]+
L       [a-zA-Z]
space [ ]

%%

int|char|float       { fprintf(yyout,"datatype found %s\n", yytext); }
{space} {}
{floating_point}	{fprintf(yyout,"float number %s\n", yytext);}
{negnum}	{fprintf(yyout,"negative number %s\n", yytext);}
{num}       { fprintf(yyout,"num detected %s\n", yytext); }
if|else|else\ if	{fprintf(yyout,"if else condition it is %s\n", yytext);}
for|while	{fprintf(yyout,"loop it is %s\n", yytext);}
switch|case	{fprintf(yyout,"this is case senario %s\n", yytext);}
&&|\|\|	{fprintf(yyout,"condtion to check 2 statement %s\n", yytext);}
{L}({L}|{num})*   { fprintf(yyout,"var number combo detected %s\n", yytext); }
\+ { fprintf(yyout,"add operator: %s\n", yytext); }
\- { fprintf(yyout,"sub operator: %s\n", yytext); }
\* { fprintf(yyout,"multi operator: %s\n", yytext); }
\/ { fprintf(yyout,"divide operator: %s\n", yytext); }

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
