#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <Python.h>

#define DATASIZE 100

#include "relay.h"

// Globals

int *dataPtr;


// Functions

int register_to_consume_data(char channelName, PyObject* callback) {
   
    //Registers data callback with relay
    //***In theory, relay would access and create new threads for all consumers that have registered using this call***

//    void (*callback)(void *) = &data_callback;

    void *data_callback = (void *)data_callback;    

    insert_consumer(channelName, callback);

    printf("registering consumer %p\n", callback);

//    display();

    return 0;
}

void *data_callback(Element element, PyObject* callback) {

    //Called by relay when a publisher publishes data
    //***Currently not working -- issue with consumer data structure not actually being accessed in relay***
    //	Definitely just me being stupid -- need to look into that

    int consumer_data[element.size];

    void* consumer_data = malloc(element.size * sizeof(void*));

    //int consumer_data[ dataSize ];

    //int *newdataPtr = (int *)dataPtr;

    memcpy(&consumer_data, element.data, element.size);

    PyObject_CallObject(callback, consumer_data);

    free(consumer_data);

    pthread_exit(0);

//    return dataPtr;

}

