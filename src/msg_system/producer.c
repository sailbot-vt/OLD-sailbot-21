#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int data[ 100 ];

static int *dataPtr;

int create_buffer();
void display();

struct channelTable {
    int *dataPtr;
    int channelName;
};

struct channelTable* search();

int register_to_produce_data(int channelName, int dataSize) {
    
    dataPtr = create_buffer(channelName, dataSize); 

    display();

    return dataPtr;
}


int publish_data(int channelName, int dataSize, int data[]) {

	
    dataPtr = search(channelName)->dataPtr;

    printf("dataPtr = %p\n", dataPtr);

    memcpy(dataPtr,data, dataSize);

    //signal relay
    
    return 0;
}

int n = 0;

int main() {

    int num;
    
    for(n; n<100; n++) {
        srand(time(NULL));
        num = rand();
	data[n] = num;
    }
    
    int channelName = 'sample_run';
    int dataSize = 100;    

    register_to_produce_data(channelName, dataSize);

    publish_data(channelName, dataSize, data);

}
