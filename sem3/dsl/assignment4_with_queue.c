#include <stdio.h>

struct Job {
	int pid;
	int exec_time;
};

struct Queue {
	struct Job arr[10];
	int front;
	int rear;
	int size;
};

int enqueue(struct Queue *queue, struct Job job);

struct Job dequeue(struct Queue *queue);

void accept(struct Queue *queue);

void jobsch(struct Queue *queue);

int main() {
	struct Queue queue = {
		.front = -1,
		.rear = -1,
		.size = 10,
	};
	accept(&queue);
	jobsch(&queue);
}

int enqueue(struct Queue *queue, struct Job job) {
	int nextRear = queue->rear + 1;
	if (nextRear == queue->size) {
		return -1;
	}
	queue->rear = nextRear;
	queue->arr[queue->rear] = job;
	return 0;
}

struct Job dequeue(struct Queue *queue) {
	if (queue->front == queue->rear) {
		struct Job empty = {-1,-1};
		return empty;
	} else {
		queue->front++;
		struct Job element = queue->arr[queue->front];
		return element;
	}
}

void accept(struct Queue *queue) {
	printf("Enter number of jobs: ");
	int count;
	scanf("%d", &count);
	for (int i = 1; i <= count; i++) {
		printf("Enter execution time of job %d:\n", i);
		struct Job job = {i, -1};
		scanf("%d", &job.exec_time);
		enqueue(queue, job);
	}
}

void jobsch(struct Queue *queue) {
	printf("PID\tWaitT\tExecT\tTaT\n");
	struct Job job;
	int curr_time = 0;
	while (1) {
		job = dequeue(queue);
		if (job.pid == -1) return;
		int wait_time = curr_time;
		int ta_time = curr_time + job.exec_time;
		printf("%d\t%d\t%d\t%d\n", job.pid, wait_time, job.exec_time, ta_time);
		curr_time += job.exec_time;
	}
}
