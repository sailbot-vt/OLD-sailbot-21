#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define DATASIZE 100

void insert_consumer();
void display();
int consumer_data[ DATASIZE ];


int register_to_consume_data(int channelName, void *data_callback) {
   
    void (*callback)(int*);

    callback = &data_callback;

    insert_consumer(channelName, callback);

    printf("registering consumer %p\n", callback);

    display();

    return 0;
}

void data_callback(int *dataPtr) {

    printf("data callback called\n");
    
    memcpy(&consumer_data, (* dataPtr), DATASIZE);

    printf("data_callback has been called back with data");

    printf("First 4 bits = %c %c %c %c", consumer_data[0], consumer_data[1], consumer_data[2], consumer_data[3]);

    pthread_exit(NULL);
}


