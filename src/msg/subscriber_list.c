#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdarg.h>


#include "subscriber_list.h"
#include "subscriber.h"


// Structs

typedef struct SubscriberNode {
    struct SubscriberNode* next_node;
    struct SubscriberNode* prev_node;
    Subscriber* subscriber;
} SubscriberNode;


struct SubscriberList {
    SubscriberNode* head;
    SubscriberNode* tail;
    pthread_mutex_t mutex;
    int size;
};


// Static Function Declarations

static SubscriberNode* find_subscriber_node_by_id(SubscriberList* subscriber_list, char* id);


// Functions

SubscriberList* init_subscriber_list() {
    SubscriberList* new_list = (SubscriberList*)malloc(sizeof(struct SubscriberList));
    new_list->head = (SubscriberNode*)malloc(sizeof(SubscriberNode));
    new_list->tail = (SubscriberNode*)malloc(sizeof(SubscriberNode));

    new_list->head->prev_node = NULL;
    new_list->tail->next_node = NULL;

    new_list->head->next_node = new_list->tail;
    new_list->tail->prev_node = new_list->head;

    new_list->size = 0;

    pthread_mutex_init(&new_list->mutex, NULL);

    return new_list;
}


void add_subscriber(SubscriberList* subscriber_list, Subscriber* subscriber) {
    if (subscriber == (Subscriber*)NULL) {
        return;
    }

    pthread_mutex_lock(&subscriber_list->mutex);

    SubscriberNode* new_node = (SubscriberNode*)malloc(sizeof(SubscriberNode));
    new_node->next_node = subscriber_list->tail;
    new_node->prev_node = subscriber_list->tail->prev_node;
    new_node->subscriber = subscriber;

    subscriber_list->tail->prev_node->next_node = new_node;
    subscriber_list->tail->prev_node = new_node;

    subscriber_list->size++;

    pthread_mutex_unlock(&subscriber_list->mutex);
}


Subscriber* remove_subscriber(SubscriberList* subscriber_list, char* id) {
    pthread_mutex_lock(&subscriber_list->mutex);

    SubscriberNode* subscriber_node = find_subscriber_node_by_id(subscriber_list, id);

    if (subscriber_node == (SubscriberNode*)NULL) {
        pthread_mutex_unlock(&subscriber_list->mutex);
        return (Subscriber*)NULL;
    }

    subscriber_node->prev_node->next_node = subscriber_node->next_node;
    subscriber_node->next_node->prev_node = subscriber_node->prev_node;

    subscriber_list->size--;

    pthread_mutex_unlock(&subscriber_list->mutex);

    Subscriber* removed = subscriber_node->subscriber;
    free(subscriber_node);

    return removed;
}


void foreach_subscriber(SubscriberList* subscriber_list, void (*func)(int, Subscriber*, int, va_list), int argc, ...) {
    va_list argv;
    va_start(argv, argc);

    SubscriberNode* current = subscriber_list->head->next_node;

    pthread_mutex_lock(&subscriber_list->mutex);

    int index = 0;
    while (current != subscriber_list->tail) {
        va_start(argv, argc);
        func(index, current->subscriber, argc, argv);
        current = current->next_node;
        index++;
    }

    pthread_mutex_unlock(&subscriber_list->mutex);

    va_end(argv);
}


int get_subscriber_list_size(SubscriberList* list) {
    return list->size;
}


void destroy_subscriber_list(SubscriberList** subscriber_list) {
    SubscriberNode* current = (**subscriber_list).head;

    pthread_mutex_lock(&(*subscriber_list)->mutex);

    while (current->next_node != (SubscriberNode*)NULL) {
        current = current->next_node;
        free(current->prev_node);
    }
    free(current);

    pthread_mutex_unlock(&(*subscriber_list)->mutex);

    free(*subscriber_list);
    *subscriber_list = (SubscriberList*)NULL;

}


// Static Functions

static SubscriberNode* find_subscriber_node_by_id(SubscriberList* subscriber_list, char* id) {
    SubscriberNode* current = subscriber_list->head->next_node;
    while (current != subscriber_list->tail
            && strcmp(current->subscriber->id, id) != 0) {
        current = current->next_node;
    }

    if (current == subscriber_list->tail) {
        return (SubscriberNode*)NULL;
    }

    return current;
}
