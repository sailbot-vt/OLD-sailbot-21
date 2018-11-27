#ifndef consumer_h
#define consumer_h

// Functions

int register_to_consume_data(char channelName, PyObject* callback);
void *data_callback(void *dataPtr, int dataSize, PyObject* callback);

#endif /* consumer_h */
