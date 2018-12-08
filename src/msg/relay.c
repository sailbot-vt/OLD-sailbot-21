#include <time.h>
#include <pthread.h>
#include <Python.h>

#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"
#include "subscriber.h"
#include "subscriber_list.h"
#include "channel_list.h"


// Globals

pthread_mutex_t* mutex;
CallbackWithData* callback_with_data;

ChannelList* channel_list;
CircularBuffer* data_buffer;



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
    data_buffer = init_circular_buffer();

    pthread_mutexattr_t* pthread_mutexattr;
    pthread_mutexattr_init(pthread_mutexattr);
    pthread_mutex_init(mutex, pthread_mutexattr);
}


Subscriber* register_subscriber(char* channel_name, PyObject* py_callback) {
    Subscriber* new_sub = malloc(sizeof(Subscriber));

    new_sub->id = sprintf("%s_%d", channel_name, clock());
    new_sub->py_callback = py_callback;

    Channel* channel = get_channel(channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(channel_list, channel);
    }

    add_subscriber_to_channel(channel, new_sub);

    return new_sub;
}


CircularBufferElement* push_data_to_msg_buffer(Data* data) {
    return circular_buffer_push(data_buffer, data);
}


void notify_subscribers(char* channel_name, CircularBufferElement* buffer_elem) {
    Channel* channel = get_channel(channel_name);

    if (channel == (Channel*)NULL) {
        channel = init_channel(channel_name);
        add_channel(channel_list, channel);
        return;  // No subscribers at this point
    }

    pthread_mutex_lock(mutex);

    callback_with_data = (CallbackWithArgs*)malloc(sizeof(CallbackWithArgs));
    callback_with_data->data = circular_buffer_get_element(channel->data_buffer, buffer_elem);

    foreach_consumer(channel->consumer_list, create_callback_thread);

    free(callback_with_data);

    pthread_mutex_unlock(mutex);
}


// Private Function Definitions

void create_callback_thread(Consumer* consumer) {
    callback_with_data->py_callback = consumer->py_callback;

    pthread_t* thread;
    pthread_attr_t* pthread_attr;
    pthread_attr_init(pthread_attr);
    pthread_create(thread, pthread_attr, data_callback, (void*)callback_with_args);
}