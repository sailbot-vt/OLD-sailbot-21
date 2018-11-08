# Messaging System

> Communication Layer between all separate processes... Allows for processes to interact with eachother while providing a level of separation

## consumer.c

### Functions

1. register_to_consume_data(int <channelName>, void\* <callback>)

```
Register with relay to consume data on channelName
Will now be called by notify_consumers upon data being published on channelName
```

2. data_callback(void \*<dataPtr>)

```
Dereference data and pass to data_callback
data_callback will call a cython function, which will serve as an intermediary to the pyton data_callback
```

## producer.c

### Functions

1. register_to_produce_data(int <channelName>, int <dataSize>)

```
Register with relay to produce data on channelName
Producer and dataPtr to publishing address are stored in hashArray by relay
```

2. publish_data(int <channelName>, int <dataSize>, int \*<sourcePtr>)

```
Receives sourcePtr to data and pushes it to shared memory
Notifies relay so that it can notify_consumers on this channel
```
 
## relay.c

### Functions

