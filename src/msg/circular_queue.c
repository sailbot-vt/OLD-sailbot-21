#include <stdlib.h>
#include <stdbool.h>

#include "circular_queue.h"

// Private function declarations
static void cirque_resize(cirque* queue);
static bool cirque_is_empty(const cirque* queue);


// Functions

/* Builds a new dynamically sized circular queue.

Returns:
A pointer to the new circular queue.
*/
cirque* cirque_create() {
    const unsigned int size = 16;  // Start with 16 entries
    cirque* queue = malloc(sizeof(cirque));

    if (queue) {
        queue->entries = malloc(size * sizeof(void*));
        if (queue->entries) {
            queue->size = size;
            queue->head = 0;
            queue->tail = 0;
            queue->is_full = 0;
        }
        else {
            free(queue);
            queue = NULL;
        }
    }

    return queue;
}


/* Empties a circular queue.

Keyword arguments:
queue -- The queue to empty.
*/
void cirque_empty(cirque* queue) {
    if (queue) {
        free(queue->entries);
        free(queue);
    }
}


/* Inserts a new element into a circular queue.

Keyword arguments:
queue -- The queue into which to insert the new element.
data -- The new element to add.

Returns:
True iff the addition was successful.
*/
bool cirque_enqueue(cirque* queue, void* data) {
    bool result = false;

    if (queue->is_full) {
        cirque_resize(queue);
    }

    if (!queue->is_full) {
        queue->entries[queue->tail++] = data;
        queue->tail %= queue->size;

        if (queue->tail == queue->head) {
            queue->is_full = true;
        }

        result = true;
    }

    return result;
}


/* Removes and returns the next element from a circular queue.

Keyword arguments:
queue -- The queue from which to remove the element.

Returns:
The removed element or NULL if the queue was empty.
*/
void* cirque_remove(cirque* queue) {
    void* data = NULL;

    if (!cirque_is_empty(queue)) {
        data = queue->entries[queue->head++];

        queue->head %= queue->size;

        if (queue->is_full) {
            queue->is_full = false;
        }
    }

    return data;
}


/* Gets the next element in a circular queue without removing it.

Keyword arguments:
queue -- The queue at which to peek.

Returns:
The next element in the queue or NULL if the queue is empty.
*/
void* cirque_peek(const cirque* queue) {
    void* data = NULL;
    if (!cirque_is_empty(queue)) {
        data = queue->entries[queue->head];
    }
    return data;
}


/* Gets the number of elements currently in the queue.

Keyword arguments:
queue -- The queue of which to check the size.

Returns:
The size of the queue.
*/
unsigned int cirque_get_count(const cirque* queue) {
    unsigned int count;
    if (cirque_is_empty(queue)) {
        count = 0;
    }
    else if (queue->is_full) {
        count = queue->size;
    }
    else if (queue->tail > queue->head) {
        count = queue->tail - queue->head;
    }
    else {
        count = queue->size - queue->head;
        if (queue->tail > 0) {
            count += queue->tail - 1;
        }
    }
    return count;
}


// Private function definitions

/* Doubles the capacity of a circular queue.

Keyword arguments:
queue -- The queue whose size will be doubled.
*/
static void cirque_resize(cirque* queue) {
    void** temp = malloc(queue->size * 2 * sizeof(void*));
    if (temp) {
        unsigned int i = 0;
        unsigned int h = queue->head;
        do {
            temp[i] = queue->entries[h++];
            h %= queue->size;
            i++;
        } while (h != queue->tail);
        free(queue->entries);
        queue->entries = temp;
        queue->head = 0;
        queue->tail = queue->size;
        queue->size *= 2;
        queue->is_full = 0;
    }
}

/* Checks to see if a circular queue is empty.

Keyword arguments:
queue -- The queue to check for elements.

Returns:
True iff the queue has no elements.
*/
static bool cirque_is_empty(const cirque* queue) {
    return (queue->head == queue->tail) && !queue->is_full;
}