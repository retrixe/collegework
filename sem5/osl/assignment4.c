#include <stdio.h>
#include <string.h>

// 5 1 7 2 5 3 1 4 2 5 3

struct Job {
	int pid;
	int exec_time;
	int remaining_time;
	int wait_time;
	int arr_time;
	int ct_time;
	int tat_time;
};

int accept(struct Job queue[10]);

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
		queue[i].remaining_time = queue[i].exec_time;
		queue[i].pid = i;
	}
	return count;
}

void inssort_arrival(struct Job queue[10], int n) {
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

void inssort_remaining(struct Job queue[10], int n) {
	for (int i = 1; i < n; i++) {
		struct Job key = queue[i];
		int j = i - 1;
		while (j >= 0 && queue[j].remaining_time < key.remaining_time) {
			queue[j + 1] = queue[j];
			j--;
		}
		queue[j + 1] = key;
	}
}

void jobsch(struct Job queue[10], int n) {
	inssort_arrival(queue, n);
	struct Job ready_jobs[10];
	int ready_jobs_count = 0;
	struct Job completed_jobs[10];
	int completed_jobs_count = 0;

	int curr_time = 0;
	int last_job_loaded = -1;
	int last_job_executed = -2; // Neither 0 nor -1

	// printf("0 - ");
	while (completed_jobs_count < n) {
		// If there's a job that arrived now, add it to the queue
		if (curr_time == queue[last_job_loaded + 1].arr_time)
			ready_jobs[ready_jobs_count++] = queue[++last_job_loaded];

		// Sort remaining jobs by shortest job last
		inssort_remaining(ready_jobs, ready_jobs_count);

		// Execute shortest job for 1 second
		const int shortest_job_idx = ready_jobs_count - 1;
		if (
			ready_jobs_count > 0 &&
			--ready_jobs[shortest_job_idx].remaining_time == 0
		) {
			// Set job properties
			ready_jobs[shortest_job_idx].ct_time = curr_time + 1;
			ready_jobs[shortest_job_idx].tat_time =
				curr_time + 1 - ready_jobs[shortest_job_idx].arr_time;
			ready_jobs[shortest_job_idx].wait_time =
				ready_jobs[shortest_job_idx].tat_time -
				ready_jobs[shortest_job_idx].exec_time;
			// Add it to completed jobs queue
			completed_jobs[completed_jobs_count++] = ready_jobs[--ready_jobs_count];
		}

		// Print Gantt chart
		if (ready_jobs_count > 0 && last_job_executed != ready_jobs[shortest_job_idx].pid) {
			printf("%d - P%d - ", curr_time, ready_jobs[shortest_job_idx].pid);
		} else if (ready_jobs_count == 0 && last_job_executed != -1) {
			printf("%d - # - ", curr_time);
		}
		last_job_executed = ready_jobs_count > 0 ? ready_jobs[shortest_job_idx].pid : -1;

		// Move to next clock
		curr_time++;
	}
	printf("\n");
	memcpy(queue, completed_jobs, sizeof(completed_jobs));
	inssort_arrival(queue, n);
}

void display(struct Job queue[10], int n) {
	int total_tat_time = 0;
	int total_wait_time = 0;
	printf("====================================\n");
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
		total_tat_time += job.tat_time;
		total_wait_time += job.wait_time;
	}
	printf("Average TaT time: %.2f\nAverage wait time: %.2f\n",
		(float)total_tat_time / (float)n,
		(float)total_wait_time / (float)n);
}
