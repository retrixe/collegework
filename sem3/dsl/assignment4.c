#include <stdio.h>

struct Job {
	int pid;
	int exec_time;
	int wait_time;
	int arr_time;
	int tat_time;
};

int accept(struct Job queue[10]);

void inssort(struct Job queue[10], int n);

void jobsch(struct Job queue[10], int n);

void display(struct Job queue[10], int n);

int main() {
	struct Job queue[10];
	int n = accept(queue);
	jobsch(queue, n);
	display(queue, n);
}

int accept(struct Job queue[10]) {
	printf("Enter number of jobs: ");
	int count;
	scanf("%d", &count);
	for (int i = 0; i < count; i++) {
		printf("Enter arrival and execution time of job %d:\n", i + 1);
		scanf("%d %d", &queue[i].arr_time, &queue[i].exec_time);
		queue[i].pid = i;
	}
	return count;
}

void inssort(struct Job queue[10], int n) {
	for (int i = 1; i < n; i++) {
		struct Job key = queue[i];
		int j = i - 1;
		while (j >= 0 && queue[j].arr_time > key.arr_time) {
			queue[j + 1] = queue[j];
			j--;
		}
		queue[j + 1] = key;
	}
}

void jobsch(struct Job queue[10], int n) {
	inssort(queue, n);
	int curr_time = 0;
	for (int i = 0; i < n; i++) {
		if (queue[i].arr_time > curr_time) {
			curr_time = queue[i].arr_time;
		}
		queue[i].wait_time = curr_time;
		curr_time += queue[i].exec_time;
		queue[i].tat_time = curr_time;
	}
}

void display(struct Job queue[10], int n) {
	printf("PID\tArrT\tWaitT\tExecT\tTaT\n");
	for (int i = 0; i < n; i++) {
		struct Job job = queue[i];
		printf("%d\t%d\t%d\t%d\t%d\n",
			job.pid,
			job.arr_time,
			job.wait_time,
			job.exec_time,
			job.tat_time);
	}
}
