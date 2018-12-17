#ifndef subscriber_list_h
#define subscriber_list_h


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
SubscriberList* create_subscriber_list(void);


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
 * func -- A function taking a Subscriber and returning void that will be applied to every subscriber in the list.
 */
void foreach_subscriber(SubscriberList* subscriber_list, void (*func)(Subscriber*));


/*
 * Deallocates a list of subscribers and every subscriber in it. Sets the pointer to the list to NULL.
 *
 * Keyword arguments:
 * subscriber_list -- The list to destroy.
 */
void destroy_subscriber_list(SubscriberList** subscriber_list);

#endif /* subscriber_list_h */
