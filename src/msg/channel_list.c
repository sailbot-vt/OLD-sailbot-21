//
// Created by William Cabell on 2018-11-30.
//


#include "string.h"


#include "channel_list.h"


#define INITIAL_CAPACITY 16


// Structs

struct ChannelList {
    Channel** channels;
    size_t size;
    size_t capacity;
};


// Static Function Declarations

/*
 * Doubles the capacity of the channel list.
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

    channel_list->channels = (Channel**)malloc(sizeof(Channel*));

    channel_list->size = 0;
    channel_list->capacity = INITIAL_CAPACITY;

    return channel_list;
}


void add_channel(ChannelList* channel_list, Channel* channel) {
    if (channel_list->size == channel_list->capacity) {
        double_capacity(channel_list);
    }

    channel_list->channels[channel_list->size] = channel;

    qsort(channel_list->channels,
          channel_list->size,
          sizeof(Channel*),
          compare_channels);
}


Channel* remove_channel(ChannelList* channel_list, char* name) {

}


Channel* get_channel(ChannelList* channel_list, char* name) {

}


void destroy_channel_list(ChannelList** channel_list) {

}


// Static Function Definitions

static void double_capacity(ChannelList* channel_list) {

}


static int compare_channels(const void* ch_a, const void* ch_b) {
    Channel* channel_a = (Channel*)ch_a;
    Channel* channel_b = (Channel*)ch_b;
    return strcmp(channel_a->name, channel_b->name);
}