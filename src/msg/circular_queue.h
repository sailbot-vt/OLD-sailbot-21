#ifndef circular_queue
#define circular_queue

#include <stdbool.h>

// Structs
typedef struct cirque {
    unsigned int head;
    unsigned int tail;
    bool is_full;
    void** entries;
    unsigned int size;
} cirque;

// Delegates
typedef void (*cirque_for_fn)(void*);

// Functions
cirque* cirque_create(void);
void cirque_empty(cirque* queue);
bool cirque_enqueue(cirque* queue, void* data);
void* cirque_dequeue(cirque* queue);
void* cirque_peek(const cirque* queue);
unsigned int cirque_get_count(const cirque* queue);
void cirque_for_each(const cirque* queue, cirque_for_fn fun);

#endif
/* circular_queue */