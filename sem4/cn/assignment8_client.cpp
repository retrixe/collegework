#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void)
{
    struct sockaddr_in socket_address = {
        .sin_family = AF_INET,
        .sin_port = htons(1100),
        .sin_addr = {},
        .sin_zero = {},
    };
    int success = inet_pton(AF_INET6, "::1", &socket_address.sin_addr);
    if (success != 1) {
        perror("failed to parse socket address");
        exit(EXIT_FAILURE);
    }

    int socket_fd = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (socket_fd == -1) {
        perror("cannot create socket");
        exit(EXIT_FAILURE);
    }

    if (connect(socket_fd, (struct sockaddr *)&socket_address, sizeof socket_address) == -1) {
        perror("connect failed");
        close(socket_fd);
        exit(EXIT_FAILURE);
    }

    for (;;) {
        // send message
        char buf[1024] = {0};
        printf("enter message: ");
        fgets(buf, sizeof(buf), stdin);
        buf[strcspn(buf, "\n")] = 0;
        if (strcmp(buf, "quit client") == 0)
            break;
        send(socket_fd, buf, strlen(buf), 0);

        // read from socket
        memset(buf, 0, sizeof(buf));
        ssize_t n = recv(socket_fd, buf, sizeof(buf), 0);
        if (n == -1) {
            printf("recv() failed\n");
        } else if (n == 0) {
            printf("client disconnected\n");
            break;
        } else {
            printf("received message: %s\n", buf);
        }
    }

    close(socket_fd);
    return EXIT_SUCCESS;
}
