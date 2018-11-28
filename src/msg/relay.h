#ifndef relay_h
#define relay_h

// Structs
typedef struct channel_table {
    int *dataPtr;
    int maxSize;
    char* channelName;
    void *consumers;
} channel_table;


// Functions

int create_buffer(char* channelName, int dataSize);
void display(void);
void *notify_consumers(char* channelName,int dataSize, int *dataPtr);

#endif /* relay_h */