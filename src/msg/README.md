# Messaging System

> Communication layer between all separate processes. Allows  processes to interact with each other without tight coupling and provides easy extensibility.

## API

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

## Organization

The `relay` module stores a `ChannelList`. Each `Channel` in the list has a `SubscriberList` of all subscribers to that `Channel` and a `CircularBuffer` to store the data broadcast along that `Channel`. Each `Subscriber` stores its callback function as a `PyObject`.

When the `publish` method from the `publisher` module is called, a copy of the passed `Data` is created and pushed onto the `CircularBuffer` associated with the correct channel. Then the `notify_subscribers` method in the `relay` module is called, which runs the callback of each subscriber on the relevant channel in a separate POSIX thread.

The `CircularBuffer` holds an array of `Data` objects: essentially, tuples of a void pointer and the size of its associated data in bytes. The buffer has a maximum size specified by `MAX_BUFFER_SIZE`, which acts as a redundant real-time measure to cut off any functions using especially old data, since pushing to the buffer will overwrite the oldest element when the buffer is full.