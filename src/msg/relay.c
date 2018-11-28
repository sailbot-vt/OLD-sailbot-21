#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <pthread.h>
#include <Python.h>

#include "circular_queue.h"
#include "consumer.h"

#define NUM_CONSUMERS 5


// Structs

typedef struct arg_struct {
    void *dataPtr;
    int dataSize;
    PyObject* callback;
} arg_struct;


// Globals

int rc;

channel_table* hashArray[SIZE];
channel_table* dummyItem;
channel_table* item;


// Private Function Declarations

static void compare_names(void* name1, void* name2);
static void* create_shared_memory(size_t size);


// Functions

/*
 *
 */
int* create_buffer(char* channel_name, int data_size) {

    int* data_ptr = create_shared_memory(data_size);

//    printf("data pointer (from relay) = %p\n", dataPtr);

    insert_producer(channel_name, data_ptr, data_size);

//    pthread_t threads[1];

//    pthread_create(&threads[0], NULL, &notify_consumers, (int *) channelName);

    return *data_ptr;

}


/*
 * Finds the channel table with the specified channel name, if it exists.
 *
 * Keyword arguments:
 * channel_name -- The name of the channel for which to search.
 *
 * Returns:
 * A ptr to the channel_table struct with the right channel name.
 */
channel_table *search(char* channelName) {
    int hashIndex = hashCode(channelName);

    //move in array until an empty spot is found
    while (hashArray[hashIndex] != NULL && hashArray[hashIndex]->dataPtr != NULL) {
        if (hashArray[hashIndex]->channelName == channelName) {
            return hashArray[hashIndex];
        }

        ++hashIndex %= SIZE;
    }

    return NULL;
}


/*
 * Adds an entry to the array of producers.
 *
 * Keyword arguments:
 * channel_name -- The channel name of the producer.
 * data_ptr -- A ptr to the shared memory owned by the producer.
 */
void insert_producer(char* channelName, int *dataPtr) {
    channel_table *new_producer = (channel_table*)malloc(sizeof(channel_table));
    new_producer->dataPtr = dataPtr;
    new_producer->channelName = channelName;
    new_producer->consumers = (void*)malloc(NUM_CONSUMERS * sizeof(void*));


    int hashIndex = hashCode(channelName);

    // move in array until an empty or deleted cell is found
    while (hashArray[hashIndex] != NULL && hashArray[hashIndex]->channelName != -1) {
	    ++hashIndex %= SIZE;	// Go to next cell and wrap around the table
    }
    hashArray[hashIndex] = new_producer;
}

void insert_consumer(char* channelName, void* consumer) {
    
    //Adds consumer data callback to hashArray corresponding to desired channel

    int hashIndex = hashCode(channelName);
    while(hashArray[hashIndex] != NULL && hashArray[hashIndex]->channelName != channelName) {
        ++hashIndex;
        hashIndex %= SIZE;
    }

    printf("consumer = %p\n", consumer);
//    display_consumers(channelName);
    for(int i=0;i < NUM_CONSUMERS; i++) { 
        if(hashArray[hashIndex]->consumers[i] == NULL) {
	        hashArray[hashIndex]->consumers[i] = consumer;
            break;
	    }
    }
}

channel_table *delete(channel_table* item) {

    //Delete desired item from hashArray (eg: producer is done producing)

    int channelName = item->channelName;

    int hashIndex = hashCode(channelName);		//get the hash

    //move in array until non-empty cell is found
    while(hashArray[hashIndex] != NULL) {
        
        if(hashArray[hashIndex]->channelName == channelName) {
	    channel_table* temp = hashArray[hashIndex];

	    hashArray[hashIndex] = dummyItem;		//assign a dummy item at deleted position
	    return temp;
	}

    ++hashIndex;		//go to next cell
    hashIndex %= SIZE;		//wrap around the table

    }
    return NULL;
}

void display() {

    //Iterates through hashArray and creates visual representation (used for debugging)

    int i = 0;
//    int n = 0;
    for(i = 0; i<SIZE; i++) {

        if(hashArray[i] != NULL) {
            printf(" (%d,%p,%p)", hashArray[i]->channelName, hashArray[i]->dataPtr,hashArray[i]->consumers);
	    }
        else
	        printf(" ~~ ");
    }
    printf("\n");
}

void display_consumers(int channelName) {
 
    //Displays consumers registered to channel
    
/*    int *consumers [NUM_CONSUMERS] = { NULL };

    channel_table *item = search(channelName);

    strcpy(consumers, item->consumers);
*/
    int hashIndex = hashCode(channelName);
    while(hashArray[hashIndex] == NULL) {
	if(hashArray[hashIndex]->channelName != channelName) {
            ++hashIndex;
            hashIndex %= SIZE;
	}
    }

    for(int i=0;i < NUM_CONSUMERS; i++) { 
        if(hashArray[hashIndex]->consumers[i] == NULL) { 
	    printf("~~");
	}
	else {
	   printf("%p", consumers[i]);
	}
    }

    printf("\n");
    }

void *notify_consumers(int channelName,int dataSize, int *dataPtr) {
   
    //Creates thread for each consumer callback subscribed to a channel
    ///Error here -- Won't actually create a thread, but will just call the function using the consumer callback pointer


    // Call get_element() here

    void *(*consumers[NUM_CONSUMERS]) (void *ptr) = { NULL };

//    strcpy(consumers, search(channelName)->consumers);
    size_t cpy_size = NUM_CONSUMERS*sizeof(void *);
    int *search_addr = &(search(channelName)->consumers);
    memcpy(&consumers, search_addr, cpy_size);

    pthread_t threads [NUM_CONSUMERS];
    
    for(int n=0; n < NUM_CONSUMERS; n++) {
        printf("%p ", consumers[n]);
    }
    printf("\n");

//    display_consumers(channelName);
    for(int i=0; i < NUM_CONSUMERS; i++) {
	    if(consumers[i] != NULL) {
//	        printf("pthread_t object = %p\n", &(threads[i]));
	        void *newDataPtr = (void *)(dataPtr);
            printf("consumer notified = %p\n", consumers[i]);
            arg_struct callback_args;
            callback_args.dataPtr = newDataPtr;
            callback_args.dataSize = dataSize;
            callback_args.callback = (void*)consumers[i];
	        rc = pthread_create((&(threads[i])), NULL, &data_callback, (void* )&callback_args);
	        if(rc)  {
	            printf("Error: unable to create thread: %i\n", rc);
		        threads[i] = NULL;
	        }
        }
	    else {
	        threads[i] = NULL;
        }
    }

    for(int i=0; i <NUM_CONSUMERS; i++) {
        if(threads[i] != NULL) {
//            continue;
	        pthread_join(threads[i], NULL);
        }
    }
}


// Private Function Definitions

/*
 * Compares two channel names.
 *
 * Keyword arguments:
 * name1 -- The first channel name
 * name2 -- The second channel name
 *
 * Returns:
 * An int >, =, or < 0, if name1 >, =, or < name2.
 */
static int compare_names(void* name1, void* name2) {
    return strncmp((char*)name1, (char*)name2, 512);
}


/*
 * Creates a region of memory that any thread can access.
 *
 * Keyword arguments:
 * size -- The size (in bytes) of the region to create.
 *
 * Returns:
 * A void* to the newly created region.
 */
static void* create_shared_memory(size_t size) {
    int protection = PROT_READ | PROT_WRITE;
    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    return mmap(NULL, size * 8, protection, visibility, 0, 0);
}
