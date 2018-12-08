#include <stdlib.h>
#include <string.h>


#include "subscriber_list.h"
#include "subscriber.h"


// Structs

typedef struct SubscriberNode {
    struct SubscriberNode* next_node;
    struct SubcriberNode* prev_node;
    Subscriber* subscriber;
} SubscriberNode;


struct SubscriberList {
    SubscriberNode* head;
    SubscriberNode* tail;
};


// Static Function Declarations

static SubscriberNode* find_subscriber_node_by_id(SubscriberList* subscriber_list, char* id);


// Functions

SubscriberList* create_subscriber_list() {
    SubscriberList* new_list = (SubscriberList*)malloc(sizeof(struct SubscriberList));
    new_list->head = (SubscriberNode*)malloc(sizeof(SubscriberNode));
    new_list->tail = (SubscriberNode*)malloc(sizeof(SubscriberNode));

    new_list->head->prev_node = NULL;
    new_list->tail->next_node = NULL;

    new_list->head->next_node = new_list->tail;
    new_list->tail->prev_node = new_list->head;
}


void add_subscriber(SubscriberList* subscriber_list, Subscriber* subscriber) {
    if (subscriber == (Subscriber*)NULL) {
        return;
    }

    SubscriberNode* new_node = (SubscriberNode*)malloc(sizeof(SubscriberNode));
    new_node->next_node = NULL;
    new_node->prev_node = subscriber_list->tail;
    new_node->subscriber = subscriber;

    subscriber_list->tail->next_node = new_node;
    subscriber_list->tail = new_node;
}


Subscriber remove_subscriber(SubscriberList* subscriber_list, char* id) {
    SubscriberNode* subscriber = find_subscriber_node_by_id(subscriber_list, id);
    subscriber->prev_node->next_node = subscriber->next_node;
    subscriber->next_node->prev_node = subscriber->prev_node;

    Subscriber local_copy = *subscriber->subscriber;

    destroy_subscriber(&subscriber->subscriber);

    return local_copy;
}


void foreach_subscriber(SubscriberList* subscriber_list, void (*func)(Subscriber*)) {
    SubscriberNode* current = subscriber_list->head->next_node;
    while (current != (SubscriberNode*)NULL) {
        func(current->subscriber);
        current = current->next_node;
    }
}


void destroy_subscriber_list(SubscriberList** subscriber_list) {
    SubscriberNode* current = (**subscriber_list).head;
    while (current != (SubscriberNode*)NULL) {
        current = current->next_node;
        free(current->prev_node);
    }

    free(*subscriber_list);
    *subscriber_list = (SubscriberList*)NULL;
}


// Static Functions

static SubscriberNode* find_subscriber_node_by_id(SubscriberList* subscriber_list, char* id) {
    SubscriberNode* current = subscriber_list->head;
    while (current->subscriber != (Subscriber*)NULL
            && strcmp(current->subscriber->id, id) != 0) {
        current = current->next_node;
    }
    return current;
}
