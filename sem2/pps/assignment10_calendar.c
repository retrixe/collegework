#include <stdio.h>

int isLeapYear(int year);

int getDaysInMonth(int year, int month);

int getFirstDay(int year, int month);

char* getMonthName(int month);

void main() {
  int year, month;
  printf("Enter year: ");
  scanf("%d", &year);
  printf("Enter month: ");
  scanf("%d", &month);

  char* monthName = getMonthName(month);
  printf("================= %d - %s =================\n", year, monthName);
  printf("Sun\tMon\tTue\tWed\tThu\tFri\tSat\n");
  int currentDay = 0;
  int daysInMonth = getDaysInMonth(year, month);

  // Leave initial blank spaces until you reach the first day
  int firstDay = getFirstDay(year, month);
  while (currentDay < firstDay) {
    printf(" \t");
    currentDay++;
  }

  // Print month
  for (int day = 1; day <= daysInMonth; day++) {
    printf("%d", day);
    // If on Saturday, go back to Sunday and go to next line
    // Else, leave a gap
    if (currentDay == 6) {
      printf("\n");
      currentDay = 0;
    } else {
      printf("\t");
      currentDay++;
    }
  }
  if (currentDay != 0) {
    printf("\n");
  }
}

int isLeapYear(int year) {
  return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
}

int getDaysInMonth(int year, int month) {
  if (month == 2) {
    if (isLeapYear(year)) {
      return 29;
    } else {
      return 28;
    }
  } else if (month <= 7) {
    if (month % 2 == 0) {
      return 30;
    } else {
      return 31;
    }
  } else {
    if (month % 2 == 0) {
      return 31;
    } else {
      return 30;
    }
  }
}

int getFirstDay(int year, int month) {
  // FIXME Feb - 2020
  // FIXME Feb - 2023
  int currentYear = 2024;
  int currentMonth = 01;
  int firstDay = 1; // Monday
  while (year != currentYear) {
    // Calculate total days in year.
    int totalDays = 0;
    for (int i = 1; i <= 12; i++) {
      totalDays += getDaysInMonth(currentYear, i);
    }
    // Reach closer to desired year.
    int leftoverDays = totalDays % 7;
    if (year < currentYear) {
      firstDay -= leftoverDays;
      if (firstDay < 0) {
        firstDay
      }
      currentYear--;
    } else {
      firstDay = (firstDay + leftoverDays) % 7;
      currentYear++;
    }
  }
  while (month != currentMonth) {
    // Calculate total days in month.
    int totalDays = getDaysInMonth(currentYear, currentMonth);
    int leftoverDays = totalDays % 7;

    firstDay = (firstDay + leftoverDays) % 7;
    currentMonth++;
  }
  return firstDay;
}

char* getMonthName(int month) {
  if (month == 1) return "January";
  if (month == 2) return "February";
  if (month == 3) return "March";
  if (month == 4) return "April";
  if (month == 5) return "May";
  if (month == 6) return "June";
  if (month == 7) return "July";
  if (month == 8) return "August";
  if (month == 9) return "September";
  if (month == 10) return "October";
  if (month == 11) return "November";
  if (month == 12) return "December";
}
