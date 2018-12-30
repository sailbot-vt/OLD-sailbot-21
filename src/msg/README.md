# Messaging System

> Communication layer between all separate processes. Allows  processes to interact with each other without tight coupling and provides easy extensibility.

## API

To start the message system (do only once), use
```
import src.msg as msg

msg.start()
```

To broadcast a message, use the `publish` method:
```
import src.msg as msg

msg.publish("your_channel_name", your_generic_data)
```

To subscribe to a channel, create a `Subscriber` object:
```
import src.msg as msg

your_channel_name_subscriber = msg.Subscriber("your_channel_name", your_callback_function)

def your_callback_function(your_data):
    do_something(your_data)
```
The `Subscriber` will automatically unsubscribe when destroyed using the special Cython method `__dealloc__`, which, unlike `__del__`, is guaranteed to be called.

## Some Implementation Details

### Organization

The `relay` module stores a `ChannelList`. Each `Channel` in the list has a `SubscriberList` of all subscribers to that `Channel` and a `CircularBuffer` to store the data broadcast along that `Channel`. Each `Subscriber` stores its callback function as a `PyObject`.

When the `publish` method from the `publisher` module is called, a copy of the passed `Data` is created and pushed onto the `CircularBuffer` associated with the correct channel. Then the `notify_subscribers` method in the `relay` module is called, which runs the callback of each subscriber on the relevant channel in a separate POSIX thread.

### State Management

The Relay struct encapsulates the entire state of the message system. A relay is held in a persistent Python thread that is automatically queried by the endpoint API calls.

The relay essentially exposes an interface to semantic actions on a channel list. External modules can register a subscriber, push data onto a channel's buffer, and call the callback for all subscribers on a channel with a buffer index pointing to the data sent.

The relay handles the entire layer of interaction with the channel list. It creates a new channel if a subscriber with an unknown channel name is registered, deletes an empty channel if the last subscriber from a channel is removed, and skips publication of data to a nonexistent channel.

### Data Structures

#### Channel List

The channel list is an array-based list of channel structs. The list is sorted on addition. Addition is `O(n^2)`, access is `O(log n)`, and removal is `O(n)`.

An array based design was chosen since the standard library functions `qsort` and `bsearch` can be used for sorting and searching to ensure `O(log n)` access. Fast access is the priority for this data structure, since the structure is accessed every time data is published, which from a logical usage standpoint, should be at least as often as a channel is created, and probably much more often (there's no point in creating a channel and then not publishing data). Access must also occur whenever a subscriber is created or destroyed.

#### Circular Buffer

The `CircularBuffer` holds an array of `Data` objects: essentially, tuples of a void pointer and the size of its associated data in bytes. The buffer has a maximum size specified by `MAX_BUFFER_SIZE`, which acts as a last-resort real-time measure to cut off any functions using especially old data, since pushing to the buffer will overwrite the oldest element when the buffer is full.

The circular buffer is not sorted and since it is essentially a fancy array wrapper, additions are `O(1)` and access is `O(1)`.

#### Subscriber List

A basic linked list of subscribers, including an iterator that is as powerful as possible given the restrictions of the C language (i.e. without closures).

The primary action on the subscriber list is an agnostic iteration over all elements (when calling each subscriber's callback), so a linked list structure is logical.