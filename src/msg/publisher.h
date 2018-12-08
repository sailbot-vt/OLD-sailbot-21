#ifndef publisher_h
#define publisher_h


// Functions

/*
 * Broadcasts data to the given channel.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel to which to publish.
 * data -- A pointer to the data to include.
 * data_size -- The number of bytes in the data.
 */
void publish(char* channel_name, void* data, size_t data_size);


#endif /* publisher_h */
