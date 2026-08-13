#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFSIZE 1024

void *handle_client(void *arg)
{
    int client_fd = (long)arg; // the socket number was passed as the argument
    char buffer[BUFSIZE];
    int n;

    while ((n = read(client_fd, buffer, BUFSIZE - 1)) > 0) {
        buffer[n] = '\0';
        printf("Received: %s", buffer);
        write(client_fd, buffer, n); // echo the same bytes back
    }

    printf("Client disconnected.\n");
    close(client_fd);
    return NULL;
}

int main(int argc, char *argv[])
{
    if (argc < 2) {
        printf("Usage: %s <port>\n", argv[0]);
        return 1;
    }
    // take the LAST argument: Android/Termux can add extra args in front
    char *port = argv[argc - 1];

    // 1. Socket()
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(atoi(port));

    // 2. Bind()
    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        return 1;
    }

    // 3. Listen()
    if (listen(server_fd, 5) < 0) {
        perror("listen");
        return 1;
    }
    printf("Echo server listening on port %s...\n", port);

    while (1) {
        // 4. Accept()
        int client_fd = accept(server_fd, NULL, NULL);
        if (client_fd < 0)
            continue;
        printf("Client connected.\n");

        pthread_t tid;
        pthread_create(&tid, NULL, handle_client, (void *)(long)client_fd);
        pthread_detach(tid);
    }
}
