#ifndef subscriber_h
#define subscriber_h


#include <Python.h>


#include "msg_types.h"
#include "relay.h"


// Structs

typedef struct Subscriber {
    char* id;
    char* channel_name;
    PyObject* py_callback;
} Subscriber;


// Functions

/*
 * Subscribes a subscriber to a channel.
 *
 * Keyword arguments:
 * relay -- The relay with the channel to subscribe to.
 * channel_name -- The name of the channel.
 * callback -- The subscriber's callback function.
 */
Subscriber* subscribe(Relay* relay, char* channel_name, PyObject* callback);


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
 * relay -- The relay from which to remove the subscriber.
 * subscriber -- The subscriber to remove.
 */
void unsubscribe(Relay* relay, Subscriber* subscriber);


/*
 * Deallocates all memory associated with a subscriber.
 *
 * Keyword arguments:
 * subscriber -- The subscriber to destroy.
 */
void destroy_subscriber(Subscriber** subscriber);

#endif /* subscriber_h */
