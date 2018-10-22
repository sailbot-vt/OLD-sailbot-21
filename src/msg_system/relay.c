#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <pthread.h>

#define SIZE 20
#define NUM_CONSUMERS 5

int pthread_create();

void* create_shared_memory(size_t size) {
    int protection = PROT_READ | PROT_WRITE;

    int visibility = MAP_SHARED | MAP_ANONYMOUS;

    return mmap(NULL, size, protection, visibility, 0, 0);
}

int consumers [NUM_CONSUMERS];
int rc;

struct channelTable {
    int *dataPtr;
    int channelName;
    int consumers [NUM_CONSUMERS];
};

struct channelTable* hashArray[SIZE];
struct channelTable* dummyItem;
struct channelTable* item;

int hashCode(int channelName) {
    return channelName % SIZE;
}

struct channelTable *search(int channelName) {
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

    struct channelTable *item = (struct channelTable*) malloc(sizeof(struct channelTable));
    item->dataPtr = dataPtr;
    item->channelName = channelName;

    int hashIndex = hashCode(channelName);		//get the hash

    //move in array until an empty or deleted cell is found
    while(hashArray[hashIndex] != NULL && hashArray[hashIndex]->channelName != -1) {
        ++hashIndex;		//go to the next cell
	hashIndex %= SIZE;	//wrap around the table

    }
    hashArray[hashIndex] = item;
}

void insert_consumer(int channelName, int consumer) {
    
    int hashIndex = hashCode(channelName);
    while(hashArray[hashIndex] != NULL && hashArray[hashIndex]->channelName != channelName) {
        ++hashIndex;
        hashIndex %= SIZE;
    }

    int i;
    for(i=0;i < NUM_CONSUMERS; i++) {
        
        if(hashArray[hashIndex]->consumers[i] == NULL) {
	    hashArray[hashIndex]->consumers[i] == consumer;
	}
    }
}

struct channelTable* delete(struct channelTable* item) {
    int channelName = item->channelName;

    int hashIndex = hashCode(channelName);		//get the hash

    //move in array until empty or deleted cell is found
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
    int i = 0;

    for(i = 0; i<SIZE; i++) {

        if(hashArray[i] != NULL)
	    printf(" (%d,%p)", hashArray[i]->channelName, hashArray[i]->dataPtr);
        else
	    printf(" ~~ ");
    }
    printf("\n");
}

void *notify_consumers(int channelName,int *dataPtr) {
//    consumers = search(channelName)->consumers;
    
    strcpy(consumers, search(channelName)->consumers);
    pthread_t threads [sizeof(consumers)];
    
    printf("Inside of notify_consumers\n");

    int i;
    for(i=0; i < sizeof(consumers) / sizeof(int); i++) {
//	rc = pthread_create(&threads[i], NULL, &consumers[i], (int *) data);
        rc = pthread_create(&threads[i], NULL, &consumers[i], (int *) dataPtr);  
    	if (rc)  {
	    printf("Error: unable to create thread");
	}
    }
    pthread_exit(NULL);
}
int create_buffer(int channelName, int dataSize) {
    
    int* dataPtr = create_shared_memory(dataSize*8);

//    printf("data pointer (from relay) = %p\n", dataPtr);

    insert_producer(channelName, dataPtr);

    pthread_t threads[1];

    pthread_create(&threads[0], NULL, &notify_consumers, (int *) channelName);

    return dataPtr;

}

/*int main() {

   dummyItem = (struct channelTable*) malloc(sizeof(struct channelTable));
   dummyItem->dataPtr = NULL;
   dummyItem->channelName = -1;

   insert(1, 20);
   insert(2, 70);
   insert(42, 80);
   insert(4, 25);
   insert(12, 44);
   insert(14, 32);
   insert(17, 11);
   insert(13, 78);
   insert(37, 97); 

   display();
   item = search(37);

   if(item != NULL) {
      printf("Element found: %i\n", item->dataPtr);
   } else {
      printf("Element not found\n");
   }

   delete(item);
   item = search(37);

   if(item != NULL) {
      printf("Element found: %i\n", item->dataPtr);
   } else {
      printf("Element not found\n");
   }
}

*/
