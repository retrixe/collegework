#include <stdio.h>

int main() {
  int rows, cols, option;
  printf("Enter number of rows (up to 10): ");
  scanf("%d", &rows);
  printf("Enter number of columns (up to 10): ");
  scanf("%d", &cols);
  int matrix1[rows][cols], matrix2[rows][cols];

  while (1) {
    printf("Options:\n");
    printf("1 - Add\n2 - Subtract\n3 - Transpose matrix\n0 - Exit\n");
    printf("Enter option: ");
    scanf("%d", &option);
    if (option > 3 || option < 0) {
      printf("ERROR: Invalid option entered!\n");
      continue;
    } else if (option == 0) {
      printf("Exiting...\n");
      return 0;
    } else {
      break;
    }
  }

  printf("===== Matrix 1 =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("Enter number for row %d, col %d: ", row + 1, col + 1);
      scanf("%d", &matrix1[row][col]);
    }
  }

  if (option == 1 || option == 2) {
    printf("===== Matrix 2 =====\n");
    for (int row = 0; row < rows; row++) {
      for (int col = 0; col < cols; col++) {
        printf("Enter number for row %d, col %d: ", row + 1, col + 1);
        scanf("%d", &matrix2[row][col]);
      }
    }
  }

  printf("===== Matrix 1 =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      printf("%d\t", matrix1[row][col]);
    }
    printf("\n");
  }

  if (option == 1 || option == 2) {
    printf("===== Matrix 2 =====\n");
    for (int row = 0; row < rows; row++) {
      for (int col = 0; col < cols; col++) {
        printf("%d\t", matrix2[row][col]);
      }
      printf("\n");
    }
  }

  printf("===== Result =====\n");
  for (int row = 0; row < rows; row++) {
    for (int col = 0; col < cols; col++) {
      switch (option) {
        case 1:
          printf("%d\t", matrix1[row][col] + matrix2[row][col]);
          break;
        case 2:
          printf("%d\t", matrix1[row][col] - matrix2[row][col]);
          break;
        case 3:
          printf("%d\t", matrix1[col][row]);
          break;
      }
    }
    printf("\n");
  }
  return 0;
}
