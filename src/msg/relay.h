#ifndef relay_h
#define relay_h

// Structs
typedef struct channel_table {
    int *dataPtr;
    int maxSize;
    int channelName;
    void (*consumers[NUM_CONSUMERS]);
} channel_table;

// Functions

void display(void);
void *notify_consumers(int channelName,int dataSize, int *dataPtr);
int create_buffer(int channelName, int dataSize);

#endif /* relay_h */