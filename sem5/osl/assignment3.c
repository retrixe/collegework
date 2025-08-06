#include <stdio.h>

// 5 0 3 2 6 4 4 6 5 8 2
// 5 1 2 2 6 4 4 6 5 8 2

struct Job {
	int pid;
	int exec_time;
	int wait_time;
	int arr_time;
	int ct_time;
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
		queue[i].ct_time = curr_time;
		queue[i].tat_time = queue[i].ct_time - queue[i].arr_time;
	}
}

void display(struct Job queue[10], int n) {
	printf("PID\tArrT\tWaitT\tExecT\tCmpT\tTaT\n");
	for (int i = 0; i < n; i++) {
		struct Job job = queue[i];
		printf("%d\t%d\t%d\t%d\t%d\t%d\n",
			job.pid,
			job.arr_time,
			job.wait_time,
			job.exec_time,
			job.ct_time,
			job.tat_time);
	}
	printf("====================================\n");
	int last_tick = queue[n - 1].ct_time;
	int current_task = 0;
	printf("0 - ");
	for (int tick = 0; tick < last_tick; tick++) {
		if (tick == queue[current_task].ct_time)
			current_task++;
		/* if (tick < queue[current_task].arr_time)
			printf("%d - #", tick);
		else
			printf("%d - P%d", tick, current_task); */
		if (tick == queue[current_task].arr_time - 1) {
			printf("# - %d - ", queue[current_task].arr_time);
		} else if (tick == queue[current_task].ct_time - 1) {
			printf("P%d - %d - ", current_task, queue[current_task].ct_time);
		}
	}
	printf("\n");
}
