#ifndef relay_h
#define relay_h


#include "msg_types.h"


// Constants

#define NUM_CONSUMERS 100


// Functions

/*
 * Adds a subscriber to the message system.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel to which the subscriber wishes to subscribe.
 * callback -- The callback function for the new subscriber.
 */
void register_subscriber(char* channel_name, void (*callback));


/*
 * Notifies subscribers of a new event.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel on which to notify subscribers
 * data -- The data to send to the subscribers
 */
void* notify_subscribers(char* channel_name , Data* data);


/*
 * Creates thread-shared memory.
 *
 * Keyword arguments:
 * size -- The number of bytes of shared memory to allocate.
 *
 * Returns:
 * A pointer to the shared memory.
 */
void* create_shared_memory(size_t size);


#endif /* relay_h */
