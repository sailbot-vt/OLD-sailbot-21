#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <Python.h>

#define DATASIZE 100

#include "relay.h"
#include "circular_buffer.h"

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

void data_callback(Data* data, PyObject* callback) {

    //Called by relay when a publisher publishes data
    //***Currently not working -- issue with consumer data structure not actually being accessed in relay***
    //	Definitely just me being stupid -- need to look into that

    void* consumer_data = malloc(data->size * sizeof(void*));

    memcpy(&consumer_data, data->data, data->size);

    Py_XINCREF(callback);

    PyObject *result;

    PyObject *arg = consumer_data;
    Py_BuildValue(arg);

    result = PyEval_CallObject(callback, arg);

    free(consumer_data);
    pthread_exit(0);
}

