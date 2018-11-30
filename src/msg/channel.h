//
// Created by William Cabell on 2018-11-30.
//

#ifndef channel_h
#define channel_h


#include "consumer_list.h"
#include "circular_buffer.h"


// Structs

typedef struct Channel {
    char* name;
    CircularBuffer* data_buffer;
    ConsumerList* consumer_list;
} Channel;


// Functions

/*
 * Creates a new, empty channel with the specified name.
 *
 * Keyword arguments:
 * name -- The name of the new channel.
 *
 * Returns:
 * A new channel with an empty data buffer and an empty list of consumers.
 */
Channel* init_channel(char* name);


/*
 * Pushes data to the channel's data buffer.
 *
 * Keyword arguments:
 * ch -- The channel
 * data -- The data to publish
 */
void publish_data(Channel* ch, Data data);


/*
 * Adds a consumer to the channel.
 *
 * Keyword arguments:
 * ch -- The channel to which to add the consumer.
 * consumer -- The consumer to add to the channel.
 */
void add_consumer_to_channel(Channel* ch, Consumer* consumer);


/*
 * Deallocates a channel and all consumers and data associated with it. Sets the given pointer to that channel to NULL.
 *
 * Keyword arguments:
 * ch -- The channel to destroy.
 */
void destroy_channel(Channel** ch);


#endif /* channel_h */
