#ifndef CircularBuffer_h
#define CircularBuffer_h


#include <stdlib.h>


#include "msg_types.h"


#define MAX_BUFFER_SIZE 256


// Structs

typedef struct CircularBufferElement {
    uint64_t revolution;
    int index;
} CircularBufferElement;


typedef struct CircularBuffer {
    int size;
    int head;
    int tail;
    uint64_t revolutions;
    Data data[MAX_BUFFER_SIZE];
} CircularBuffer;


// Functions

/*
 * Creates a new CircularBuffer.
 *
 * Returns:
 * A new CircularBuffer struct initialized to be empty.
 */
CircularBuffer* init_circular_buffer(void);

/*
 * Adds a new Data item to the buffer.
 *
 * WILL OVERRIDE DATA ALREADY IN THE BUFFER.
 *
 *
 * Keyword arguments:
 * buffer -- The CircularBuffer to which to add the data.
 * data -- The data to add.
 */
CircularBufferElement* circular_buffer_push(CircularBuffer* buffer, Data data);

/*
 * Gets an element from the buffer.
 *
 * Returns NULL and executes the callback function if the requested data has been overridden.
 *
 * Keyword arguments:
 * buffer -- The buffer from which to attempt to get the data.
 * elem -- An element struct specifying which index and iteration of the data to get.
 *
 * Returns:
 * The Data struct containing the data or NULL.
 */
Data* circular_buffer_get_element(CircularBuffer* buffer, CircularBufferElement* elem);

/*
 * Empties the provided buffer.
 *
 * Keyword arguments:
 * buffer -- The buffer to empty.
 */
void empty_circular_buffer(CircularBuffer *buffer);

/*
 * Deallocates the provided buffer, and sets the pointer to it to NULL.
 *
 * Keyword arguments:
 * buffer -- The buffer to deallocate.
 */
void destroy_circular_buffer(CircularBuffer** buffer);

#endif /* CircularBuffer_h */
