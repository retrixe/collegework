#include <stdio.h>

int main() {
  printf("Enter year: ");
  int year;
  scanf("%d", &year);
  int isLeapYear = year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
  printf("Is leap year: %s\n", isLeapYear ? "Yes" : "No");
}
