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

# To send messages to file
b_filewriter = make_broadcaster(BroadcasterType.FileWriter)
b_filewriter.update_dictionary(data={"test":1})

# To store messages to dictionary
b_testable = make_broadcater(BroadcasterType.Testable)
b_testable.update_dictionary(data={"test":1})
```