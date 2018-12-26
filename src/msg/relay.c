#include <Python.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
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


// Private Function Definitions

/*
 * Creates a callback thread for the consumer.
 *
 * Keyword arguments:
 * subscriber -- The subscriber owning the callback.
 * argc -- Should be 2, for data and thread array, respectively
 * va_list -- The data and thread array are passed, respectively
 */
static void create_callback_thread(int index, Subscriber* subscriber, int argc, va_list);


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

    int num_callbacks = get_subscriber_list_size(channel->subscriber_list);
    pthread_t** threads = (pthread_t**)malloc(num_callbacks * sizeof(pthread_t*));
    for (int i = 0; i < num_callbacks; ++i) {
        threads[i] = (pthread_t*)NULL;
    }

    Data* data = circular_buffer_get_element(channel->data_buffer, buffer_elem);

    foreach_subscriber(channel->subscriber_list, create_callback_thread, 2, data, threads);

    pthread_mutex_unlock(&relay->mutex);


    // Wait for threads to finish before exiting
    // Outside of mutex, so does not block subsequent calls to notify_subscribers_on_channel
    for (int i = 0; i < num_callbacks; ++i) {
        pthread_join(*threads[i], NULL);
    }

    // Free completed threads
    for (int i = 0; i < num_callbacks; ++i) {
        free(threads[i]);
    }
    free(threads);
}


void destroy_relay(Relay** relay) {
    // TODO
}


// Private Function Definitions

static void create_callback_thread(int index, Subscriber* subscriber, int argc, va_list argv) {
    CallbackWithData* callback_with_data = (CallbackWithData*)malloc(sizeof(CallbackWithData));
    callback_with_data->data = va_arg(argv, Data*);
    callback_with_data->py_callback = subscriber->py_callback;

    pthread_t** threads = va_arg(argv, pthread_t**);

    pthread_create(threads[index], NULL, data_callback, (void*)callback_with_data);
}
