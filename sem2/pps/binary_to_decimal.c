#include <stdio.h>

int powInt(int num, int exponent) {
  if (exponent == 0)
    return 1;
  int sum = num;
  while (exponent != 1) {
    sum *= num;
    exponent -= 1;
  }
  return sum;
}

int main() {
  printf("Enter number to convert to decimal: ");
  int number;
  scanf("%d", &number);

  int power = 0;
  int output = 0;
  while (number != 0) {
    // remove last digit
    int lastdigit = number % 10;
    number /= 10;
    // add last digit to decimal
    output += lastdigit * powInt(2, power);
    // increase power
    power += 1;
  }
  printf("%d\n", output);
}
