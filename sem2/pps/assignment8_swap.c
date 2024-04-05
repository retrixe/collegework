#include <stdio.h>

void swap(int* a, int* b) {
  int temp = *a;
  *a = *b;
  *b = temp;
  printf("A and B in swap function: %d, %d\n", *a, *b);
}

int main() {
  int a, b;
  printf("Enter a: ");
  scanf("%d", &a);
  printf("Enter b: ");
  scanf("%d", &b);

  printf("A and B before swapping in function: %d, %d\n", a, b);
  swap(&a, &b);
  printf("A and B after swapping in function: %d, %d\n", a, b);

  int temp = b;
  b = a;
  a = temp;
  printf("A and B after swapping w/out function: %d, %d\n", a, b);
  return 0;
}
