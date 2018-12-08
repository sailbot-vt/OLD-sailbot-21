#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <pthread.h>
#include <Python.h>

#include "relay.h"
#include "msg_types.h"
#include "circular_buffer.h"
#include "subscriber.h"
#include "subscriber_list.h"
#include "channel_list.h"


// Globals

int rc;
CallbackWithData* callback_with_data;
ChannelList* channel_list;
pthread_mutex_t* mutex;


// Private Function Definitions

/*
 * Creates a callback thread for the consumer.
 *
 * Keyword arguments:
 * consumer -- The subscriber owning the callback.
 */
void create_callback_thread(Consumer* consumer);


// Functions

void start_relay() {
    channel_list = init_channel_list();
    pthread_mutexattr_t* pthread_mutexattr;
    pthread_mutexattr_init(pthread_mutexattr);
    pthread_mutex_init(mutex, pthread_mutexattr);
}


void register_subscriber(char* channel_name, PyObject* py_callback) {
    Consumer* new_sub = malloc(sizeof(Consumer));

    new_sub->id = sprintf("%s_%d", channel_name, clock());
    new_sub->py_callback = py_callback;

    add_consumer_to_channel(channel_name, new_sub);
}


void* notify_subscribers(char* channel_name, CircularBufferElement* buffer_elem) {
    Channel* channel = get_channel(channel_name);

    pthread_mutex_lock(mutex);

    callback_with_data = (CallbackWithArgs*)malloc(sizeof(CallbackWithArgs));
    callback_with_data->data = circular_buffer_get_element(channel->data_buffer, buffer_elem);

    foreach_consumer(channel->consumer_list, create_callback_thread);

    free(callback_with_data);

    pthread_mutex_unlock(mutex);
}


void* create_shared_memory(size_t size) {
    int protection = PROT_READ | PROT_WRITE;
    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    return mmap(NULL, size, protection, visibility, 0, 0);
}


// Private Function Definitions

void create_callback_thread(Consumer* consumer) {
    callback_with_data->py_callback = consumer->py_callback;

    pthread_t* thread;
    pthread_attr_t* pthread_attr;
    pthread_attr_init(pthread_attr);
    pthread_create(thread, pthread_attr, data_callback, (void*)callback_with_args);
}