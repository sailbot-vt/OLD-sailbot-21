#ifndef relay_h
#define relay_h


#include <Python.h>


#include "msg_types.h"
#include "circular_buffer.h"


// Structs

typedef struct Relay Relay;
typedef struct Subscriber Subscriber; // To avoid circular dependency


// Functions

/*
 * Initializes a new relay.
 *
 * Returns:
 * A new relay.
 */
Relay* init_relay(void);


/*
 * Adds a subscriber to the message system.
 *
 * Keyword arguments:
 * relay -- The relay to add the subscriber to.
 * channel_name -- The name of the channel to which the subscriber wishes to subscribe.
 * subscriber -- The subscriber to add.
 */
void register_subscriber_on_channel(Relay* relay, Subscriber* subscriber);


/*
 * Pushes data to the message data buffer.
 *
 * Keyword arguments:
 * relay -- The relay to which to push the data.
 * channel_name -- The name of the channel for the data.
 * data -- The data to add.
 *
 * Returns:
 * A buffer index to access the data.
 */
CircularBufferElement push_data_to_channel(Relay* relay, char* channel_name, Data data);


/*
 * Notifies subscribers of a new event.
 *
 * Keyword arguments:
 * relay -- The relay on which to notify subscribers.
 * channel_name -- The name of the channel on which to notify subscribers.
 * buffer_elem -- The buffer index associated with the data.
 */
void notify_subscribers_on_channel(Relay* relay, char* channel_name, CircularBufferElement buffer_elem);


/*
 * Removes a subscriber from its channel.
 */
Subscriber* remove_subscriber_from_channel(Relay* relay, Subscriber* subscriber);


/*
 * Deallocates a relay and all memory associated with it.
 *
 * Deallocates all subscribers, channels, and data on the relay.
 */
void destroy_relay(Relay** relay);


#endif /* relay_h */
