#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <pthread.h>
#include <Python.h>

#include "consumer.h"

#define SIZE 20
#define NUM_CONSUMERS 100
#define QUEUE_LENGTH 256

// Structs

typedef struct arg_struct {
    void *dataPtr;
    int dataSize;
    PyObject* callback;
} arg_struct;


// Globals

int consumers [NUM_CONSUMERS];
int rc;

channel_table* hashArray[SIZE];
channel_table* dummyItem;
channel_table* item;


// Private Function Declarations

void* create_shared_memory(size_t size);
int hashCode(char channelName);


// Functions

channel_table *search(char channelName) {

    //Searches hashArray and returns channel_table object corresponding to channelName (if that object exists)

    //get the hash
    int hashIndex = hashCode(channelName);

    //move in array until a filled spot is found
    while (hashArray[hashIndex] != NULL && hashArray[hashIndex]->dataPtr != NULL) {
    
    //search using bsearch

	    if (hashArray[hashIndex]->channelName == channelName) {

            return hashArray[hashIndex];
        
        }
	    ++hashIndex;		//go to next cell
	    hashIndex %= SIZE; 	//wrap around the table
    }

    return NULL;
}

void insert_producer(char channelName, int *dataPtr) {

    //Makes entry into hashArray containing channnelName and data ptr

    channel_table *item = (channel_table*) malloc(sizeof(channel_table));
    item->dataPtr = dataPtr;
    item->channelName = channelName;
    void *consumers [ NUM_CONSUMERS ] = { NULL };
//    for(int i = 0; i<NUM_CONSUMERS;i++) {
//        consumers[i] = NULL;
//    }
    strcpy(item->consumers, consumers);

    int hashIndex = hashCode(channelName);		//get the hash

    //move in array until an empty or deleted cell is found
    while(hashArray[hashIndex] != NULL && hashArray[hashIndex]->channelName != -1) {
        ++hashIndex;		//go to the next cell
	hashIndex %= SIZE;	//wrap around the table

    }
    hashArray[hashIndex] = item;

    //SORT USING qsort
}

void insert_consumer(char channelName, void* consumer) {
    
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

channel_table* delete(channel_table* item) {

    //Delete desired item from hashArray (eg: producer is done producing)

    char channelName = item->channelName;

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

void display_consumers(char channelName) {
 
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

void *notify_consumers(char channelName,int dataSize, int *dataPtr) {
   
    //Creates thread for each consumer callback subscribed to a channel
    ///Error here -- Won't actually create a thread, but will just call the function using the consumer callback pointer

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

int create_buffer(char channelName, int dataSize) {
   
    //Returns data ptr to shared memory allocated to channel

    int* dataPtr = create_shared_memory(dataSize * QUEUE_LENGTH);        //WHAT IS LENGTH OF QUEUE??

//    printf("data pointer (from relay) = %p\n", dataPtr);

    insert_producer(channelName, dataPtr);

//    pthread_t threads[1];

//    pthread_create(&threads[0], NULL, &notify_consumers, (int *) channelName);

    return *dataPtr;

}


// Private Function Definitions

static int hashCode(char channelName) {
    return channelName % SIZE;
}

static void* create_shared_memory(size_t size) {

    //Returns data ptr to shared memory which has been allocated to this producer

    int protection = PROT_READ | PROT_WRITE;  // Don't worry about fixed-width ints here, since mmap needs ints as arguments

    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    return mmap(NULL, size, protection, visibility, 0, 0);
}
