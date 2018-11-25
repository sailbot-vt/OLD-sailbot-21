#ifndef producer_h
#define producer_h

// Structs



// Functions

int register_to_produce_data(int channelName, int dataSize);
int publish_data(int channelName, int dataSize, int *sourcePtr);
int deregister_to_produce_data(int channelName);

#endif /* producer_h */