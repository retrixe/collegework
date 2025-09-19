#include <stdio.h>
#include <stdbool.h>

#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int num_processes, num_resources;
int available[MAX_RESOURCES];
int maximum[MAX_PROCESSES][MAX_RESOURCES];
int allocation[MAX_PROCESSES][MAX_RESOURCES];
int need[MAX_PROCESSES][MAX_RESOURCES];
int finish[MAX_PROCESSES];
int work[MAX_RESOURCES];

bool is_safe() {
    int safe_sequence[MAX_PROCESSES];
    int count = 0;

    for (int i = 0; i < num_resources; i++) {
        work[i] = available[i];
    }

    for (int i = 0; i < num_processes; i++) {
        finish[i] = false;
    }

    while (count < num_processes) {
        bool found = false;
        for (int i = 0; i < num_processes; i++) {
            if (finish[i] == false) {
                int can_finish = true;
                for (int j = 0; j < num_resources; j++) {
                    if (need[i][j] > work[j]) {
                        can_finish = false;
                        break;
                    }
                }
                if (can_finish) {
                    for (int k = 0; k < num_resources; k++) {
                        work[k] += allocation[i][k];
                    }
                    safe_sequence[count] = i;
                    finish[i] = true;
                    found = true;
                    count++;
                }
            }
        }
        if (found == false) {
            return false;
        }
    }

    printf("System is in a safe state, can execute in order: ");
    for (int i = 0; i < num_processes; i++) {
        printf("P%d", safe_sequence[i]);
        if (i < num_processes - 1) {
            printf(" -> ");
        }
    }
    printf("\n");

    return true;
}

void request_resources(int process_id, int request[]) {
    for (int i = 0; i < num_resources; i++) {
        if (request[i] > need[process_id][i]) {
            printf("Process P%d exceeded its max need\n", process_id);
            return;
        } else if (request[i] > available[i]) {
            printf("Resources are not available for process P%d\n", process_id);
            return;
        }
    }

    for (int i = 0; i < num_resources; i++) {
        available[i] -= request[i];
        allocation[process_id][i] += request[i];
        need[process_id][i] -= request[i];
   }

    if (is_safe()) {
        printf("Resources allocated to P%d successfully\n", process_id);
    } else {
        printf("Unsafe state when P%d requested resources\n", process_id);
    }
}

int main() {
    printf("Enter number of processes: ");
    scanf("%d", &num_processes);

    printf("Enter number of resources: ");
    scanf("%d", &num_resources);

    printf("Enter available resources: ");
    for (int i = 0; i < num_resources; i++) {
        scanf("%d", &available[i]);
    }

    printf("Enter maximum resource matrix:\n");
    for (int i = 0; i < num_processes; i++) {
        for (int j = 0; j < num_resources; j++) {
            scanf("%d", &maximum[i][j]);
        }
    }

    printf("Enter allocation matrix:\n");
    for (int i = 0; i < num_processes; i++) {
        for (int j = 0; j < num_resources; j++) {
            scanf("%d", &allocation[i][j]);
        }
    }

    for (int i = 0; i < num_processes; i++) {
        for (int j = 0; j < num_resources; j++) {
            need[i][j] = maximum[i][j] - allocation[i][j];
        }
    }

    printf("\n");
    is_safe();

    int process_id;
    int request[MAX_RESOURCES];
    printf("Enter process ID to request resources for (0 to %d): ", num_processes - 1);
    scanf("%d", &process_id);
    printf("Enter resource request for P%d: ", process_id);
    for (int i = 0; i < num_resources; i++) {
        scanf("%d", &request[i]);
    }

    request_resources(process_id, request);

    return 0;
}
