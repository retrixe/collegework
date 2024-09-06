#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX 40

char stack[MAX];
char* sstack[MAX];
int top = -1;

int isFull();

int isEmpty();

void push(char element);

char pop();

void spush(char* element);

char* spop();

void strrev(char str[MAX]);

void infixToPrefix(char infix[MAX], char prefix[MAX]);

void infixToPostfix(char infix[MAX], char postfix[MAX]);

void prefixToInfix(char prefix[MAX], char infix[MAX]);

void postfixToInfix(char postfix[MAX], char infix[MAX]);

void prefixToPostfix(char prefix[MAX], char postfix[MAX]);

void postfixToPrefix(char postfix[MAX], char prefix[MAX]);

int isOperand(char op);

int isp(char op);

int icp(char op);

int main() {
	while (1) {
		int choice;
		printf("===============\n");
		printf("Select choice:\n1. Infix\n2. Prefix\n3. Postfix\n0. Exit\n");
		printf("===============\n");
		printf("Enter choice: ");
		char input[4]; fgets(input, 4, stdin); sscanf(input, "%d", &choice);
		if (choice == 0) {
			return 0;
		} else if (choice > 3 || choice < 0) {
			printf("Incorrect choice!\n");
			continue;
		} else if (choice == 1) {
			char infix[MAX];
			printf("Enter infix expression: ");
			fgets(infix, MAX, stdin);

			char prefix[MAX];
			infixToPrefix(infix, prefix);
			printf("Prefix expression: %s\n", prefix);

			char postfix[MAX];
			infixToPostfix(infix, postfix);
			printf("Postfix expression: %s\n", postfix);
		} else if (choice == 2) {
			char prefix[MAX];
			printf("Enter prefix expression: ");
			fgets(prefix, MAX, stdin);

			char infix[MAX];
			prefixToInfix(prefix, infix);
			printf("Infix expression: %s\n", infix);

			char postfix[MAX];
			prefixToPostfix(prefix, postfix);
			printf("Postfix expression: %s\n", postfix);
		} else if (choice == 3) {
			char postfix[MAX];
			printf("Enter postfix expression: ");
			fgets(postfix, MAX, stdin);

			char infix[MAX];
			postfixToInfix(postfix, infix);
			printf("Infix expression: %s\n", infix);

			char prefix[MAX];
			postfixToPrefix(postfix, prefix);
			printf("Prefix expression: %s\n", prefix);
		}
	}
}

int isFull() {
	return top == MAX - 1;
}

int isEmpty() {
	return top == -1;
}

void push(char element) {
	if (isFull(top)) {
		printf("Stack is full\n");
	} else {
		stack[++top] = element;
	}
}

char pop() {
	if (isEmpty(top)) {
		return -1;
	} else {
		return stack[top--];
	}
}

void spush(char* element) {
	if (isFull(top)) {
		printf("Stack is full\n");
	} else {
		sstack[++top] = element;
	}
}

char* spop() {
	if (isEmpty()) {
		return NULL;
	} else {
		return sstack[top--];
	}
}

void strrev(char str[MAX]) {
	for (int i = 0; str[i] != '\0'; i++) {
		push(str[i]);
	}
	int k = 0;
	while (!isEmpty(top)) {
		str[k++] = pop();
	}
	str[k] = '\0';
}

void infixToPrefix(char infix[MAX], char prefix[MAX]) {
	char exp[MAX];
	strcpy(exp, infix);
	strrev(exp);

	int pc = 0;
	for (int ic = 0; exp[ic] != '\0'; ic++) {
		char token = exp[ic];
		if (token == ' ' || token == '\n') {
			continue;
		} else if (isOperand(token)) {
			prefix[pc++] = token;
		} else if (token == ')') {
			push('(');
		} else if (token == '(') {
			char ch = pop();
			while (ch != '(') {
				prefix[pc++] = ch;
				ch = pop();
			}
		} else {
			while (!isEmpty(top) && isp(stack[top]) > icp(token)) {
				prefix[pc++] = pop();
			}
			push(token);
		}
	}
	while (!isEmpty(top)) {
		prefix[pc++] = pop();
	}

	strrev(prefix);
}

