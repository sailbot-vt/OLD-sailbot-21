#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "test_circular_buffer.h"
#include "../../../src/msg/msg_types.h"
#include "../../../src/msg/circular_buffer.h"


#define NUM_TESTS 2


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_push(void);
static void test_get_element(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_push,
        test_get_element
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

    data1.size = 0;
    data1.data = NULL;

    data2.size = 0;
    data2.data = NULL;

    data3.size = 0;
    data3.data = NULL;

    CircularBufferElement index = circular_buffer_push(buffer, data1);
    assert(index.index == 0);
    assert(index.revolution == 0);

    index = circular_buffer_push(buffer, data2);
    assert(index.index == 1);
    assert(index.revolution == 0);

    index = circular_buffer_push(buffer, data3);
    assert(index.index == 2);
    assert(index.revolution == 0);

    for (int i = 0; i < 297; ++i) {
        Data data;
        data.size = 0;
        data.data = NULL;
        circular_buffer_push(buffer, data);
    }

    index = circular_buffer_push(buffer, data1);

    // (2 + 297 + 1) % 256 == 300 % 256 == 44
    assert(index.index == 44);
    assert(index.revolution == 1);
}


/*
 * Tests the get_element method.
 */
static void test_get_element() {
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

    Data retrieved = circular_buffer_get_element(buffer, index);
    assert(data1.data == retrieved.data);
    assert(data1.size == retrieved.size);

    index = circular_buffer_push(buffer, data2);

    retrieved = circular_buffer_get_element(buffer, index);
    assert(data2.data == retrieved.data);
    assert(data2.size == retrieved.size);

    index = circular_buffer_push(buffer, data3);

    retrieved = circular_buffer_get_element(buffer, index);
    assert(data3.data == retrieved.data);
    assert(data3.size == retrieved.size);

    free(data1.data);
    free(data2.data);
    free(data3.data);
}