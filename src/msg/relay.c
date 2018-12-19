#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#include <Python.h>
#include <stdio.h>
#include <stdbool.h>

#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"
#include "subscriber.h"
#include "subscriber_list.h"
#include "channel_list.h"


// Structs

struct Relay {
    ChannelList *channel_list;
    pthread_mutex_t mutex;
};

// Globals

CallbackWithData *callback_with_data;


// Private Function Definitions

/*
 * Creates a callback thread for the consumer.
 *
 * Keyword arguments:
 * subscriber -- The subscriber owning the callback.
 */
static void create_callback_thread(Subscriber* subscriber);


// Functions

Relay* init_relay() {
    Relay* new_relay = (Relay*)malloc(sizeof(Relay));
    new_relay->channel_list = init_channel_list();
    pthread_mutex_init(&new_relay->mutex, NULL);
    return new_relay;
}


void register_subscriber_on_channel(Relay* relay, char* channel_name, Subscriber* subscriber) {
    Channel* channel = get_channel(relay->channel_list, channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(relay->channel_list, channel);
    }

    add_subscriber_to_channel(channel, subscriber);
}


CircularBufferElement push_data_to_channel(Relay* relay, char* channel_name, Data* data) {
    Channel* channel = get_channel(relay->channel_list, channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(relay->channel_list, channel);
    }

    return publish_data(channel, data);
}


void notify_subscribers_on_channel(Relay* relay, char* channel_name, CircularBufferElement buffer_elem) {
    Channel* channel = get_channel(relay->channel_list, channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(relay->channel_list, channel);
        return;  // No subscribers at this point
    }

    pthread_mutex_lock(&relay->mutex);

    callback_with_data = (CallbackWithData*)malloc(sizeof(CallbackWithData));
    callback_with_data->data = circular_buffer_get_element(channel->data_buffer, buffer_elem);

    foreach_subscriber(channel->subscriber_list, create_callback_thread);

    free(callback_with_data);

    pthread_mutex_unlock(&relay->mutex);
}


void destroy_relay(Relay** relay) {
    // TODO
}


// Private Function Definitions

static void create_callback_thread(Subscriber* subscriber) {
    callback_with_data->py_callback = subscriber->py_callback;

    pthread_t* thread = NULL;
    pthread_create(thread, NULL, data_callback, (void*)callback_with_data);
}
