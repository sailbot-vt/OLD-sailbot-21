#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#include <Python.h>
#include <stdio.h>

#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"
#include "subscriber.h"
#include "subscriber_list.h"
#include "channel_list.h"


// Globals

pthread_mutex_t relay_mutex = PTHREAD_MUTEX_INITIALIZER;
CallbackWithData* callback_with_data;

ChannelList* channel_list;



// Private Function Definitions

/*
 * Creates a callback thread for the consumer.
 *
 * Keyword arguments:
 * subscriber -- The subscriber owning the callback.
 */
void create_callback_thread(Subscriber* subscriber);


// Functions

void start_relay() {
    channel_list = init_channel_list();
}


Subscriber* register_subscriber_on_channel(char* channel_name, PyObject* py_callback) {
    Subscriber* new_sub = malloc(sizeof(Subscriber));

    new_sub->id = (char*)calloc((strlen(channel_name) + 6), sizeof(char));
    sprintf(new_sub->id, "%s_%5f", channel_name, (double)clock());

    new_sub->py_callback = py_callback;

    Channel* channel = get_channel(channel_list, channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(channel_list, channel);
    }

    add_subscriber_to_channel(channel, new_sub);

    return new_sub;
}


CircularBufferElement push_data_to_channel(char* channel_name, Data* data) {
    Channel* channel = get_channel(channel_list, channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(channel_list, channel);
    }

    return publish_data(channel, data);
}


void notify_subscribers_on_channel(char* channel_name, CircularBufferElement buffer_elem) {
    Channel* channel = get_channel(channel_list, channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(channel_list, channel);
        return;  // No subscribers at this point
    }

    pthread_mutex_lock(&relay_mutex);

    callback_with_data = (CallbackWithData*)malloc(sizeof(CallbackWithData));
    callback_with_data->data = circular_buffer_get_element(channel->data_buffer, buffer_elem);

    foreach_subscriber(channel->subscriber_list, create_callback_thread);

    free(callback_with_data);

    pthread_mutex_unlock(&relay_mutex);
}


// Private Function Definitions

void create_callback_thread(Subscriber* subscriber) {
    callback_with_data->py_callback = subscriber->py_callback;

    pthread_t* thread = NULL;
    pthread_create(thread, NULL, data_callback, (void*)callback_with_data);
}