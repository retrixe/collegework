#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
	int pipe_rw[2];
	int success = pipe(pipe_rw);
	if (success < 0) {
		printf("pipe failed\n");
		return -1;
	}

	pid_t forkpid = fork();
	if (forkpid < 0) {
		printf("fork failed\n");
		return -1;
	}

	if (forkpid == 0) {
		// This is the child process
		// Display messages received over pipe
		while (1) {
			char msg[1024];
			const ssize_t size = read(pipe_rw[0], &msg, sizeof(msg));
			if (size < 0) {
				printf("read failed\n");
			} else {
				msg[size] = '\0';
			}

			if (size == 0 || strcmp(msg, "exit\n") == 0) {
				break;
			}
			printf("Received message: %s", msg);
		}
	} else {
		// This is the parent process
		while (1) {
			usleep(10 * 1000);
			printf("Enter message: ");
			char msg[1024];
			fgets(msg, 1024, stdin); // Read entire line
			const ssize_t status = write(pipe_rw[1], msg, strlen(msg));
			if (status < 0) {
				printf("write failed\n");
			} else if (strcmp(msg, "exit\n") == 0) {
				close(pipe_rw[0]);
				close(pipe_rw[1]);
				break;
			}
		}

		// Wait for child to terminate
		int status;
		pid_t waitpid = wait(&status);
		if (forkpid != waitpid) {
			printf("unknown child process terminated\n");
		} else {
			printf("child process terminated with status %d\n", status);
		}
	}
	return 0;
}
