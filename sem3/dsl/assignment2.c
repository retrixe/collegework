#include <stdio.h>

void accept(int matrix[5][5], int rows, int cols);
void displayMatrix(int matrix[5][5], int rows, int cols);
void displaySparse(int matrix[15][3]);
void compact(int matrix[5][5], int rows, int cols, int sparse[15][3]);
void simpleTranspose(int original[15][3], int transpose[15][3]);
void fastTranspose(int original[15][3], int transpose[15][3]);

int main() {
	while (1) {
		int matrix[5][5];
		int rows, cols;

		printf("Enter matrix rows: ");
		scanf("%d", &rows);
		printf("Enter matrix cols: ");
		scanf("%d", &cols);

		if (rows > 10 || cols > 10) {
			printf("Error: Max rows and cols are 10!\n");
			continue;
		}

		accept(matrix, rows, cols);
		printf("Entered matrix:\n");
		displayMatrix(matrix, rows, cols);

		int sparse[15][3];
		compact(matrix, rows, cols, sparse);
		printf("Sparse matrix:\n");
		displaySparse(sparse);

		int transpose1[15][3];
		simpleTranspose(sparse, transpose1);
		printf("Simple transpose:\n");
		displaySparse(transpose1);

		int transpose2[15][3];
		fastTranspose(sparse, transpose2);
		printf("Fast transpose:\n");
		displaySparse(transpose2);
	}
	return 0;
}

void accept(int matrix[5][5], int rows, int cols) {
	for (int row = 0; row < rows; row++) {
		for (int col = 0; col < cols; col++) {
			printf("Enter element at row %d / col %d - ", row, col);
			scanf("%d", &matrix[row][col]);
		}
	}
}

void displayMatrix(int matrix[5][5], int rows, int cols) {
	for (int row = 0; row < rows; row++) {
		for (int col = 0; col < cols; col++) {
			printf("%d ", matrix[row][col]);
		}
		printf("\n");
	}
}

void displaySparse(int matrix[15][3]) {
    int rows = matrix[0][2] + 1, cols = 3;
	for (int row = 0; row < rows; row++) {
		for (int col = 0; col < cols; col++) {
			printf("%d ", matrix[row][col]);
		}
		printf("\n");
	}
}

void compact(int matrix[5][5], int rows, int cols, int sparse[15][3]) {
    int index = 1;
    sparse[0][0] = rows;
    sparse[0][1] = cols;
	for (int row = 0; row < rows; row++) {
		for (int col = 0; col < cols; col++) {
			if (matrix[row][col] != 0) {
				sparse[index][0] = row;
				sparse[index][1] = col;
				sparse[index][2] = matrix[row][col];
				index++;
			}
		}
	}
    sparse[0][2] = index - 1;
}

void simpleTranspose(int original[15][3], int transpose[15][3]) {
	transpose[0][0] = original[0][1];
	transpose[0][1] = original[0][0];
	transpose[0][2] = original[0][2];
	if (transpose[0][2] <= 0) return;

	int index = 1;
	for (int col = 0; col < original[0][1]; col++) {
		for (int row = 1; row <= original[0][2]; row++) {
			if (original[row][1] == col) {
				transpose[index][0] = original[row][1];
				transpose[index][1] = original[row][0];
				transpose[index][2] = original[row][2];
				index++;
			}
		}
	}
}

void fastTranspose(int original[15][3], int transpose[15][3]) {
	transpose[0][0] = original[0][1];
	transpose[0][1] = original[0][0];
	transpose[0][2] = original[0][2];
	if (transpose[0][2] <= 0) return;

	int freq[original[0][1]];
	for (int i = 0; i < original[0][1]; i++) {
		freq[i] = 0;
	}

	for (int row = 1; row <= original[0][2]; row++) {
		freq[original[row][1]]++;
	}
	int locs[original[0][1]];
	locs[0] = 1;
	for (int col = 1; col < original[0][1]; col++) {
		locs[col] = locs[col - 1] + freq[col - 1];
	}

	for (int row = 1; row <= original[0][2]; row++) {
		int col = original[row][1];
		transpose[locs[col]][0] = col;
		transpose[locs[col]][1] = original[row][0];
		transpose[locs[col]][2] = original[row][2];
		locs[col]++;
	}
}
