#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Student {
  int  rollNo;
  char name[32];
  int  marks;
};

void acceptStudents(struct Student students[], int count);

void printStudents(struct Student students[], int count);

void bubbleSort(struct Student students[], int count);

void selectionSort(struct Student students[], int count);

void insertionSort(struct Student students[], int count);

void shellSort(struct Student students[], int count);

int main() {
  while (1) {
    int studentCount;
    printf("Enter no of students: ");
    scanf("%d", &studentCount);
    struct Student students[studentCount];
    acceptStudents(students, studentCount);

    printf("==========================\nEntered student data:\n==========================\n");
    printStudents(students, studentCount);

    printf("Sort methods:\n");
    printf("1) Selection sort\n2) Insertion sort\n3) Bubble sort\n4) Shell sort\n0) Exit\n");
    printf("Select method: ");
    int sortMethod;
    scanf("%d", &sortMethod);
    switch (sortMethod) {
      case 0: exit(0); break;
      case 1: selectionSort(students, studentCount); break;
      case 2: insertionSort(students, studentCount); break;
      case 3: bubbleSort(students, studentCount); break;
      case 4: shellSort(students, studentCount); break;
      default: printf("Invalid option!\n"); continue;
    }

    printf("==========================\nSorted student data:\n==========================\n");
    printStudents(students, studentCount);
  }
}

void acceptStudents(struct Student students[], int count) {
  for (int i = 0; i < count; i++) {
    printf("Accepting value for student %d:\n", i + 1);
    // scanf("%d %s %d", &students[i].rollNo, students[i].name, &students[i].marks);
    /* printf("- Enter roll no: ");
    scanf("%d", &students[i].rollNo);
    printf("- Enter name: ");
    scanf("%s", students[i].name);
    printf("- Enter marks: ");
    scanf("%d", &students[i].marks); */
  }
  students[0].rollNo = 7;
  strcpy(students[0].name, "A");
  students[0].marks = 23;

  students[1].rollNo = 12;
  strcpy(students[1].name, "B");
  students[1].marks = 43;

  students[2].rollNo = 2;
  strcpy(students[2].name, "C");
  students[2].marks = 83;

  students[3].rollNo = 5;
  strcpy(students[3].name, "D");
  students[3].marks = 46;

  students[4].rollNo = 28;
  strcpy(students[4].name, "E");
  students[4].marks = 59;
}

void printStudents(struct Student students[], int count) {
  printf("Roll no\tName\tMarks\n");
  for (int i = 0; i < count; i++) {
    printf("%d\t%s\t%d\n", students[i].rollNo, students[i].name, students[i].marks);
  }
}

void bubbleSort(struct Student students[], int count) {
  for (int pass = 1; pass < count; pass++) {

    int comparisons = 0;
    int swaps = 0;

    for (int index = 0; index < count - pass; index++) {
      comparisons++;
      if (students[index].rollNo > students[index + 1].rollNo) {
        swaps++;
        struct Student temp = students[index];
        students[index] = students[index + 1];
        students[index + 1] = temp;
      }
    }

    printf("Result of pass %d:\n- Comparisons: %d\n- Swaps: %d\n", pass, comparisons, swaps);
    printStudents(students, count);
  }
}

void selectionSort(struct Student students[], int count) {
  for (int pass = 0; pass < count - 1; pass++) {

    int comparisons = 0;
    int swaps = 0;

    int minIndex = pass;
    for (int index = pass + 1; index < count; index++) {
      comparisons++;
      if (students[index].rollNo < students[minIndex].rollNo) {
        minIndex = index;
      }
    }

    if (minIndex != pass) {
        swaps++;
        struct Student temp = students[minIndex];
        students[minIndex] = students[pass];
        students[pass] = temp;
    }

    printf("Result of pass %d:\n- Comparisons: %d\n- Swaps: %d\n", pass, comparisons, swaps);
    printStudents(students, count);
  }
}

void insertionSort(struct Student students[], int count) {
  for (int pass = 1; pass < count; pass++) {
    int swaps = 0;

    struct Student current = students[pass];
    int index = pass - 1;
    while (index >= 0 && students[index].rollNo > current.rollNo) {
      students[index + 1] = students[index];
      index--;
      swaps++;
    }
    students[index + 1] = current;

    printf("Result of pass %d:\n- Comparisons: %d\n- Swaps: %d\n", pass, swaps + 1, swaps);
    printStudents(students, count);
  }
}

void shellSort(struct Student students[], int count) {
  int gap = count / 2;
  int passes = 0;

  while (gap != 0) {
    passes++;
    int comparisons = 0;
    int swaps = 0;

    int swapped = 0;
    do {
      swaps += swapped;
      swapped = 0;
      for (int i = 0; i < count - gap; i++) {
        comparisons++;
        if (students[i].rollNo > students[i + gap].rollNo) {
          int temp = students[i].rollNo;
          students[i].rollNo = students[i + gap].rollNo;
          students[i + gap].rollNo = temp;
          swapped++;
        }
      }
    } while (swapped != 0);
    gap = gap / 2;

    printf("Result of pass %d:\n- Comparisons: %d\n- Swaps: %d\n", passes, comparisons, swaps);
    printStudents(students, count);
  }
}
