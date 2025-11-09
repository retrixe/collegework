#include <stdio.h>
#include <stdbool.h>

// Define the number of processes and resources
#define P 5 // Number of processes
#define R 3 // Number of resource types

// Function to calculate the Need matrix
void calculateNeed(int need[P][R], int max[P][R], int alloc[P][R]) {
    for (int i = 0; i < P; i++) {
        for (int j = 0; j < R; j++) {
            // Need = Max - Allocation
            need[i][j] = max[i][j] - alloc[i][j];
        }
    }
}

// Function to check if the system is in a safe state
bool isSafe(int processes[], int avail[], int max[][R], int alloc[][R], int need[][R]) {
    int work[R];
    // Initialize Work = Available
    for (int i = 0; i < R; i++) {
        work[i] = avail[i];
    }

    bool finish[P] = {0}; // Initialize all processes as unfinished
    int safeSeq[P];       // Array to store the safe sequence
    int count = 0;        // Count of finished processes

    // Loop until all processes are finished or no safe sequence is found
    while (count < P) {
        bool found = false; // Flag to check if a process was found in this iteration
        for (int p = 0; p < P; p++) {
            // Find a process 'p' which is not finished
            if (finish[p] == false) {
                // Check if Need[p] <= Work
                int j;
                for (j = 0; j < R; j++) {
                    if (need[p][j] > work[j])
                        break; // This process needs more resources than available
                }

                // If all resources for process 'p' are <= work
                if (j == R) {
                    // This process can finish.
                    // Add its allocated resources back to Work
                    for (int k = 0; k < R; k++) {
                        work[k] += alloc[p][k];
                    }

                    // Add process 'p' to the safe sequence
                    safeSeq[count++] = p;

                    // Mark this process as finished
                    finish[p] = true;
                    found = true;
                }
            }
        }

        // If no process was found in a full iteration, the system is in an unsafe state
        if (found == false) {
            printf("System is in an UNSAFE state.\n");
            return false;
        }
    }

    // If we reach here, the system is in a safe state
    printf("System is in a SAFE state.\nSafe sequence is: ");
    for (int i = 0; i < P; i++) {
        printf("P%d", safeSeq[i]);
        if (i < P - 1) {
            printf(" -> ");
        }
    }
    printf("\n");
    return true;
}

// Function to handle a resource request from a process
void resourceRequest(int p_num, int request[], int processes[], int avail[], int max[][R], int alloc[][R], int need[][R]) {
    
    printf("\n--- Processing Request from P%d for [", p_num);
    for(int j=0; j<R; j++) printf("%d ", request[j]);
    printf("] ---\n");

    // 1. Check if Request[i] <= Need[i]
    for (int j = 0; j < R; j++) {
        if (request[j] > need[p_num][j]) {
            printf("Error: Process P%d has exceeded its maximum claim.\n", p_num);
            printf("Request DENIED.\n");
            return;
        }
    }

    // 2. Check if Request[i] <= Available
    for (int j = 0; j < R; j++) {
        if (request[j] > avail[j]) {
            printf("Error: Resources not available. Process P%d must wait.\n", p_num);
            printf("Request DENIED.\n");
            return;
        }
    }

    // 3. Pretend to allocate the resources
    for (int j = 0; j < R; j++) {
        avail[j] -= request[j];
        alloc[p_num][j] += request[j];
        need[p_num][j] -= request[j];
    }

    // 4. Run the safety algorithm to check if this new state is safe
    if (isSafe(processes, avail, max, alloc, need)) {
        // If safe, the allocation is permanent
        printf("Request for P%d GRANTED.\n", p_num);
    } else {
        // If unsafe, roll back the changes
        printf("Request for P%d DENIED (leads to unsafe state). Rolling back.\n", p_num);
        for (int j = 0; j < R; j++) {
            avail[j] += request[j];
            alloc[p_num][j] -= request[j];
            need[p_num][j] += request[j];
        }
    }
}

// Helper function to print the current state
void printState(int avail[], int max[][R], int alloc[][R], int need[][R]) {
    printf("\nCurrent System State:\n");
    printf("   Allocation     Max       Need\n");
    printf("   A  B  C      A  B  C    A  B  C\n");
    for (int i = 0; i < P; i++) {
        printf("P%d ", i);
        // Allocation
        for (int j = 0; j < R; j++) printf("%-2d ", alloc[i][j]);
        printf("    ");
        // Max
        for (int j = 0; j < R; j++) printf("%-2d ", max[i][j]);
        printf("    ");
        // Need
        for (int j = 0; j < R; j++) printf("%-2d ", need[i][j]);
        printf("\n");
    }
    printf("\nAvailable Resources: [A=%d, B=%d, C=%d]\n", avail[0], avail[1], avail[2]);
}

// Main driver function
int main() {
    // P0, P1, P2, P3, P4
    int processes[] = {0, 1, 2, 3, 4};

    // Available instances of resources (A, B, C)
    int avail[] = {3, 3, 2};

    // Maximum resource needs for each process
    int max[P][R] = {
        {7, 5, 3}, // P0
        {3, 2, 2}, // P1
        {9, 0, 2}, // P2
        {2, 2, 2}, // P3
        {4, 3, 3}  // P4
    };

    // Resources currently allocated to each process
    int alloc[P][R] = {
        {0, 1, 0}, // P0
        {2, 0, 0}, // P1
        {3, 0, 2}, // P2
        {2, 1, 1}, // P3
        {0, 0, 2}  // P4
    };

    // Need matrix
    int need[P][R];

    // Calculate the initial Need matrix
    calculateNeed(need, max, alloc);

    // Print the initial state
    printState(avail, max, alloc, need);

    // Check if the initial state is safe
    printf("\n--- Checking Initial State ---\n");
    isSafe(processes, avail, max, alloc, need);

    // --- Request 1: P1 requests (1, 0, 2) ---
    // This should be GRANTED
    int req1[] = {1, 0, 2};
    resourceRequest(1, req1, processes, avail, max, alloc, need);
    printState(avail, max, alloc, need); // Print state after successful request

    // --- Request 2: P4 requests (3, 3, 0) ---
    // This should be DENIED (Request > Available)
    int req2[] = {3, 3, 0};
    resourceRequest(4, req2, processes, avail, max, alloc, need);
    printState(avail, max, alloc, need); // State should be unchanged

    // --- Request 3: P0 requests (0, 2, 0) ---
    // This should be DENIED (Leads to an unsafe state)
    int req3[] = {0, 2, 0};
    resourceRequest(0, req3, processes, avail, max, alloc, need);
    printState(avail, max, alloc, need); // State should be unchanged

    // --- Request 4: P3 requests (0, 1, 0) ---
    // This should be GRANTED
    int req4[] = {0, 1, 0};
    resourceRequest(3, req4, processes, avail, max, alloc, need);
    printState(avail, max, alloc, need); // State should update

    return 0;
}
