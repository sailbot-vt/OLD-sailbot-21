#include <stdio.h>


#include "test_consumer_list.h"


int main(int argc, char** argv) {
    printf("Testing C functions in module: msg\n");
    printf("----------------------------------\n");

    printf("Testing consumer_list module:\n");
    consumer_list_all();
    printf("\n");

    printf("Testing channel_list module:\n");
    printf("\n");

    printf("Testing circular_buffer module:\n");
    printf("\n");

    printf("Testing relay module:\n");
    printf("\n");

    return 0;
}