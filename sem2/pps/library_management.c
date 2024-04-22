#include <stdio.h>
#include <string.h>

// Design a program that simulates a simple library management system using
// structures and file handling to store book information and perform operations like
// adding, searching, and borrowing books.

// Structure to store book information
struct Book
{
  char title[256];
  char author[256];
  int year;
  char genre[256];
  int copies;
  int borrowed;
};

struct Book readBookFromLine(char line[1024])
{
  struct Book book = {.title = "", .author = "", .year = 0, .genre = "", .copies = 0};
  char *title = strsep(&line, ",");
  strcpy(book.title, title);
  char *author = strsep(&line, ",");
  strcpy(book.author, author);
  char *year = strsep(&line, ",");
  sscanf(year, "%d", &book.year);
  char *genre = strsep(&line, ",");
  strcpy(book.genre, genre);
  char *copies = strsep(&line, ",");
  sscanf(copies, "%d", &book.copies);
  char *borrowed = strsep(&line, ",");
  sscanf(borrowed, "%d", &book.borrowed);
  return book;
}

void writeAllBooks(struct Book books[1024], int bookCount)
{
  FILE *libraryFile = fopen("library.txt", "w");
  if (libraryFile == NULL)
  {
    printf("Failed to open file!\n");
  }
  for (int i = 0; i < bookCount; i++)
  {
    struct Book book = books[i];
    fprintf(libraryFile, "%s,%s,%d,%s,%d,%d\n",
      book.title, book.author, book.year,
      book.genre, book.copies, book.borrowed);
  }
  fclose(libraryFile);
}

