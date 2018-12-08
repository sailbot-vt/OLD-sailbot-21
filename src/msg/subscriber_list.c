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


// Globals

pthread_mutex_t* mutex;


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

    pthread_mutexattr_t* pthread_mutexattr;
    pthread_mutexattr_init(pthread_mutexattr);
    pthread_mutex_init(mutex, pthread_mutexattr);
}


void add_subscriber(SubscriberList* subscriber_list, Subscriber* subscriber) {
    if (subscriber == (Subscriber*)NULL) {
        return;
    }

    pthread_mutex_lock(mutex);

    SubscriberNode* new_node = (SubscriberNode*)malloc(sizeof(SubscriberNode));
    new_node->next_node = NULL;
    new_node->prev_node = subscriber_list->tail;
    new_node->subscriber = subscriber;

    subscriber_list->tail->next_node = new_node;
    subscriber_list->tail = new_node;

    pthread_mutex_unlock(mutex);
}


Subscriber remove_subscriber(SubscriberList* subscriber_list, char* id) {
    pthread_mutex_lock(mutex);

    SubscriberNode* subscriber = find_subscriber_node_by_id(subscriber_list, id);

    subscriber->prev_node->next_node = subscriber->next_node;
    subscriber->next_node->prev_node = subscriber->prev_node;

    pthread_mutex_unlock(mutex);

    Subscriber local_copy = *subscriber->subscriber;
    destroy_subscriber(&subscriber->subscriber);

    return local_copy;
}


void foreach_subscriber(SubscriberList* subscriber_list, void (*func)(Subscriber*)) {
    SubscriberNode* current = subscriber_list->head->next_node;

    pthread_mutex_lock(mutex);

    while (current != (SubscriberNode*)NULL) {
        func(current->subscriber);
        current = current->next_node;
    }

    pthread_mutex_unlock(mutex);
}


void destroy_subscriber_list(SubscriberList** subscriber_list) {
    SubscriberNode* current = (**subscriber_list).head;

    pthread_mutex_lock(mutex);

    while (current != (SubscriberNode*)NULL) {
        current = current->next_node;
        free(current->prev_node);
    }

    free(*subscriber_list);
    *subscriber_list = (SubscriberList*)NULL;

    pthread_mutex_unlock(mutex);
    free(mutex);
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
