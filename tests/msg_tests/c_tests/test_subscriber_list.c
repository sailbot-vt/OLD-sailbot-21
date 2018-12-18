#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>


#include "test_subscriber_list.h"
#include "../../../src/msg/msg_types.h"
#include "../../../src/msg/subscriber_list.h"
#include "../../../src/msg/subscriber.h"


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_add_subscriber(void);


// Globals

/*
 * NULL-terminated array of all test methods.
 */
Test tests[2] = {
        test_add_subscriber,
        (Test)NULL
};


// Functions

void subscriber_list_all() {
    int i = 0;
    while (tests[i] != (Test)NULL) {
        set_up();
        printf("Running test %d ... ", i);
        tests[i]();
        printf("passed.\n");  // Tests should halt execution of test suite on failure
        tear_down();
        i++;
    }
}


/********************************************************
 *****************       Tests          *****************
 ********************************************************/


// Test Globals

SubscriberList* list;
int counter;


// Test Helpers

static void increment(Subscriber*);


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    list = init_subscriber_list();
    counter = 0;
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    destroy_subscriber_list(&list);
}


// Test Definitions

/*
 * Tests the add_subscriber method.
 */
static void test_add_subscriber() {
    Subscriber* new_sub = malloc(sizeof(Subscriber));

    add_subscriber(list, new_sub);

    foreach_subscriber(list, increment);
    assert(1 == counter);

    free(new_sub);
    new_sub = malloc(sizeof(Subscriber));

    add_subscriber(list, new_sub);

    counter = 0;
    foreach_subscriber(list, increment);
    assert(2 == counter);

    free(new_sub);
}




// Test Helper Definitions

static void increment(Subscriber* _) {
    counter++;
}
