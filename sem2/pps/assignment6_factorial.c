#include <stdio.h>

int recursiveFactorial(int num) {
  if (num == 0) {
    return 1;
  }
  return num * recursiveFactorial(num - 1);
}

int proceduralFactorial(int num) {
  int result = 1;
  for (int i = 1; i <= num; i++) {
    result *= i;
  }
  return result;
}

int main() {
  printf("Enter number to calculate factorial of: ");
  int num;
  scanf("%d", &num);
  printf("Factorial via recursion: %d\n", recursiveFactorial(num));
  printf("Factorial via loop: %d\n", proceduralFactorial(num));
}
