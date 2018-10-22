#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define DATASIZE 100

void insert_consumer();
int consumer_data[ DATASIZE ];


int register_to_consume_data(int channelName, void *data_callback) {
    
    insert_consumer(channelName, data_callback);

    printf("registering consumer");

    return 0;
}

void data_callback(int *dataPtr) {

    memcpy(&consumer_data, (* dataPtr), DATASIZE);

    printf("data_callback has been called back with data");

    printf("First 4 bits = %c %c %c %c", consumer_data[0], consumer_data[1], consumer_data[2], consumer_data[3]);

    pthread_exit(NULL);
}


