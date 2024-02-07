#include <stdio.h>

int main() {
  int rows, cols;
  printf("Enter number of rows (up to 10): ");
  scanf("%d", &rows);
  printf("Enter number of columns (up to 10): ");
  scanf("%d", &cols);
  int matrix1[rows][cols], matrix2[rows][cols];

  printf("===== Matrix 1 =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("Enter number for row %d, col %d: ", row + 1, col + 1);
      scanf("%d", &matrix1[row][col]);
    }
  }

  printf("===== Matrix 2 =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("Enter number for row %d, col %d: ", row + 1, col + 1);
      scanf("%d", &matrix2[row][col]);
    }
  }

  printf("===== Matrix 1 =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("%d\t", matrix1[row][col]);
    }
    printf("\n");
  }

  printf("===== Matrix 2 =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("%d\t", matrix2[row][col]);
    }
    printf("\n");
  }

  printf("===== Result =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("%d\t", matrix1[row][col] + matrix2[row][col]);
    }
    printf("\n");
  }
  return 0;
}
