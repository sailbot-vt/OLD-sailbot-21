#ifndef producer_h
#define producer_h

// Structs



// Functions

int register_to_produce_data(char channelName, int dataSize);
int publish_data(char channelName, int dataSize, int *sourcePtr);
int deregister_to_produce_data((char channelName);

#endif /* producer_h */
