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
Starts the event listening in RC receiver.

### `rc_receiver.py`
Contains the functionality of an RC receiver, scaling inputs and sending them to the broadcaster.

### `rc_broadcaster.py`
Generates and publishes events based on inputs. Includes factory to get a testable broadcaster that records calls to the broadcaster.

### `config.yml`
Stores the pin configuration for the RC receiver as well as other configuration settings. See the header comment for formatting information.

### `config_reader.py`
Parses the YAML config file into Python.