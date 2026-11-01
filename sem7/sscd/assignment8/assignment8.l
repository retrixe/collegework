%{
#include "y.tab.h"
extern int yylval;
%}

%%

[0-9]+                      { yylval = atoi(yytext); return NUM; }
"+"                         { return PLUS; }
"-"                         { return MINUS; }
"*"                         { return MUL; }
"/"                         { return DIV; }
"%"                         { return MOD; }
[ \t]                       { }
\n                          { return '\n'; }
.                           { return yytext[0]; }

%%

int yywrap() {
  return 1;
}
