# airmar

> Detects serial data from airmar and parses nmeasentences to be broadcasted.

## API

To start reading Airmar input and sending events, use the following code:
```
from src.airmar.airmar_input_thread import AirmarInputThread

airmar_reader = AirmarInputThread()
airmar_reader.start()
```

To pause Airmar input reading without killing the thread, use
```
airmar.stop()
```
and to continue, just run
```
airmar.run()
```
again.

### `airmar_input_thread.py`
Starts the event listening in airmar receiver.

### `airmar_receiver.py`
Contains the functionality of an airmar receiver, reads in messages from port.

### `airmar_processor.py`
Parses nmea sentences from airmar_receiver, sending them to the broadcaster.

### `airmar_broadcaster.py`
Generates and publishes events based on inputs. Includes factory to get a testable broadcaster that records calls to the broadcaster.

### `config.yml`
Stores the pin and port configuration for the Airmar receiver as well as other configuration settings. See the header comment for formatting information.

### `config_reader.py`
Parses the YAML config file into Python.