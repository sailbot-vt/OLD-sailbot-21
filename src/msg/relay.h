#ifndef relay_h
#define relay_h


#include <Python.h>


#include "subscriber.h"
#include "msg_types.h"
#include "circular_buffer.h"


// Functions

/*
 * Adds a subscriber to the message system.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel to which the subscriber wishes to subscribe.
 * callback -- The callback function for the new subscriber.
 */
Subscriber* register_subscriber(char* channel_name, PyObject* py_callback);


/*
 * Pushes data to the message data buffer.
 *
 * Keyword arguments:
 * data -- The data to add.
 *
 * Returns:
 * A buffer index to access the data.
 */
CircularBufferElement* push_data_to_msg_buffer(Data* data);


/*
 * Notifies subscribers of a new event.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel on which to notify subscribers.
 * buffer_elem -- The buffer index associated with the data.
 */
void notify_subscribers(char* channel_name, CircularBufferElement* buffer_elem);


#endif /* relay_h */
