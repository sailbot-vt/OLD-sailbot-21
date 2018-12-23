#include <stdlib.h>
#include <string.h>
#include <pthread.h>


#include "channel_list.h"


#define INITIAL_CAPACITY 16


// Structs

struct ChannelList {
    Channel** channels;
    size_t size;
    size_t capacity;
    pthread_mutex_t mutex;
};


// Static Function Declarations

/*
 * Doubles the capacity of a channel list.
 *
 * Keyword arguments:
 * channel_list -- The list of channels to double.
 */
static void double_capacity(ChannelList* channel_list);


/*
 * Compares two channels alphabetically.
 *
 * Keyword arguments:
 * ch_a -- The first channel
 * ch_b -- The second channel
 *
 * Returns:
 * The return value of strcmp applied to the names of both channels.
 */
static int compare_channels(const void* ch_a, const void* ch_b);


// Functions

ChannelList* init_channel_list() {
    ChannelList* channel_list = (ChannelList*)malloc(sizeof(ChannelList));

    channel_list->channels = (Channel**)malloc(sizeof(Channel*) * INITIAL_CAPACITY);

    channel_list->size = 0;
    channel_list->capacity = INITIAL_CAPACITY;

    pthread_mutex_init(&channel_list->mutex, NULL);

    return channel_list;
}


void add_channel(ChannelList* channel_list, Channel* channel) {
    if (get_channel(channel_list, channel->name) != (Channel*)NULL) {
        return;
    }

    if (channel_list->size == channel_list->capacity) {
        double_capacity(channel_list);
    }

    pthread_mutex_lock(&channel_list->mutex);

    channel_list->channels[channel_list->size] = channel;
    channel_list->size++;

    qsort((void*)channel_list->channels,
          channel_list->size,
          sizeof(Channel*),
          compare_channels);

    pthread_mutex_unlock(&channel_list->mutex);
}


Channel* get_channel(ChannelList* channel_list, char* name) {
    Channel* with_name = init_channel(name);

    pthread_mutex_lock(&channel_list->mutex);

    void* result = bsearch((void*)&with_name,
            (void*)channel_list->channels,
            channel_list->size,
            sizeof(Channel*),
            compare_channels);

    pthread_mutex_unlock(&channel_list->mutex);

    destroy_channel(&with_name);

    if (result == NULL) {
        return (Channel*)NULL;
    }

    return *(Channel**)result;
}


Channel* remove_channel(ChannelList* channel_list, char* name) {
    size_t index = 0;

    pthread_mutex_lock(&channel_list->mutex);

    while (index < channel_list->size &&
           strcmp(channel_list->channels[index]->name, name) != 0) {
        index++;
    }

    if (index < channel_list->size) {
        Channel* rmd = channel_list->channels[index];

        while (index < channel_list->size - 1) {
            channel_list->channels[index] = channel_list->channels[index + 1];
            index++;
        }

        channel_list->size--;

        pthread_mutex_unlock(&channel_list->mutex);

        return rmd;
    }

    pthread_mutex_unlock(&channel_list->mutex);

    return (Channel*)NULL;
}


void destroy_channel_list(ChannelList** channel_list) {
    free((*channel_list)->channels);
    free(*channel_list);
    *channel_list = (ChannelList*)NULL;
}


// Static Function Definitions

static void double_capacity(ChannelList* channel_list) {
    pthread_mutex_lock(&channel_list->mutex);

    channel_list->capacity *= 2;
    Channel** new_list = (Channel**)malloc(channel_list->capacity * sizeof(Channel**));

    for (size_t i = 0; i < channel_list->size; ++i) {
        new_list[i] = channel_list->channels[i];
    }

    free(channel_list->channels);
    channel_list->channels = new_list;

    pthread_mutex_unlock(&channel_list->mutex);
}


static int compare_channels(const void* ch_a, const void* ch_b) {
    Channel** channel_a = (Channel**)ch_a;
    Channel** channel_b = (Channel**)ch_b;
    return strcmp((*channel_a)->name, (*channel_b)->name);
}
