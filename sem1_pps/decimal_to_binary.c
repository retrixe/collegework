#include <stdio.h>

int main() {
  printf("Enter number to convert to binary: ");
  int number;
  scanf("%d", &number);

  // repeatedly divide by 2 and add to a number
  int power = 1;
  int output = 0;
  while (number != 0) {
    // get remainder
    int modulo = number % 2;
    // divide number by 2 and store it
    number /= 2;
    // add the bit to the start of the binary representation
    output += modulo * power;
    // increase power by 10 so the next bit is placed 1 digit above
    power *= 10;
  }
  printf("%d\n", output);
}
