#include <stdio.h>

int main() {
  int studentCount;
  printf("Enter number of students: ");
  scanf("%d", &studentCount);
  int subjectCount;
  printf("Enter subject count: ");
  scanf("%d", &subjectCount);

  struct Student {
    int rollNo;
    char name[64];
    int marks[subjectCount];
  };

  struct Student students[studentCount];

  for (int student = 0; student < studentCount; student++) {
    printf("=========================\n");
    printf("Enter details for student %d:\n", student + 1);
    printf("- Roll no: ");
    scanf("%d", &students[student].rollNo);
    printf("- Name: ");
    scanf("%s", students[student].name);
    for (int subject = 0; subject < subjectCount; subject++) {
      printf("- Subject %d: ", subject + 1);
      scanf("%d", &students[student].marks[subject]);
    }
  }

  printf("=========================\n");
  printf("Roll No\tName\t");
  for (int i = 0; i < subjectCount; i++) {
    printf("Subject #%d\t", i + 1);
  }
  printf("Total\tPercentage\tClass\n");
  for (int student = 0; student < studentCount; student++) {
    printf("%d\t", students[student].rollNo); // Roll No
    printf("%s\t", students[student].name); // Name
    int total = 0;
    for (int subject = 0; subject < subjectCount; subject++) {
      printf("%d\t\t", students[student].marks[subject]); // Subject #N
      total += students[student].marks[subject];
    }
    printf("%d\t", total); // Total
    float percentage = total / subjectCount;
    printf("%.2f\t\t", percentage); // Percentage
    if (percentage > 90) {
      printf("First Class");
    } else if (percentage > 70) {
      printf("Second Class");
    } else if (percentage < 40) {
      printf("Fail");
    } else {
      printf("N/A");
    }
    printf("\n");
  }
}
