#include <stdlib.h>


#include "channel.h"
#include "msg_types.h"
#include "subscriber.h"


Channel* init_channel(char* name) {
    Channel* new_ch = (Channel*)malloc(sizeof(Channel));
    new_ch->name = name;
    new_ch->data_buffer = init_circular_buffer();
    new_ch->subscriber_list = init_subscriber_list();
    return new_ch;
}


CircularBufferElement publish_data(Channel* ch, Data data) {
    return circular_buffer_push(ch->data_buffer, data);
}


void add_subscriber_to_channel(Channel* ch, Subscriber* subscriber) {
    add_subscriber(ch->subscriber_list, subscriber);
}


void destroy_channel(Channel** ch) {
    destroy_circular_buffer(&(**ch).data_buffer);
    destroy_subscriber_list(&(**ch).subscriber_list);
    *ch = (Channel*)NULL;
}
