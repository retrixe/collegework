#include <stdio.h>

int main() {
  printf("Calculator App\n");
  while (1) {
    printf("Options:\n1 - Add\n2 - Subtract\n3 - Multiply\n4 - Divide\n0 - Exit\nEnter option: ");
    int option;
    scanf("%d", &option);
    if (option > 4 || option < 0) {
      printf("ERROR: Invalid option entered!\n");
      continue;
    } else if (option == 0) {
      printf("Exiting...\n");
      return 0;
    }

    float n1, n2;
    printf("Enter number 1: ");
    scanf("%f", &n1);
    printf("Enter number 2: ");
    scanf("%f", &n2);
    printf("==========================\n");
    switch (option) {
      case 1:
      printf("Result: %.2f\n", n1 + n2);
      break;
      case 2:
      printf("Result: %.2f\n", n1 - n2);
      break;
      case 3:
      printf("Result: %.2f\n", n1 * n2);
      break;
      case 4:
      printf("Result: %.2f\n", n1 / n2);
    }
    printf("==========================\n");
  }
  return 0;
}
