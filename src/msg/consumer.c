#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <Python.h>

#define DATASIZE 100

#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"

// Globals

int *dataPtr;


// Functions

void subscribe(char* channel_name, PyObject* callback) {
   
    //Registers data callback with relay
    //***In theory, relay would access and create new threads for all consumers that have registered using this call***

//    void (*callback)(void *) = &data_callback;

    void* data_callback = (void*)callback;

    insert_consumer(channelName, callback);

    printf("registering consumer %p\n", callback);

//    display();
}


void data_callback(void* callback_with_args) {
    Data* data = ((CallbackWithArgs*)callback_with_args)->data;
    PyObject* py_callback = ((CallbackWithArgs*)callback_with_args)->callback;

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

