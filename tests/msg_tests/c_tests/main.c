#include <stdio.h>


#include "test_subscriber_list.h"
#include "test_channel_list.h"
#include "test_circular_buffer.h"
#include "test_relay.h"


int main(int argc, char** argv) {
    printf("Testing C functions in module: msg\n");
    printf("----------------------------------\n");

    printf("Testing subscriber_list module:\n");
    subscriber_list_all();
    printf("\n");

    printf("Testing channel_list module:\n");
    channel_list_all();
    printf("\n");

    printf("Testing circular_buffer module:\n");
    circular_buffer_all();
    printf("\n");

    printf("Testing relay module:\n");
    relay_all();
    printf("\n");

    return 0;
}