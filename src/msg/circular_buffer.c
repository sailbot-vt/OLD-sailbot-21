//
// Created by William Cabell on 11/27/18.
//

#include "circular_buffer.h"


// Functions

CircularBuffer* init_circular_buffer() {
    CircularBuffer* new_buffer = (CircularBuffer*)malloc(sizeof(CircularBuffer));
    new_buffer->size = 0;
    new_buffer->head = 0;
    new_buffer->tail = 0;
}


void push(CircularBuffer* buffer, void* data, size_t data_size) {
    Data* new_data = (Data*)malloc(sizeof(Data));
    new_data->size = data_size;
    new_data->data = data;

    int next_index = buffer->size == 0 ? 1 : (buffer->head + 1) % MAX_BUFFER_SIZE;

    buffer->data[next_index] = *new_data;

    buffer->head = next_index;
    buffer->tail = (buffer->head - buffer->size + 1) % MAX_BUFFER_SIZE;

    if (buffer->size < MAX_BUFFER_SIZE) {
        buffer->size++;
    }
}


Data* get_element(CircularBuffer* buffer, Element elem) {
    if (elem.index <= buffer->head && buffer->revolutions != elem.revolution) {
        return (Data*)NULL;
    }

    return &buffer->data[elem.index];
}


void empty_buffer(CircularBuffer* buffer) {
    buffer->size = 0;
    buffer->head = 0;
    buffer->tail = 0;
}


void destroy_circular_buffer(CircularBuffer** buffer) {
    free(*buffer);
    *buffer = (CircularBuffer*)NULL;
}