void infixToPostfix(char infix[MAX], char postfix[MAX]) {
	int pc = 0;
	for (int ic = 0; infix[ic] != '\0'; ic++) {
		char token = infix[ic];
		if (token == ' ' || token == '\n') {
			continue;
		} else if (isOperand(token)) {
			postfix[pc++] = token;
		} else if (token == '(') {
			push('(');
		} else if (token == ')') {
			char ch = pop();
			while (ch != '(') {
				postfix[pc++] = ch;
				ch = pop();
			}
		} else {
			while (!isEmpty(top) && isp(stack[top]) >= icp(token)) {
				postfix[pc++] = pop();
			}
			push(token);
		}
	}
	while (!isEmpty(top)) {
		postfix[pc++] = pop();
	}
}

void prefixToInfix(char prefix[MAX], char infix[MAX]) {
	for (int i = strlen(prefix); i >= 0; i--) {
		char token = prefix[i];
		if (isOperand(token)) {
			char* op = calloc(2, sizeof(char));
			op[0] = token;
			spush(op);
		} else if (token == ' ' || token == '\n') {
			continue;
		} else {
			char* operand1 = spop();
			char* operand2 = spop();
			char* res = calloc(MAX, sizeof(char));
			snprintf(res, MAX * sizeof(char), "(%s%c%s)", operand1, token, operand2);
			free(operand1);
			free(operand2);
			spush(res);
		}
	}
	char* exp = spop();
	strcpy(infix, exp);
	free(exp);
}

void postfixToInfix(char postfix[MAX], char infix[MAX]) {
	for (int i = 0; postfix[i] != '\0'; i++) {
		char token = postfix[i];
		if (isOperand(token)) {
			char* op = calloc(2, sizeof(char));
			op[0] = token;
			spush(op);
		} else if (token == ' ' || token == '\n') {
			continue;
		} else {
			char* operand2 = spop();
			char* operand1 = spop();
			char* res = calloc(MAX, sizeof(char));
			snprintf(res, MAX * sizeof(char), "(%s%c%s)", operand1, token, operand2);
			free(operand1);
			free(operand2);
			spush(res);
		}
	}
	char* exp = spop();
	strcpy(infix, exp);
	free(exp);
}

void prefixToPostfix(char prefix[MAX], char postfix[MAX]) {
	for (int i = strlen(prefix); i >= 0; i--) {
		char token = prefix[i];
		if (isOperand(token)) {
			char* op = calloc(2, sizeof(char));
			op[0] = token;
			spush(op);
		} else if (token == ' ' || token == '\n') {
			continue;
		} else {
			char* operand1 = spop();
			char* operand2 = spop();
			char* res = calloc(MAX, sizeof(char));
			snprintf(res, MAX * sizeof(char), "%s%s%c", operand1, operand2, token);
			free(operand1);
			free(operand2);
			spush(res);
		}
	}
	char* exp = spop();
	strcpy(postfix, exp);
	free(exp);
}

void postfixToPrefix(char postfix[MAX], char prefix[MAX]) {
	for (int i = 0; postfix[i] != '\0'; i++) {
		char token = postfix[i];
		if (isOperand(token)) {
			char* op = calloc(2, sizeof(char));
			op[0] = token;
			spush(op);
		} else if (token == ' ' || token == '\n') {
			continue;
		} else {
			char* operand2 = spop();
			char* operand1 = spop();
			char* res = calloc(MAX, sizeof(char));
			snprintf(res, MAX * sizeof(char), "%c%s%s", token, operand1, operand2);
			free(operand1);
			free(operand2);
			spush(res);
		}
	}
	char* exp = spop();
	strcpy(prefix, exp);
	free(exp);
}

int isOperand(char op) {
	return (op >= 'a' && op <= 'z') ||
		(op >= 'A' && op <= 'Z') ||
		(op >= '0' && op <= '9');
}

int isp(char op) {
	switch (op) {
		case '(': return 0;
		case '^': return 3;
		case '*':
		case '/':
		case '%': return 2;
		case '+':
		case '-': return 1;
	}
}

int icp(char op) {
	switch (op) {
		case '(': return 5;
		case '^': return 4;
		case '*':
		case '/':
		case '%': return 2;
		case '+':
		case '-': return 1;
	}
}
