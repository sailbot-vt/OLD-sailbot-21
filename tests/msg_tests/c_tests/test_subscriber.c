#include <Python.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "../../../src/msg/subscriber.h"
#include "../../../src/msg/relay.h"
#include "../../../src/msg/channel.h"
#include "../../../src/msg/subscriber_list.h"
#include "../../../src/msg/channel_list.h"
#include "test_subscriber.h"


#define NUM_TESTS 1


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_subscribe_unsubscribe(void);
//NOTE --- Test of data_callback will be done from python
//         Need valid python function to make to be callback

// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_subscribe_unsubscribe
};


// Functions

void subscriber_all() {
    for (int i = 0; i < NUM_TESTS; i++) {
        set_up();
        printf("Running test %d ... ", i + 1);
        tests[i]();
        printf("passed.\n");  // Tests should halt execution of test suite on failure
        tear_down();
    }
}


/********************************************************
 *****************       Tests          *****************
 ********************************************************/


// Test Globals

char *channel_name = "test";

// For some reason, some Python.h types are available and some aren't
// Py_None isn't available for some reason, so do either this or #define Py_None NULL
static PyObject *test_callback = (PyObject*)NULL;


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    // Tests not implemented
}


/*
 * Runs after each test method.
 */
static void tear_down() { 
    // Tests not implemented
}


// Test Definitions


// External Structs

struct Relay {
    ChannelList *channel_list;
    pthread_mutex_t mutex;
};

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

// External Static Funcs

static SubscriberNode* find_subscriber_node_by_id(SubscriberList* subscriber_list, char* id) {
    SubscriberNode* current = subscriber_list->head->next_node;
    while (current != subscriber_list->tail
            && strcmp(current->subscriber->id, id) !=  0) {
        current = current->next_node;
    }

    if (current == subscriber_list->tail) {
        return (SubscriberNode*)NULL;
    }

    return current;
}

/*
 * Tests the subscribe and unsubscribe methods.
 */
static void test_subscribe_unsubscribe() { 
    Relay *test_relay = init_relay();

    Subscriber *test_subscriber = subscribe(test_relay, channel_name, test_callback);

    unsubscribe(test_relay, test_subscriber);

//    ChannelList *test_ch_list = test_relay->channel_list;

//    Channel* test_channel = get_channel(test_ch_list, test_subscriber->channel_name);

//    SubscriberList *test_sub_list = test_channel->subscriber_list;

//    assert(find_subscriber_node_by_id(test_sub_list, test_subscriber->id)==(SubscriberNode*)NULL);

    assert(find_subscriber_node_by_id(get_channel(test_relay->channel_list, test_subscriber->channel_name)->subscriber_list, test_subscriber->id)==(SubscriberNode*)NULL);
//    assert(false);  // The test shouldn't pass unless it's finished
}
