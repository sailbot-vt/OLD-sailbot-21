#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int register_to_produce_data();
int publish_data();
int register_to_consume_data();
void data_callback();
void data_callback_2();

void (*callback)(void *) = &data_callback;
void (*callback_2)(void *) = &data_callback_2;

int channelName = "sample";
int channelName2 = "diff";
int dataSize = 100;


int main() {

    int n;
    int data[dataSize];
    for(n=0; n<100; n++) {
	data[n] = n;
    }

//  printf("First 4 ints (from main) = %i %i %i %i\n", data[0], data[1], data[2], data[3]);
    
    register_to_produce_data(channelName, dataSize);
    register_to_consume_data(channelName, callback);
    register_to_consume_data(channelName, callback_2);

    publish_data(channelName, dataSize, &data);

    return 0;
}
