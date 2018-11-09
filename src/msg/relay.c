#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <pthread.h>
#include <Python.h>

#define SIZE 20
#define NUM_CONSUMERS 5

int pthread_create();

void *data_callback(void *dataPtr, int dataSize, PyObject* callback);
struct arg_struct {
    void *dataPtr;
    int dataSize;
    PyObject* callback;
};


void* create_shared_memory(size_t size) {
    
    //Returns data ptr to shared memory which has been allocated to this producer
	
    int protection = PROT_READ | PROT_WRITE;                    //inttypes.h -- fixed width integers

    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    return mmap(NULL, size, protection, visibility, 0, 0);
}

int consumers [NUM_CONSUMERS];
int rc;

struct channelTable {
    int *dataPtr;
    int channelName;
    void (*consumers[NUM_CONSUMERS]);
};

struct channelTable* hashArray[SIZE];
struct channelTable* dummyItem;
struct channelTable* item;

int hashCode(int channelName) {
    return channelName % SIZE;
}

struct channelTable *search(int channelName) {

    //Searches hashArray and returns channelTable object corresponding to channelName (if that object exists)

    //get the hash
    int hashIndex = hashCode(channelName);

    //move in array until an empty spot is found
    while(hashArray[hashIndex] != NULL && hashArray[hashIndex]->dataPtr != NULL) {
        
	if(hashArray[hashIndex]->channelName == channelName)
            return hashArray[hashIndex];

	++hashIndex;		//go to next cell
	hashIndex %= SIZE; 	//wrap around the table
    }

    return NULL;
}

void insert_producer(int channelName, int *dataPtr) {

    //Makes entry into hashArray containing channnelName and data ptr

    struct channelTable *item = (struct channelTable*) malloc(sizeof(struct channelTable));
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
}

void insert_consumer(int channelName, void* consumer) {
    
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

struct channelTable* delete(struct channelTable* item) {

    //Delete desired item from hashArray (eg: producer is done producing)

    int channelName = item->channelName;

    int hashIndex = hashCode(channelName);		//get the hash

    //move in array until non-empty cell is found
    while(hashArray[hashIndex] != NULL) {
        
        if(hashArray[hashIndex]->channelName == channelName) {
	    struct channelTable* temp = hashArray[hashIndex];

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

    struct channelTable *item = search(channelName);

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
            struct arg_struct callback_args;
            callback_args.dataPtr = newDataPtr;
            callback_args.dataSize = dataSize;
            callback_args.callback *consumers[i];
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

int create_buffer(int channelName, int dataSize) {
   
    //Returns data ptr to shared memory allocated to channel

    int* dataPtr = create_shared_memory(dataSize*8);

//    printf("data pointer (from relay) = %p\n", dataPtr);

    insert_producer(channelName, dataPtr);

//    pthread_t threads[1];

//    pthread_create(&threads[0], NULL, &notify_consumers, (int *) channelName);

    return *dataPtr;

}

