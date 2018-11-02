#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define DATASIZE 100

void insert_consumer();
void display();
int consumer_data[ DATASIZE ];


int register_to_consume_data(int channelName, void *data_callback) {
   
    //Registers data callback with relay
    //***In theory, relay would access and create new threads for all consumers that have registered using this call***

    void (*callback)(int*);

    callback = &data_callback;

    insert_consumer(channelName, callback);

    printf("registering consumer %p\n", callback);

    display();

    return 0;
}

void data_callback(int *dataPtr) {

    //Called by relay when a publisher publishes data
    //***Currently not working -- issue with consumer data structure not actually being accessed in relay***
    //	Definitely just me being stupid -- need to look into that

    printf("data callback called\n");
    
    memcpy(&consumer_data, (* dataPtr), DATASIZE);

    printf("data_callback has been called back with data");

    printf("First 4 bits = %c %c %c %c", consumer_data[0], consumer_data[1], consumer_data[2], consumer_data[3]);

    //<cython_callback>

    pthread_exit(NULL);
}


