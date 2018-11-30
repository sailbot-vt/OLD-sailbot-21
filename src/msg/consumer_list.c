//
// Created by William Cabell on 2018-11-30.
//


#include <stdlib.h>
#include <string.h>


#include "consumer_list.h"


// Structs

typedef struct ConsumerNode {
    struct ConsumerNode* next_node;
    struct ConsumerNode* prev_node;
    Consumer* consumer;
} ConsumerNode;


struct ConsumerList {
    ConsumerNode* head;
    ConsumerNode* tail;
};


// Static function declarations

static ConsumerNode* find_consumer_node_by_id(ConsumerList* consumer_list, char* id);
static void free_consumer(Consumer* consumer);


// Functions

ConsumerList* create_consumer_list() {
    ConsumerList* new_list = (ConsumerList*)malloc(sizeof(struct ConsumerList));
    new_list->head = (ConsumerNode*)malloc(sizeof(ConsumerNode));
    new_list->tail = (ConsumerNode*)malloc(sizeof(ConsumerNode));

    new_list->head->prev_node = NULL;
    new_list->tail->next_node = NULL;

    new_list->head->next_node = new_list->tail;
    new_list->tail->prev_node = new_list->head;
}


void add_consumer(ConsumerList* consumer_list, Consumer* consumer) {
    ConsumerNode* new_node = (ConsumerNode*)malloc(sizeof(ConsumerNode));
    new_node->next_node = NULL;
    new_node->prev_node = consumer_list->tail;
    new_node->consumer = consumer;

    consumer_list->tail->next_node = new_node;
    consumer_list->tail = new_node;
}


Consumer remove_consumer(ConsumerList* consumer_list, char* id) {
    ConsumerNode* consumer = find_consumer_node_by_id(consumer_list, id);
    consumer->prev_node->next_node = consumer->next_node;
    consumer->next_node->prev_node = consumer->prev_node;

    Consumer local_copy = *consumer->consumer;

    free_consumer(consumer->consumer);
    free(consumer);

    return local_copy;
}


void foreach_consumer(ConsumerList* consumer_list, void (*func)(Consumer*)) {
    ConsumerNode* current = consumer_list->head->next_node;
    while (current != (ConsumerNode*)NULL) {
        func(current->consumer);
        current = current->next_node;
    }
}


void destroy_consumer_list(ConsumerList** consumer_list) {
    foreach_consumer(*consumer_list, free_consumer);

    ConsumerNode* current = (**consumer_list).head;
    while (current != (ConsumerNode*)NULL) {
        current = current->next_node;
        free(current->prev_node);
    }

    free(*consumer_list);
    *consumer_list = (ConsumerList*)NULL;
}


// Static functions

static ConsumerNode* find_consumer_node_by_id(ConsumerList* consumer_list, char* id) {
    ConsumerNode* current = consumer_list->head;
    while (current->consumer != (Consumer*)NULL
            && strcmp(current->consumer->id, id) != 0) {
        current = current->next_node;
    }
    return current;
}


// This should be tied to the Consumer struct and should be in the consumer module
static void free_consumer(Consumer* consumer) {
    free(consumer->callback);
    free(consumer);
}