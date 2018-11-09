# rc_input

> Detects RC inputs, scales them appropriately, and publishes events notifying the system of new inputs.

## API

To start reading RC input and sending events, use the following code:
```
from src.rc_input.rc_input_thread import RCInputThread

rc_reader = RCInputThread()
rc_reader.start()
```

To pause RC input reading without killing the thread, use
```
rc_reader.stop()
```
and to continue, just run
```
rc_reader.run()
```
again.

### `rc_input_thread.py`
Starts the event listening in RC receiver. Maybe this should go in `__init__.py`? Except that `__init__.py` is usually reserved for special purposes, and I don't know if this qualifies.

### `rc_receiver.py`
Contains functionality of an RC receiver, including a factory method to get configuration-specific receiver models.

### `rc_broadcaster.py`
Generates and publishes events based on inputs. Includes factory to get a testable broadcaster that records calls to the broadcaster.

### `__init.py__`
Indicates that `rc_input` is a module.