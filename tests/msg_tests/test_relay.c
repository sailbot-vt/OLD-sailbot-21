#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "test_relay.h"
#include "../../src/msg/relay.h"
#include "../../src/msg/subscriber.h"


#define NUM_TESTS 2


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_register_subscriber(void);
static void test_push_data(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_register_subscriber,
        test_push_data
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

Relay* relay;


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    relay = init_relay();
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    destroy_relay(&relay);
}


// Test Definitions

/*
 * Tests the register_subscriber_on_channel method.
 */
static void test_register_subscriber() {
    Subscriber sub1;
    sub1.channel_name = "test";
    sub1.id = "1";

    Subscriber sub2;
    sub2.channel_name = "test";
    sub2.id = "2";

    Subscriber sub3;
    sub3.channel_name = "test_b";
    sub3.id = "3";

    Subscriber sub4;
    sub4.channel_name = "test";
    sub4.id = "4";

    Subscriber sub5;
    sub5.channel_name = "test_b";
    sub5.id = "5";

    register_subscriber(relay, &sub1);
    register_subscriber(relay, &sub2);
    register_subscriber(relay, &sub3);
    register_subscriber(relay, &sub4);
    register_subscriber(relay, &sub5);

    Subscriber* result = remove_subscriber(relay, &sub1);
    assert(!strcmp(result->id, "1"));

    result = remove_subscriber(relay, &sub2);
    assert(!strcmp(result->id, "2"));

    result = remove_subscriber(relay, &sub3);
    assert(!strcmp(result->id, "3"));

    result = remove_subscriber(relay, &sub4);
    assert(!strcmp(result->id, "4"));

    result = remove_subscriber(relay, &sub5);
    assert(!strcmp(result->id, "5"));
}


/*
 * Tests the push_data_to_channel method.
 */
static void test_push_data() {
    Data data1;
    data1.size = 8;
    data1.data = malloc(data1.size);

    Data data2;
    data2.size = 8;
    data2.data = malloc(data2.size);

    push_data_to_channel(relay, "test", data1);
    push_data_to_channel(relay, "test", data2);

    // Not really anything to test

    free(data1.data);
    free(data2.data);
}
