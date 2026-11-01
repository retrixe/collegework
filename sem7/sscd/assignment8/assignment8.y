%{
#include <stdio.h>
#include <stdlib.h>

int yylex();
void yyerror(const char *s);
%}

%token NUM PLUS MINUS MUL DIV MOD

%%

ed : e '\n'                  { $$ = $1; printf("ed -> e\n");
                               printf("Valid expression -- Result: %d\n", $1); exit(0); };
e  : NUM PLUS NUM            { $$ = $1 + $3; printf("e  -> num + num\n"); }
e  : NUM MINUS NUM           { $$ = $1 - $3; printf("e  -> num - num\n"); }
e  : NUM MUL NUM             { $$ = $1 * $3; printf("e  -> num * num\n"); }
e  : NUM DIV NUM             { if ($3 == 0) { printf("Error: division by zero\n"); exit(0); }
                               $$ = $1 / $3; printf("e  -> num / num\n"); }
e  : NUM MOD NUM             { if ($3 == 0) { printf("Error: division by zero\n"); exit(0); }
                               $$ = $1 % $3; printf("e  -> num %% num\n"); };

%%

void yyerror(const char *s) {
  printf("Invalid expression: %s\n", s);
  exit(0);
}

int main() {
  printf("Enter expression: ");
  yyparse();
  return 0;
}
