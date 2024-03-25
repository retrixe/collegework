#include <stdio.h>
#include <string.h>

int main() {
  char path1[256], path2[256];
  printf("Enter path 1 to copy from: ");
  scanf("%s", path1); // fgets(path1, 256, stdin);
  printf("Enter path 2 to copy to: ");
  scanf("%s", path2); // fgets(path2, 256, stdin);

  FILE* file1 = fopen(path1, "r");
  FILE* file2 = fopen(path2, "w");
  if (file1 == NULL || file2 == NULL) {
    printf("Failed to open file!\n");
    return 1;
  }
  // Read string
  char buf[64];

  /* while (1) {
    fgets(buf, 64, file1);
    if (feof(file1)) {
      return 0;
    }
    fputs(buf, file2);
  } */
  int bytes_read;
  do {
    bytes_read = fread(buf, 1, 64, file1);
    fwrite(buf, 1, bytes_read, file2);
  } while (bytes_read == 64);

  fclose(file1);
  fclose(file2);
  return 0;
}
