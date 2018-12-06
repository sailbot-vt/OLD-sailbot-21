#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>


#include "test_consumer_list.h"
#include "../../../src/msg/msg_types.h"


// Delegates

typedef void (*Test)(void);


// Static Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_add_channel(void);


// Globals

/*
 * NULL-terminated array of all test methods.
 */
Test tests[2] = {
        test_add_channel,
        (Test)NULL
};


// Functions

void consumer_list_all() {
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


// Static Function Definitions

/*
 * Runs before each test method.
 */
static void set_up() {
    // Nothing to do here
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    // Nothing to do here
}


/********************************************************
 *****************       Tests          *****************
 ********************************************************/


// Test Globals


// Test Definitions

/*
 * Sample test method
 */
static void test_add_channel() {
    assert(false);
}
