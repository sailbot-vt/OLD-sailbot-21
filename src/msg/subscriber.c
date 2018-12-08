#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <Python.h>


#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"


// Functions

void subscribe(char* channel_name, PyObject* callback) {
    register_subscriber(channel_name, callback);
}


void data_callback(void* callback_with_args) {
    Data* data = ((CallbackWithArgs*)callback_with_args)->data;
    PyObject* py_callback = ((CallbackWithArgs*)callback_with_args)->callback;

    void* subscriber_data = malloc(data->size);
    memcpy(&subscriber_data, data->data, data->size);

    // Adds the Python function to the Python ref counter
    Py_XINCREF(py_callback);

    PyObject *result;

    // Unpickles the local copy of the object passed by publisher
    PyObject *arg = subscriber_data;
    Py_BuildValue(arg);

    // Calls the Python function
    result = PyEval_CallObject(py_callback, arg);

    free(subscriber_data);
    pthread_exit(0);
}

void unsubscribe(Subscriber **subscriber) {
    // TODO: Remove from channel

    free((**subscriber).py_callback);
    free(*subscriber);
    *subscriber = (Subscriber*)NULL;
}