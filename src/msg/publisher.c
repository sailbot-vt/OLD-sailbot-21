#include <sys/types.h>
#include <sys/mman.h>
#include <string.h>


#include "publisher.h"
#include "msg_types.h"
#include "relay.h"


// Private Function Declarations

/*
 * Creates thread-shared memory.
 *
 * Keyword arguments:
 * size -- The number of bytes of shared memory to allocate.
 *
 * Returns:
 * A pointer to the shared memory.
 */
static void* create_shared_memory(size_t size);


// Functions

void publish(char* channel_name, void* data, size_t data_size) {
    Data* data_wrapper = (Data*)malloc(sizeof(Data));
    data_wrapper->data = create_shared_memory(data_size);
    data_wrapper->size = data_size;
    memcpy(data_wrapper->data, data, data_size);

    notify_subscribers(channel_name, push_data_to_msg_buffer(data_wrapper));
}


// Private Function Definitions

static void* create_shared_memory(size_t size) {
    int protection = PROT_READ | PROT_WRITE;
    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    void* new_addr = mmap(NULL, size, protection, visibility, 0, 0);
    return new_addr;
}