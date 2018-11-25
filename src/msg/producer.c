#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "relay.h"

// Globals

int *dataPtr;


// Function Definitions

int register_to_produce_data(int channelName, int dataSize) {
    
    //Calls create buffer which creates a shared memory block for publisher to publish to
    //Producer and corresponding data ptr are stored in hashArray

    dataPtr = create_buffer(channelName, dataSize); 

    return dataPtr;
}

int publish_data(int channelName, int dataSize, int *sourcePtr) {

    //Uses hashArray to find where to publish data to then memcpy's to there
    //Calls notify_consumers method of relay
	
    int *dataPtr = search(channelName)->dataPtr;

    memcpy(dataPtr,sourcePtr, dataSize);

    notify_consumers(channelName, dataSize, dataPtr);

    return 0;
}

int deregister_to_produce_data(int channelName) {

    channel_table table = search(channelName);

    int *loc_ptr = table->dataPtr;

    int dataSize = table->maxSize;

    void *realloc(loc_ptr, dataSize);
} 
