#include <Python.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "../../../src/msg/subscriber.h"
#include "../../../src/msg/relay.h"
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

    static PyObject *test_callback = Py_None;


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

/*
 * Tests the subscribe and unsubscribe methods.
 */
static void test_subscribe_unsubscribe() { 
    Relay *test_relay = init_relay();
    Subscriber *test_subscriber = subscribe(test_relay, channel_name, test_callback);
    unsubscribe(test_relay, &test_subscriber);
}
