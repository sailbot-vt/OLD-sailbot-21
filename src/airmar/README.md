# airmar

> Detects serial data from airmar and parses NMEA0183 formatted sentences for relevent data. Data is broadcasted through pubsub by default.

## API

To start reading Airmar input and sending events, use the following code:
```python
from src.airmar.airmar_input_thread import AirmarInputThread

airmar_reader = AirmarInputThread()
airmar_reader.start()
```

### `airmar_input_thread.py`
Starts the event listening in airmar receiver.

### `airmar_receiver.py`
Contains the functionality of an airmar receiver, reads in messages from specified communication port.

### `airmar_processor.py`
Parses nmea sentences from airmar_receiver, sending them to be broadcasted.

For now, only supports readings for apparent/true wind and boat gps.
```python
# Broadcasted keys:
data = {
    "wind speed apparent" : float(), # meters per second
    "wind angle apparent" : float(), # 0 - 360 degrees
    "wind speed true": float() # meters per second
    "wind angle true": float() # 0 - 360 degrees
    "boat latitude": float() # nearest .0001 minute
    "boat longitude": float() # nearest .0001 minute
    "boat speed": float() # speed over ground km/hr nearest 0.1 kmh
    "boat heading": float() # degrees True, nearest 0.1 degree
}
```
### `config.yml`
Stores the pin and port configuration for the Airmar receiver as well as other configuration settings. See the header comment for formatting information.

### `config_reader.py`
Parses the YAML config file into Python.

### `prototype`
Using Testable Broadcaster:
```python
from src.airmar.airmar_input_thread import AirmarInputThread

from src.broadcaster.broadcaster import BroadcasterType

airmar = AirmarInputThread(broadcaster_type=BroadcasterType.Testable)
output = airmar.broadcaster 
# Broadcaster types: Testable, Messenger, FileWriter

airmar.start()
while True:
    print("wind speed apparent: ", output.update_key("wind speed apparent"))
    print("wind speed true: ", output.update_key("wind speed true"))
    print("wind angle apparent: ", output.update_key("wind angle apparent"))
    print("wind angle true: ", output.update_key("wind angle true"))
    print("boat latitude: ", output.update_key("boat latitude"))
    print("boat longitude: ", output.update_key("boat longitude"))
    print("boat heading: ", output.update_key("boat heading"))
    print("boat speed: ", output.update_key("boat speed"))
```
Using pubsub:
```python
from src.airmar.airmar_input_thread import AirmarInputThread

airmar = AirmarInputThread()
airmar.start()

class AirmarPubsub():
    def __init__(self):
        pub.subscribe(self.read_latitude, "boat latitude")
        pub.subscribe(self.read_longitude, "boat longitude")
        pub.subscribe(self.read_heading, "boat heading")
        # etc ...

    def read_latitude(self, latitude):
        return latitude

    def read_longitude(self, longitude):
        return longitude

    # etc ...
```