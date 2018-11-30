//
// Created by William Cabell on 2018-11-30.
//


#ifndef consumer_list_h
#define consumer_list_h


#include "consumer.h"

// Structs

typedef struct ConsumerList ConsumerList;


// Functions

/*
 * Creates a new list of consumers.
 *
 * Returns:
 * A new, empty list of consumers.
 */
ConsumerList* create_consumer_list();


/*
 * Adds a new consumer to the list.
 *
 * Keyword arguments:
 * consumer_list -- The list to which to add the consumer.
 * consumer -- The consumer to add.
 */
void add_consumer(ConsumerList* consumer_list, Consumer* consumer);


/*
 * Removes a consumer from the list.
 *
 * Keyword arguments:
 * consumer_list -- The list to which to remove the consumer.
 * id -- The ID of the consumer to remove.
 */
Consumer remove_consumer(ConsumerList* consumer_list, char* id);


/*
 * Applies a function on each consumer in the list.
 *
 * KKeyword arguments:
 * consumer_list -- The list over which to iterate.
 * func -- A function taking a Consumer and returning void that will be applied to every consumer in the list.
 */
void foreach_consumer(ConsumerList* consumer_list, void (*func)(Consumer));


/*
 * Deallocates a list of consumers and every consumer in it. Sets the pointer to the list to NULL.
 *
 * Keyword arguments:
 * consumer_list -- The list to destroy.
 */
void destroy_consumer_list(ConsumerList** consumer_list);

#endif /* consumer_list_h */
