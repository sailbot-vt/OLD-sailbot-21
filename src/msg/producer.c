#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "relay.h"

// Globals

int *dataPtr;


// Function Definitions

int register_to_produce_data(char channelName, int dataSize) {
    
    //Calls create buffer which creates a shared memory block for publisher to publish to
    //Producer and corresponding data ptr are stored in hashArray

    if(search(channelName) != NULL) {

        return create_buffer(channelName); 
    }

    return NULL;

}

int publish_data(char channelName, int dataSize, int *sourcePtr) {

    //Uses hashArray to find where to publish data to then memcpy's to there
    //Calls notify_consumers method of relay
	
    int *dataPtr = search(channelName)->dataPtr;

    memcpy(dataPtr,sourcePtr, dataSize);

    notify_consumers(channelName, dataSize, dataPtr);

    return 0;
}

int deregister_to_produce_data(char channelName) {

    channel_table table = search(channelName);

    int *loc_ptr = table->dataPtr;

    int dataSize = table->maxSize;

    void *realloc(loc_ptr, dataSize);
} 
