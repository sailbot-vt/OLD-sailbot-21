#ifndef channel_h
#define channel_h


#include "subscriber_list.h"
#include "circular_buffer.h"


// Structs

typedef struct Channel {
    char* name;
    CircularBuffer* data_buffer;
    SubscriberList* subscriber_list;
} Channel;


// Functions

/*
 * Creates a new, empty channel with the specified name.
 *
 * Keyword arguments:
 * name -- The name of the new channel.
 *
 * Returns:
 * A new channel with an empty data buffer and an empty list of subscribers.
 */
Channel* init_channel(char* name);


/*
 * Pushes data to the channel's data buffer.
 *
 * Keyword arguments:
 * ch -- The channel
 * data -- The data to publish
 */
CircularBufferElement publish_data(Channel* ch, Data* data);


/*
 * Adds a subscriber to the channel.
 *
 * Keyword arguments:
 * ch -- The channel to which to add the subscriber.
 * subscriber -- The subscriber to add to the channel.
 */
void add_subscriber_to_channel(Channel* ch, Subscriber* subscriber);


/*
 * Deallocates a channel and all subscribers and data associated with it. Sets the given pointer to that channel to NULL.
 *
 * Keyword arguments:
 * ch -- The channel to destroy.
 */
void destroy_channel(Channel** ch);


#endif /* channel_h */
