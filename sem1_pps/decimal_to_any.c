#include <stdio.h>

// repeatedly divide by base and add to the start of a number
int convertToLowerBase(int number, int base) {
  int power = 1;
  int output = 0;
  while (number != 0) {
    // get remainder
    int modulo = number % base;
    // divide number by base and store it
    number /= base;
    // add the bit to the start of the binary representation
    output += modulo * power;
    // increase power by 10 so the next bit is placed 1 digit above
    power *= 10;
  }
  return output;
}

int main() {
  printf("Enter number to convert: ");
  int number;
  scanf("%d", &number);

  while (1) {
    printf("Choices:\n");
    printf("1) Decimal to binary\n");
    printf("2) Decimal to octal\n");
    printf("3) Decimal to hexadecimal\n");
    printf("Select choice: ");
    int choice;
    scanf("%d", &choice);

    switch (choice) {
      case 1:
        printf("Binary representation: %d\n", convertToLowerBase(number, 2));
        return 0;
      case 2:
        printf("Octal representation: %d\n", convertToLowerBase(number, 8));
        return 0;
      case 3:
        int base = 16;
        char output[10];
        int position = 0;
        while (number != 0) {
          // get remainder
          int modulo = number % base;
          // divide number by base and store it
          number /= base;
          // add to current position, then increase position
          if (modulo >= 10) {
            output[position++] = 'F' - 15 + modulo; // 55 + modulo;
          } else {
            output[position++] = '0' + modulo;
          }
        }
        printf("Hexadecimal representation: ");
        for (int i = 9; i >= 0; i--) printf("%c", output[i]);
        printf("\n");
        return 0;
      default:
        printf("Invalid choice!");
    }
  }
  return 1;
}
