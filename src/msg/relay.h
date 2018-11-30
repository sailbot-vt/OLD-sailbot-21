#ifndef relay_h
#define relay_h

//Constants
#define NUM_CONSUMERS 100

// Functions

void display(void);
void *notify_consumers(char channelName,int dataSize, int *dataPtr);
int create_buffer(char channelName, int dataSize);

#endif /* relay_h */
