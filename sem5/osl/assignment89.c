#include <stdio.h>

#define FRAME_SIZE 4

void fifo(int pages[], int n) {
  int frames[FRAME_SIZE];
  int page_faults = 0;
  int index = 0;

  for (int i = 0; i < FRAME_SIZE; i++)
    frames[i] = -1;

  printf("\nFIFO page replacement:\n");
  for (int i = 0; i < n; i++) {
    int page = pages[i];
    int found = 0;

    for (int j = 0; j < FRAME_SIZE; j++) {
      if (frames[j] == page) {
        found = 1;
        break;
      }
    }

    if (!found) {
      frames[index] = page;
      index = (index + 1) % FRAME_SIZE;
      page_faults++;
    }

    printf("Page %d -> Frames: ", page);
    for (int k = 0; k < FRAME_SIZE; k++) {
      if (frames[k] != -1)
        printf("%d ", frames[k]);
      else
        printf("- ");
    }
    printf("\n");
  }

  printf("Total page faults = %d\n", page_faults);
}

void lru(int pages[], int n) {
  int frames[FRAME_SIZE];
  int usage[FRAME_SIZE];
  int page_faults = 0;

  for (int i = 0; i < FRAME_SIZE; i++) {
    frames[i] = -1;
    usage[i] = -1;
  }

  printf("\nLRU page replacement:\n");
  for (int i = 0; i < n; i++) {
    int page = pages[i];
    int found = 0;

    for (int j = 0; j < FRAME_SIZE; j++) {
      if (frames[j] == page) {
        found = 1;
        usage[j] = i;
        break;
      }
    }

    if (!found) {
      int lru_index = 0;
      int min_usage = usage[0];
      for (int j = 1; j < FRAME_SIZE; j++) {
        if (usage[j] < min_usage) {
          min_usage = usage[j];
          lru_index = j;
        }
      }

      frames[lru_index] = page;
      usage[lru_index] = i;
      page_faults++;
    }

    printf("Page %d -> Frames: ", page);
    for (int k = 0; k < FRAME_SIZE; k++) {
      if (frames[k] != -1)
        printf("%d ", frames[k]);
      else
        printf("- ");
    }
    printf("\n");
  }

  printf("Total page faults = %d\n", page_faults);
}

int main() {
  int n, choice;

  printf("Enter number of pages: ");
  scanf("%d", & n);

  int pages[n];
  printf("Enter page reference string: ");
  for (int i = 0; i < n; i++)
    scanf("%d", & pages[i]);

  printf("Select page replacement algorithm:\n");
  printf("1. FIFO\n");
  printf("2. LRU\n");
  printf("Enter your choice: ");
  scanf("%d", & choice);

  switch (choice) {
  case 1:
    fifo(pages, n);
    break;
  case 2:
    lru(pages, n);
    break;
  default:
    printf("Invalid choice!\n");
  }

  return 0;
}
