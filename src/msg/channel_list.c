//
// Created by William Cabell on 2018-11-30.
//

#include "channel_list.h"


// Structs

typedef struct ConsumerNode {
    struct ConsumerNode* next;
    Consumer* consumer;
} ConsumerNode;


struct ChannelList {
    ConsumerNode* head;
};


//