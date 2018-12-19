#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "test_channel_list.h"
#include "../../../src/msg/channel_list.h"
#include "../../../src/msg/channel.h"


#define NUM_TESTS 3


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_add_channel(void);
static void test_remove_channel(void);
static void test_get_channel(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_add_channel,
        test_remove_channel,
        test_get_channel
};


// Functions

void channel_list_all() {
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

ChannelList* list;


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    list = init_channel_list();
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    destroy_channel_list(&list);
}


// Test Definitions

/*
 * Tests the add_subscriber method.
 */
static void test_add_channel() {

    // Normal use cases

    assert(false);


    // Edge cases

}


/*
 * Tests the remove_subscriber method.
 */
static void test_remove_channel() {

    // Normal use cases

    assert(false);


    // Edge cases



    // Clean-up
}


/*
 * Tests the foreach_subscriber method.
 */
static void test_get_channel() {

    // Normal use cases

    assert(false);


    // Clean-up

}
