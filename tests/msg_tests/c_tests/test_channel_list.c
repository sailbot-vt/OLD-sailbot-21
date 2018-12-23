#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>


#include "test_channel_list.h"
#include "../../../src/msg/channel_list.h"
#include "../../../src/msg/channel.h"


#define NUM_TESTS 2


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_add_channel(void);
static void test_remove_channel(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_add_channel,
        test_remove_channel
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

static ChannelList* ch_list;


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    ch_list = init_channel_list();
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    destroy_channel_list(&ch_list);
}


// Test Definitions

/*
 * Tests the add_channel method.
 */
static void test_add_channel() {

    // Normal use cases

    Channel* channel_1 = init_channel("1");
    Channel* channel_2 = init_channel("2");
    Channel* channel_3 = init_channel("3");

    add_channel(ch_list, channel_1);

    assert(channel_1 == get_channel(ch_list, "1"));

    add_channel(ch_list, channel_2);

    assert(channel_1 = get_channel(ch_list, "1"));
    assert(channel_2 = get_channel(ch_list, "2"));

    add_channel(ch_list, channel_3);

    assert(channel_3 = get_channel(ch_list, "3"));
    assert(channel_2 = get_channel(ch_list, "2"));
    assert(channel_1 = get_channel(ch_list, "1"));


    // Clean-up

    destroy_channel(&channel_1);
    destroy_channel(&channel_2);
    destroy_channel(&channel_3);
}


/*
 * Tests the remove_channel method.
 */
static void test_remove_channel() {

    // Normal use cases

    Channel* channel_1 = init_channel("1");
    Channel* channel_2 = init_channel("2");

    add_channel(ch_list, channel_1);
    add_channel(ch_list, channel_2);

    assert(channel_1 == remove_channel(ch_list, "1"));

    assert((Channel*)NULL == get_channel(ch_list, "1"));
    assert(channel_2 == get_channel(ch_list, "2"));

    assert(channel_2 == remove_channel(ch_list, "2"));

    assert((Channel*)NULL == get_channel(ch_list, "2"));


    // Edge cases

    assert((Channel*)NULL == remove_channel(ch_list, "nonexistent channel"));


    // Clean-up

    destroy_channel(&channel_1);
    destroy_channel(&channel_2);
}
