#include <stdio.h>


#include "test_subscriber_list.h"
#include "test_channel_list.h"


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
    printf("\n");

    printf("Testing relay module:\n");
    printf("\n");

    return 0;
}