#ifndef subscriber_h
#define subscriber_h


#include <Python.h>


#include "msg_types.h"


// Structs

typedef struct Subscriber {
    char* id;
    PyObject* py_callback;
} Subscriber;


// Functions

/*
 * Subscribes a subscriber to a channel.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel.
 * callback -- The subscriber's callback function.
 */
Subscriber* subscribe(char* channel_name, PyObject* callback);


/*
 * Calls a PyObject callback with pickled Python argument data.
 *
 * Keyword arguments:
 * callback_with_args -- The PyObject and the data to pass along with it.
 */
void* data_callback(void* callback_with_data);


/*
 * Removes a subscriber and sets the pointer to the subscriber to NULL.
 *
 * Keyword arguments:
 * subscriber -- The subscriber to remove.
 */
void unsubscribe(Subscriber **subscriber);

#endif /* subscriber_h */
