#include <stdio.h>

int factorial(int input) {
  if (input == 0) return 1;
  else return input * factorial(input - 1);
}

int main() {
  int input;
  printf("Enter number to factorial: ");
  scanf("%d", &input);
  printf("Factorial: %d\n", factorial(input));
  return 0;
}
