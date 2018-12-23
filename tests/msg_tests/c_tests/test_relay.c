#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "test_relay.h"
#include "../../../src/msg/relay.h"


#define NUM_TESTS 3


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_register_subscriber(void);
static void test_push_data(void);
static void test_notify_subscribers(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_register_subscriber,
        test_push_data,
        test_notify_subscribers
};


// Functions

void relay_all() {
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
 * Tests the register_subscriber_on_channel method.
 */
static void test_register_subscriber() {
    assert(false);
}


/*
 * Tests the push_data_to_channel method.
 */
static void test_push_data() {
    assert(false);
}


/*
 * Tests the notify_subscribers_on_channel method.
 */
static void test_notify_subscribers() {
    assert(false);
}
