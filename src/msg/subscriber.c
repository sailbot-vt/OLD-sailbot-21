#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <Python.h>


#include "subscriber.h"
#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"


// Functions

Subscriber* subscribe(char* channel_name, PyObject* callback) {
    return register_subscriber(channel_name, callback);
}


void* data_callback(void* callback_with_data) {
    Data* data = ((CallbackWithData*)callback_with_data)->data;
    PyObject* py_callback = ((CallbackWithData*)callback_with_data)->py_callback;

    void* subscriber_data = malloc(data->size);
    memcpy(&subscriber_data, data->data, data->size);

    // Why can't we do this part in Python?

    // Adds the Python function to the Python ref counter
    Py_XINCREF(py_callback);

    PyObject *result;

    // Unpickles the local copy of the object passed by publisher
    PyObject *arg = subscriber_data;
    Py_BuildValue(arg);

    // Calls the Python function
    result = PyEval_CallObject(py_callback, arg);

    free(subscriber_data);

    // Have to return something
    return NULL;
}

void unsubscribe(Subscriber **subscriber) {
    // TODO: Remove from channel

    free((**subscriber).py_callback);
    free(*subscriber);
    *subscriber = (Subscriber*)NULL;
}