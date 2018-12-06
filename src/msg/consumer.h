#include "msg_types.h"

#ifndef consumer_h
#define consumer_h

// Structs

typedef struct Consumer {
    char* id;
    void (*callback)(void);
} Consumer;


// Functions

/*
 * Subscribes a subscriber to a channel.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel.
 * callback -- The subscriber's callback function.
 *
 * Returns:
 * ?
 */
int register_to_consume_data(char channel_name, PyObject* callback);

/*
 * Calls a PyObject callback with pickled Python argument data.
 *
 * Keyword arguments:
 * data -- The pickled Python object.
 * callback -- The Python callback function.
 */
void data_callback(Data* data, PyObject* callback);

#endif /* consumer_h */