int main()
{
  printf("Library Management System\n");
  FILE *libraryFile = fopen("library.txt", "r");
  if (libraryFile == NULL)
  {
    printf("Failed to open file!\n");
    return 1;
  }

  struct Book books[1024];
  int booksCount = 0;
  while (!feof(libraryFile))
  {
    char buf[1024];
    fgets(buf, 1024, libraryFile);
    if (feof(libraryFile))
      break;
    if (strcmp(buf, "\n") == 0) // Skip empty lines
      continue;
    books[booksCount] = readBookFromLine(buf);
    booksCount++;
  }
  fclose(libraryFile);

  while (1)
  {
    printf("======== Options ========\n");
    printf("1) Add a book\n");
    printf("2) Search for a book\n");
    printf("3) Borrow a book\n");
    printf("4) Return a book\n");
    printf("5) Show all books\n");
    printf("6) Edit book copies count\n");
    printf("7) Remove a book\n");
    printf("0) Exit\n");
    printf("Select option: ");
    int option;
    scanf("%d", &option);
    switch (option)
    {
    case 1:
      struct Book book = {.borrowed = 0}; // Initially, borrowers are nil
      getchar(); // Remove newline character from scanf

      printf("Enter book title: ");
      fgets(book.title, 256, stdin);
      book.title[strcspn(book.title, "\n")] = 0;

      printf("Enter book author: ");
      fgets(book.author, 256, stdin);
      book.author[strcspn(book.author, "\n")] = 0;

      printf("Enter book publishing year: ");
      char year[16];
      fgets(year, 16, stdin);
      sscanf(year, "%d", &book.year);

      printf("Enter book genre: ");
      fgets(book.genre, 256, stdin);
      book.genre[strcspn(book.genre, "\n")] = 0;

      printf("Enter number of copies: ");
      char copies[16];
      fgets(copies, 16, stdin);
      sscanf(copies, "%d", &book.copies);

      // Append to end of file
      libraryFile = fopen("library.txt", "a");
      if (libraryFile == NULL)
      {
        printf("Failed to open file!\n");
        return 1;
      }
      fprintf(libraryFile, "%s,%s,%d,%s,%d,%d\n",
        book.title, book.author, book.year,
        book.genre, book.copies, book.borrowed);
      fclose(libraryFile);

      // Add to books struct and increase count
      books[booksCount] = book;
      printf("Successfully added book at index %d\n", ++booksCount);
      break;
    case 2:
      int searchResults[1024];
      int searchResultsCount = 0;
      printf("Enter search query: ");
      char query[256];
      getchar(); // Remove newline character from scanf
      fgets(query, 256, stdin);
      query[strcspn(query, "\n")] = 0;
      for (int i = 0; i < booksCount; i++)
      {
        if (strstr(books[i].title, query) != NULL ||
            strstr(books[i].author, query) != NULL ||
            strstr(books[i].genre, query) != NULL)
        {
          searchResults[searchResultsCount++] = i;
        }
      }
      if (searchResultsCount == 0)
      {
        printf("No results found!\n");
        break;
      }
      printf("=======================================\n");
      for (int i = 0; i < searchResultsCount; i++)
      {
        printf("- Book #%d:\n  %s (%d), by %s\n  Genre: %s\n  Copies: %d, Borrowed: %d\n",
          searchResults[i] + 1,
          books[searchResults[i]].title,
          books[searchResults[i]].year,
          books[searchResults[i]].author,
          books[searchResults[i]].genre,
          books[searchResults[i]].copies,
          books[searchResults[i]].borrowed);
      }
      printf("=======================================\n");
      break;
    case 3:
      int borrowIndex;
      printf("Enter book index to borrow: ");
      scanf("%d", &borrowIndex);
      if (borrowIndex < 1 || borrowIndex > booksCount)
      {
        printf("Invalid book index!\n");
        break;
      }
      if (books[borrowIndex - 1].borrowed == books[borrowIndex - 1].copies)
      {
        printf("All copies are borrowed!\n");
        break;
      }
      books[borrowIndex - 1].borrowed++;
      writeAllBooks(books, booksCount);
      printf("Successfully borrowed \"%s\"!\n", books[borrowIndex - 1].title);
      break;
    case 4:
      int returnIndex;
      printf("Enter book index to return: ");
      scanf("%d", &returnIndex);
      if (returnIndex < 1 || returnIndex > booksCount)
      {
        printf("Invalid book index!\n");
        break;
      }
      if (books[returnIndex - 1].borrowed == 0)
      {
        printf("No copies are borrowed!\n");
        break;
      }
      books[returnIndex - 1].borrowed--;
      writeAllBooks(books, booksCount);
      printf("Successfully returned \"%s\"!\n", books[returnIndex - 1].title);
      break;
    case 5:
      for (int i = 0; i < booksCount; i++)
      {
        printf("- Book #%d:\n  %s (%d), by %s\n  Genre: %s\n  Copies: %d, Borrowed: %d\n",
          i + 1,
          books[i].title, books[i].year,
          books[i].author, books[i].genre,
          books[i].copies, books[i].borrowed);
      }
      break;
    case 6:
      int editIndex;
      printf("Enter book index to edit copies of: ");
      scanf("%d", &editIndex);
      if (editIndex < 1 || editIndex > booksCount)
      {
        printf("Invalid book index!\n");
        break;
      }
      printf("Enter new number of copies: ");
      scanf("%d", &books[editIndex - 1].copies);
      writeAllBooks(books, booksCount);
      printf("Successfully updated copies for \"%s\"!\n", books[borrowIndex - 1].title);
      break;
    case 7:
      int removeIndex;
      printf("Enter book index to remove: ");
      scanf("%d", &removeIndex);
      if (removeIndex < 1 || removeIndex > booksCount)
      {
        printf("Invalid book index!\n");
        break;
      }
      struct Book removedBook = books[removeIndex - 1];
      for (int i = removeIndex - 1; i < booksCount - 1; i++)
      {
        books[i] = books[i + 1];
      }
      booksCount--;
      writeAllBooks(books, booksCount);
      printf("Successfully removed book \"%s\"!\n", removedBook.title);
      break;
    case 0:
      return 0;
    default:
      printf("Invalid option!\n");
    }
  }
}
