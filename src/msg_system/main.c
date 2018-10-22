#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int register_to_produce_data();
int publish_data();
int register_to_consume_data();
void data_callback();

int channelName = 'sample';
int dataSize = 100;


int main() {
    
    int num;
    int n;
    int data[dataSize];
    for(n=0; n<100; n++) {
        srand(time(NULL));
        num = rand();
	data[n] = num;
    }

    register_to_produce_data(channelName, dataSize);
    register_to_consume_data(channelName, data_callback);

    printf("\n\nSTILL RUNNING\n\n\n");

    publish_data(channelName, dataSize, data);

    return 0;
}
