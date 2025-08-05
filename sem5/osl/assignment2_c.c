#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
	pid_t status = fork();
	if (status == -1) {
		printf("An error occurred!");
		return 1;
	}

	if (status == 0) {
		printf("The parent process ID is %d\n", getppid());
		printf("This is child process ID %d\n", getpid());
	} else {
		sleep(10);
		printf("This is parent process ID %d\n", getpid());
		printf("The child process ID is %d\n", status);
	}
}
