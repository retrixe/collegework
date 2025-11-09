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
        int request[MAX_PROCESSES];
        int requested;
        printf("Make a request at time %d? (0: No, 1: Yes) ", count);
        scanf("%d", &requested);
        if (requested == 1) {
            printf("Enter process ID to request resources for (0 to %d): ", num_processes - 1);
            scanf("%d", &requested);
            printf("Enter resource request for P%d: ", requested);
            for (int i = 0; i < num_resources; i++) {
                scanf("%d", &request[i]);
                work[i] -= request[i];
            }
        } else if (requested == 0) {
            requested = -1;
        }

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
                    if (requested >= 0) {
                        printf("Processed request successfully!\n");
                    }
                    for (int j = 0; j < num_resources; j++) {
                        work[j] += allocation[i][j] + (requested >= 0 ? request[j] : 0);
                    }
                    safe_sequence[count] = i;
                    finish[i] = true;
                    found = true;
                    count++;
                }
            }
        }

        if (found == false && requested >= 0) {
            for (int i = 0; i < num_resources; i++) {
                work[i] += request[i];
            }
            printf("Could not process request.\n");
        } else if (found == false) {
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

    return 0;
}
