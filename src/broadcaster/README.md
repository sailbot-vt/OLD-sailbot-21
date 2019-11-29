# broadcaster

> Broadcaster class to broadcast data throughout SailBOT system. Supports writing to file, storing to dictionary, and pubsub

## API

To start broadcasting use the import the follow header:
```python
from src.broadcaster.broadcaster import Broadcaster, BroadcasterType, make_broadcaster
```

Specific usages:
```python
# To send messages to pubsub
b_messenger = Broadcaster() # = make_broadcaster(Broadcastertype.Messenger)
b_messenger.update_dictionary(data={"test":1})
assert 1 == b_messenger.update_key("test")

# To send messages to file
b_filewriter = make_broadcaster(BroadcasterType.FileWriter)

# To store messages to dictionary
b_testable = make_broadcater(BroadcasterType.Testable)
```