%{
#include "y.tab.h"
%}

%%

"if"                        { return IF; }
"then"                      { return THEN; }
"("                         { return OP; }
")"                         { return CP; }
"<"|">"|"<="|">="|"=="|"!=" { return ROP; }
"="                         { return AOP; }
[0-9]+                      { return NUM; }
[a-zA-Z_][a-zA-Z0-9_]*      { return ID; }
[ \t]                       { }
\n                          { return '\n'; }
.                           { return yytext[0]; }

%%

int yywrap() {
  return 1;
}
