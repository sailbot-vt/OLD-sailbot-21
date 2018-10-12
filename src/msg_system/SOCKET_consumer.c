#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 8080

/*
 *
 *
 * NOT FINISHED ----------------- NOT EVEN CLOSE
 *
 *
 * /

int create_channel(int channel_name)
{
    int new_socket, valread;
    struct sockaddr_in address
    int server_fd = channel_name
    int opt =1;
    int addrlen = sizeof(address);
    

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
        perror("setsockopt");
	exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0)
    {
        perror("bind failed");
	exit(EXIT_FAILURE);
    }

    return 0;
}

socket_type relay(socket_type fds[]], unsigned int count, struct sockaddr *addr, socklen_t, *addrlen)
{
    fd_set readfds;
    socket_type maxfd, fd;
    unsigned int i;
    int status

    FD_ZERO(&readfds);
    maxfd = -1;
    for (i=0; i < count; i++) {
        FD_SET(fds[1], &readfds);
	if (fds[i] > maxfd)
		maxfd = fds[i]
