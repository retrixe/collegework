#include <stdio.h>
#include <string.h>

int main() {
  int option;
  while (1) {
    printf("Options:\n");
    printf("1 - Show string length\n");
    printf("2 - Copy string\n");
    printf("3 - Concatenate 2 strings\n");
    printf("4 - Compare 2 strings\n");
    printf("0 - Exit\n");
    printf("Enter option: ");
    scanf("%d", &option);

    char str1[256], str2[128];
    switch (option) {
      case 0:
        return 0;
      case 1:
        printf("Enter string: ");
        scanf("%s", &str1);
        int length = strlen(str1);
        printf("String length: %d\n", length);
        break;
      case 2:
        printf("Enter string: ");
        scanf("%s", &str1);
        strcpy(str2, str1);
        printf("Copied string: %s\n", str2);
        break;
      case 3:
        printf("Enter string 1: ");
        scanf("%s", &str1);
        printf("Enter string 2: ");
        scanf("%s", &str2);
        strcat(str1, str2);
        printf("Concatenated string: %s\n", str1);
        break;
      case 4:
        printf("Enter string 1: ");
        scanf("%s", &str1);
        printf("Enter string 2: ");
        scanf("%s", &str2);
        int cmp = strcmp(str1, str2);
        if (cmp == 0) {
          printf("Both strings are equal!\n");
        } else {
          printf("Both strings are unequal.\n");
        }
        break;
      default:
        printf("Invalid option!\n==================\n");
        continue;
    }
    break;
  }
  return 0;
}
