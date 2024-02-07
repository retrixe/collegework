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

  while (1) {
    printf("==================\n");
    printf("Options:\n");
    printf("1 - Add\n2 - Subtract\n3 - Transpose matrix 1\n4 - Invert matrix 1\n0 - Exit\n");
    printf("Enter option: ");
    int option;
    scanf("%d", &option);
    if (option > 4 || option < 0) {
      printf("ERROR: Invalid option entered!\n");
      continue;
    } else if (option == 0) {
      printf("Exiting...\n");
      return 0;
    }

    if (option == 4) {
      // Invert matrix 1 and store in matrix2
    }

    printf("===== Result =====\n");
    for (int row = 0; row < rows; row++) {
      for (int col = 0; col < cols; col++) {
        if (option == 1)
          printf("%d\t", matrix1[row][col] + matrix2[row][col]);
        if (option == 2)
          printf("%d\t", matrix1[row][col] - matrix2[row][col]);
        if (option == 3)
          printf("%d\t", matrix1[col][row]);
        if (option == 4) {}
// TODO: Perform inversion          printf("%d\t", matrix1[row][col] + matrix2[row][col]);
      }
      printf("\n");
    }
    return 0;
  }
}
