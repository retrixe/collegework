#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

void bubbleSort(int numbers[], int count, int desc) {
	for (int pass = 1; pass < count; pass++) {
		for (int index = 0; index < count - pass; index++) {
			if (
				(numbers[index] > numbers[index + 1] && desc) ||
				(numbers[index] < numbers[index + 1] && !desc)
			) {
				int temp = numbers[index];
				numbers[index] = numbers[index + 1];
				numbers[index + 1] = temp;
			}
		}
	}
}

int main() {
	// 10 2 3 9 6 5 7 4 1 8 0
	int count;
	printf("Enter number of elements: ");
	scanf("%d", &count);
	printf("Enter elements: ");
	int numbers[count];
	for (int i = 0; i < count; i++) {
		scanf("%d", &numbers[i]);
	}

	pid_t status = fork();
	if (status == -1) {
		printf("An error occurred!");
		return 1;
	}

	bubbleSort(numbers, 10, status == 0);
	for (int i = 0; i < 10; i++) {
		printf("%d\n", numbers[i]);
	}
	if (status == 0) {
		printf("The parent process ID is %d\n", getppid());
		printf("This is child process ID %d\n", getpid());
	} else {
		printf("This is parent process ID %d\n", getpid());
		printf("The child process ID is %d\n", status);
		wait(NULL);
	}
}
