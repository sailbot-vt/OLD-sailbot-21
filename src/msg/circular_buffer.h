//
// Created by William Cabell on 11/27/18.
//

#ifndef CircularBuffer_h
#define CircularBuffer_h


#include <stdlib.h>


#define MAX_BUFFER_SIZE 256


// Structs

typedef struct Element {
    uint64_t revolution;
    int index;
} Element;


typedef struct Data {
    size_t size;
    void* data;
} Data;


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
 * data -- A pointer to the data.
 * data_size -- The number of bytes in the data.
 */
void push(CircularBuffer* buffer, void* data, size_t data_size);

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
Data* get_element(CircularBuffer* buffer, Element elem);

/*
 *
 */
void empty_buffer(CircularBuffer *buffer);

/*
 *
 */
void destroy_circular_buffer(CircularBuffer** buffer);

#endif /* CircularBuffer_h */
