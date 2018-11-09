#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <Python.h>

#define DATASIZE 100

void insert_consumer();
void display();
int consumer_data[ DATASIZE ];

static int *dataPtr;

struct channelTable {
    int *dataPtr;
    int channelName;
};

struct channelTable* search();


int register_to_consume_data(int channelName, void *callback) {
   
    //Registers data callback with relay
    //***In theory, relay would access and create new threads for all consumers that have registered using this call***

//    void (*callback)(void *) = &data_callback;

    insert_consumer(channelName, callback);

    printf("registering consumer %p\n", callback);

//    display();

    return 0;
}

void *data_callback(void *dataPtr) {

    //Called by relay when a publisher publishes data
    //***Currently not working -- issue with consumer data structure not actually being accessed in relay***
    //	Definitely just me being stupid -- need to look into that

    int *newdataPtr = (int *)dataPtr;

    printf("data callback called: %p\n", &consumer_data);
    
    memcpy(&consumer_data, newdataPtr, DATASIZE);

    printf("First 4 ints = %i %i %i %i\n", consumer_data[0], consumer_data[1], consumer_data[2], consumer_data[3]);

    

    pthread_exit(0);

//    return dataPtr;

}


void *data_callback_2(void *dataPtr) {

    //Called by relay when a publisher publishes data
    //***Currently not working -- issue with consumer data structure not actually being accessed in relay***
    //	Definitely just me being stupid -- need to look into that

    int *newdataPtr = (int *)dataPtr;

    printf("data callback 2 called: %p\n", &consumer_data);
    
    memcpy(&consumer_data, newdataPtr, DATASIZE);

    printf("Second 4 ints = %i %i %i %i\n", consumer_data[4], consumer_data[5], consumer_data[6], consumer_data[7]);

    //<cython_callback>

    pthread_exit(0);

//    return dataPtr;

}
