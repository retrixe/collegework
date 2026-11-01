/*
procedure E()
	T()
	E'()
end

procedure E'()
	if input_symbol = '+' then
		ADVANCE()
		T()
		E'()
	end
end

procedure T()
	F()
	T'()
end

procedure T'()
	if input_symbol = '*' then begin
		ADVANCE()
		F()
		T'()
	end
end

procedure F()
	if input_symbol = '(' then
		ADVANCE()
		E()
		if input_symbol = ')' then
			ADVANCE()
		else
			ERROR()
		end
	else if input_symbol = id then
		ADVANCE()
	else
		ERROR()
	end
end
*/

/*
Grammar (left recursion removed):
    E  -> T E'
    E' -> + T E' | e
    T  -> F T'
    T' -> * F T' | e
    F  -> ( E ) | id
id is any identifier or number, e.g. a, x1, 25
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char input[100];
int pos = 0;
int depth = 0;

void e();
void e_dash();
void t();
void t_dash();
void f();

void skip_spaces() {
    while (input[pos] == ' ' || input[pos] == '\t')
        pos++;
}

char input_symbol() {
    skip_spaces();
    return input[pos];
}

void trace(char *procedure) {
    int i;
    for (i = 0; i < depth; i++)
        printf("  ");
    printf("%s  remaining: %s\n", procedure, input + pos);
}

void advance() {
    skip_spaces();
    pos++;
}

void error() {
    skip_spaces();
    if (input[pos] == '\0')
        printf("\nError at position %d: unexpected end of input\n", pos);
    else
        printf("\nError at position %d near '%s'\n", pos, input + pos);
    printf("String is not accepted\n");
    exit(0);
}

void e() {
    trace("E -> T E'");
    depth++;
    t();
    e_dash();
    depth--;
}

void e_dash() {
    if (input_symbol() == '+') {
        trace("E' -> + T E'");
        depth++;
        advance();
        t();
        e_dash();
        depth--;
    } else {
        trace("E' -> e");
    }
}

void t() {
    trace("T -> F T'");
    depth++;
    f();
    t_dash();
    depth--;
}

void t_dash() {
    if (input_symbol() == '*') {
        trace("T' -> * F T'");
        depth++;
        advance();
        f();
        t_dash();
        depth--;
    } else {
        trace("T' -> e");
    }
}

void f() {
    if (input_symbol() == '(') {
        trace("F -> ( E )");
        depth++;
        advance();
        e();
        if (input_symbol() == ')')
            advance();
        else
            error();
        depth--;
    } else if (isalnum(input_symbol())) {
        trace("F -> id");
        while (isalnum(input[pos]) || input[pos] == '_')
            pos++;
    } else {
        error();
    }
}

int main() {
    printf("Enter expression: ");
    if (fgets(input, sizeof(input), stdin) == NULL)
        return 0;
    input[strcspn(input, "\n")] = '\0';

    printf("\nParsing steps:\n");
    e();

    if (input_symbol() == '\0')
        printf("\nString is accepted\n");
    else
        error();

    return 0;
}
