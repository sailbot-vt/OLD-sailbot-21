#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "test_circular_buffer.h"
#include "../../../src/msg/msg_types.h"
#include "../../../src/msg/circular_buffer.h"


#define NUM_TESTS 3


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_push(void);
static void test_get_element(void);
static void test_empty(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_push,
        test_get_element,
        test_empty
};


// Functions

void circular_buffer_all() {
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
CircularBuffer* buffer;


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    buffer = init_circular_buffer();
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    destroy_circular_buffer(&buffer);
}


// Test Definitions

/*
 * Tests the push method.
 */
static void test_push() {
    Data data1;
    Data data2;
    Data data3;

    data1.size = 8;
    data1.data = malloc(data1.size);

    data2.size = 16;
    data2.data = malloc(data2.size);

    data3.size = 24;
    data3.data = malloc(data3.size);

    CircularBufferElement index = circular_buffer_push(buffer, data1);

    assert(data1.data == circular_buffer_get_element(buffer, index).data);

    assert(false);
}


/*
 * Tests the get_element method.
 */
static void test_get_element() {
    assert(false);
}


/*
 * Tests the empty method.
 */
static void test_empty() {
    assert(false);
}
