%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
void yyerror(const char *s);
%}

%token IF THEN OP CP ROP AOP ID NUM

%%

sd   : sif '\n'              { printf("sd   -> sif\n"); printf("Valid statement\n"); exit(0); };
sif  : IF cmp THEN stmt      { printf("sif  -> if cmp then stmt\n"); };
cmp  : OP ID ROP ID CP       { printf("cmp  -> ( id rop id )\n"); };
stmt : ID AOP NUM            { printf("stmt -> id = num\n"); };

%%

void yyerror(const char *s) {
  printf("Invalid statement: %s\n", s);
  exit(0);
}

int main() {
  printf("Enter statement: ");
  yyparse();
  return 0;
}
