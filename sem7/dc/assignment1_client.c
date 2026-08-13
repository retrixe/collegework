#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFSIZE 1024

int main(int argc, char *argv[])
{
    if (argc < 3) {
        printf("Usage: %s <server-ip> <port>\n", argv[0]);
        return 1;
    }
    // take the LAST two arguments: Android/Termux can add extra args in front
    char *server_ip = argv[argc - 2];
    char *port = argv[argc - 1];

    // 1. Socket()
    int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(server_ip);
    server_addr.sin_port = htons(atoi(port));

    // 2. Connect()
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        return 1;
    }
    printf("Connected to server. Press Ctrl+D to quit.\n");

    char buffer[BUFSIZE];
    int n;

    while (1) {
        printf("Enter message: ");
        fflush(stdout);
        if (fgets(buffer, BUFSIZE, stdin) == NULL)
            break;

        // 3. Write()
        write(sock_fd, buffer, strlen(buffer));

        // 4. Read()
        n = read(sock_fd, buffer, BUFSIZE - 1);
        if (n <= 0) {
            printf("Server closed the connection.\n");
            break;
        }
        buffer[n] = '\0';
        printf("Echo from server: %s", buffer);
    }

    close(sock_fd);
    return 0;
}
