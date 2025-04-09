#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    struct sockaddr_in socket_address = {
        .sin_family = AF_INET,
        .sin_port = htons(1100),
        .sin_addr = {
            .s_addr = htonl(INADDR_ANY),
        },
        .sin_zero = {},
    };

    int socket_fd = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (socket_fd == -1) {
        perror("cannot create socket");
        exit(EXIT_FAILURE);
    }

    if (bind(socket_fd, (struct sockaddr *) &socket_address, sizeof socket_address) == -1) {
        perror("bind failed");
        close(socket_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(socket_fd, 10) == -1) {
        perror("listen failed");
        close(socket_fd);
        exit(EXIT_FAILURE);
    }

    printf("server listening on port 1100\n");
    for (;;) {
        const int connection_fd = accept(socket_fd, nullptr, nullptr);

        if (connection_fd == -1) {
            perror("accept failed");
            close(socket_fd);
            exit(EXIT_FAILURE);
        }

        printf("accepted new connection\n");

        char buffer[1024];
        for (;;) {
            memset(buffer, 0, sizeof(buffer));
            const ssize_t n = read(connection_fd, buffer, sizeof(buffer));
            buffer[strcspn(buffer, "\n")] = 0;
            if (n == -1 || n == 0 || strcmp(buffer, "quit server") == 0) {
                break;
            }
            printf("received message: %s\n", buffer);
            write(connection_fd, buffer, strlen(buffer));
        }

        if (shutdown(connection_fd, SHUT_RDWR) == -1) {
            perror("shutdown failed");
            close(connection_fd);
            close(socket_fd);
            exit(EXIT_FAILURE);
        }
        close(connection_fd);

        if (strcmp(buffer, "quit server") == 0) {
            break;
        }
    }

    close(socket_fd);
    return EXIT_SUCCESS;
}
