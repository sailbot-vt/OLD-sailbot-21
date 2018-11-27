//
// Created by William Cabell on 11/27/18.
//

#ifndef CircularBuffer_h
#define CircularBuffer_h

#define MAX_QUEUE_SIZE 256


// Structs

typedef struct CircularBuffer {
    unsigned int head;
    unsigned int tail;

} CircularBuffer;

typedef struct Element {
    uint64_t iteration;
    int index;
} Element;

typedef struct Data {
    size_t size;
    void* data;
};


// Functions

void push(CircularBuffer*, void* data, size_t size);
Data get_element(CircularBuffer*, Element);
void emptyQueue(CircularBuffer*)

#endif /* CircularBuffer_h */
