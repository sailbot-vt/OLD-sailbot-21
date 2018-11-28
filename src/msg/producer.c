#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "relay.h"


// Function Definitions

/*
 * Creates a shared memory region and adds the
 */
int register_to_produce_data(char* channel_name, int data_size) {

    //Calls create buffer which creates a shared memory block for publisher to publish to
    //Producer and corresponding data ptr are stored in

    return create_buffer(channel_name, data_size);
}


int publish_data(char* channelName, int dataSize, int *sourcePtr) {

    //Uses hashArray to find where to publish data to then memcpy's to there
    //Calls notify_consumers method of relay
	
    int *dataPtr = search(channelName)->dataPtr;

    memcpy(dataPtr,sourcePtr, dataSize);

    notify_consumers(channelName, dataSize, dataPtr);

    return 0;
}


int deregister_to_produce_data(char* channelName) {

    channel_table table = search(channelName);

    int *loc_ptr = table->dataPtr;

    int dataSize = table->maxSize;

    void *realloc(loc_ptr, dataSize);
} 
