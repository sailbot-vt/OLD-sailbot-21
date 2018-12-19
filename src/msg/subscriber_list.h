#ifndef subscriber_list_h
#define subscriber_list_h


#include <stdarg.h>


#include "subscriber.h"


// Structs

typedef struct SubscriberList SubscriberList;


// Functions

/*
 * Creates a new list of subscribers.
 *
 * Returns:
 * A new, empty list of subscribers.
 */
SubscriberList* init_subscriber_list(void);


/*
 * Adds a new subscribers to the list.
 *
 * Keyword arguments:
 * subscriber_list -- The list to which to add the subscriber.
 * subscriber -- The subscriber to add.
 */
void add_subscriber(SubscriberList* subscriber_list, Subscriber* subscriber);


/*
 * Removes a subscriber from the list and destroys the subscriber struct associated with it.
 *
 * Keyword arguments:
 * subscriber_list -- The list to which to remove the subscriber.
 * id -- The ID of the subscriber to remove.
 */
Subscriber* remove_subscriber(SubscriberList* subscriber_list, char* id);


/*
 * Applies a function on each subscriber in the list.
 *
 * Keyword arguments:
 * subscriber_list -- The list over which to iterate.
 * func -- A function that will be applied for every subscriber in the list.
 *
 *     func should have a prototype
 *
 *         void func(int index, Subscriber* subscriber, int argc, va_list argv);
 *
 *     The variable parameters passed to foreach_subscriber will be applied to func in order, as
 *
 *         func(index, subscriber, argc, param1, param2, param3, ..., param[argc])
 *
 * argc -- The number of other arguments to be passed.
 * ... -- The argc other arguments
 */
void foreach_subscriber(SubscriberList* subscriber_list, void (*func)(int, Subscriber*, int, va_list), int argc, ...);


/*
 * Gets the number of subscribers in a SubscriberList.
 *
 * Keyword arguments:
 * list -- The list to count.
 */
int get_subscriber_list_size(SubscriberList* list);

/*
 * Deallocates a list of subscribers and every subscriber in it. Sets the pointer to the list to NULL.
 *
 * Keyword arguments:
 * subscriber_list -- The list to destroy.
 */
void destroy_subscriber_list(SubscriberList** subscriber_list);

#endif /* subscriber_list_h */
