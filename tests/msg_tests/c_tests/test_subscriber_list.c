#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdarg.h>


#include "test_subscriber_list.h"
#include "../../../src/msg/msg_types.h"
#include "../../../src/msg/subscriber_list.h"
#include "../../../src/msg/subscriber.h"


#define NUM_TESTS 3


// Delegates

typedef void (*Test)(void);


// Environment Setup Function Declarations

static void set_up(void);
static void tear_down(void);


// Test Declarations

static void test_add_subscriber(void);
static void test_remove_subscriber(void);
static void test_foreach_subscriber(void);


// Globals

/*
 * Array of all test methods.
 */
static Test tests[NUM_TESTS] = {
        test_add_subscriber,
        test_remove_subscriber,
        test_foreach_subscriber
};


// Functions

void subscriber_list_all() {
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

static SubscriberList* sub_list;
static char container[4] = {'\0'};
static int accumulator = 0;


// Test Helpers

static void concat(int index, Subscriber* sub, int argc, va_list argv);


// Environment Setup

/*
 * Runs before each test method.
 */
static void set_up() {
    sub_list = init_subscriber_list();
}


/*
 * Runs after each test method.
 */
static void tear_down() {
    destroy_subscriber_list(&sub_list);
}


// Test Definitions

/*
 * Tests the add_subscriber method.
 */
static void test_add_subscriber() {

    // Normal use cases

    Subscriber* new_sub = malloc(sizeof(Subscriber));

    add_subscriber(sub_list, new_sub);

    assert(1 == get_subscriber_list_size(sub_list));

    free(new_sub);
    new_sub = malloc(sizeof(Subscriber));

    add_subscriber(sub_list, new_sub);

    assert(2 == get_subscriber_list_size(sub_list));


    // Edge cases

    free(new_sub);
    new_sub = NULL;

    add_subscriber(sub_list, new_sub);

    assert(2 == get_subscriber_list_size(sub_list));
}


/*
 * Tests the remove_subscriber method.
 */
static void test_remove_subscriber() {

    // Normal use cases

    Subscriber* new_sub_1 = malloc(sizeof(Subscriber));
    new_sub_1->id = "a";

    add_subscriber(sub_list, new_sub_1);

    Subscriber* new_sub_2 = malloc(sizeof(Subscriber));
    new_sub_2->id = "b";

    add_subscriber(sub_list, new_sub_2);

    Subscriber* rmd = remove_subscriber_from_list(sub_list, new_sub_2->id);

    assert(!strcmp(rmd->id, new_sub_2->id));
    assert(1 == get_subscriber_list_size(sub_list));


    // Edge cases

    Subscriber* new_sub_3 = malloc(sizeof(Subscriber));
    new_sub_3->id = "c";

    rmd = remove_subscriber_from_list(sub_list, new_sub_3->id);

    assert(rmd == (Subscriber*)NULL);
    assert(1 == get_subscriber_list_size(sub_list));

    remove_subscriber_from_list(sub_list, new_sub_1->id);

    assert(0 == get_subscriber_list_size(sub_list));


    // Clean-up

    free(new_sub_1);
    free(new_sub_2);
    free(new_sub_3);
}


/*
 * Tests the foreach_subscriber method.
 */
static void test_foreach_subscriber() {

    // Normal use cases

    Subscriber* new_sub_1 = malloc(sizeof(Subscriber));
    new_sub_1->id = "a";
    add_subscriber(sub_list, new_sub_1);
    Subscriber* new_sub_2 = malloc(sizeof(Subscriber));
    new_sub_2->id = "b";
    add_subscriber(sub_list, new_sub_2);
    Subscriber* new_sub_3 = malloc(sizeof(Subscriber));
    new_sub_3->id = "c";
    add_subscriber(sub_list, new_sub_3);

    foreach_subscriber(sub_list, concat, 1, 2);

    assert(!strcmp("abc", container));
    assert(6 == accumulator);

    // Clean-up

    free(new_sub_1);
    free(new_sub_2);
    free(new_sub_3);
}


// Test Helper Definitions

static void concat(int index, Subscriber* sub, int argc, va_list argv) {
    int multiplier = va_arg(argv, int);
    accumulator += index * multiplier;

    strcat(container, sub->id);
}
