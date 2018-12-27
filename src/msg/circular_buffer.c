#include <stdlib.h>
#include <pthread.h>
#include <sys/mman.h>


#include "circular_buffer.h"


// Structs

struct CircularBuffer {
    int size;
    int head;
    uint64_t revolutions;
    Data data[MAX_BUFFER_SIZE];
    pthread_mutex_t mutex;
};


// Functions

CircularBuffer* init_circular_buffer() {
    CircularBuffer* new_buffer = (CircularBuffer*)malloc(sizeof(CircularBuffer));
    new_buffer->size = 0;
    new_buffer->head = 0;

    pthread_mutex_init(&new_buffer->mutex, NULL);

    return new_buffer;
}


CircularBufferElement circular_buffer_push(CircularBuffer* buffer, Data data) {
    pthread_mutex_lock(&buffer->mutex);

    int next_index = buffer->size == 0 ? 1 : (buffer->head + 1) % MAX_BUFFER_SIZE;

    buffer->data[next_index] = data;

    buffer->head = next_index;

    if (buffer->size < MAX_BUFFER_SIZE) {
        buffer->size++;
    }

    if (next_index == 0) {
        buffer->revolutions++;
    }

    CircularBufferElement element;
    element.index = next_index;
    element.revolution = buffer->revolutions;

    CircularBufferElement old_element = element;
    element.revolution -= 1;

    Data to_overwrite = circular_buffer_get_element(buffer, old_element);
    munmap(to_overwrite.data, to_overwrite.size);

    pthread_mutex_unlock(&buffer->mutex);

    return element;
}


Data circular_buffer_get_element(CircularBuffer* buffer, CircularBufferElement elem) {
    pthread_mutex_lock(&buffer->mutex);

    if (elem.index <= buffer->head && buffer->revolutions != elem.revolution) {
        Data null;
        null.data = NULL;
        null.size = 0;
        return null;
    }

    pthread_mutex_unlock(&buffer->mutex);

    return buffer->data[elem.index];
}


void empty_circular_buffer(CircularBuffer* buffer) {
    pthread_mutex_lock(&buffer->mutex);

    buffer->size = 0;
    buffer->head = 0;

    pthread_mutex_unlock(&buffer->mutex);
}


void destroy_circular_buffer(CircularBuffer** buffer) {
    free(*buffer);
    *buffer = (CircularBuffer*)NULL;
}