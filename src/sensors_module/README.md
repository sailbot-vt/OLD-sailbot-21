# sensor_movement 

> Listens for generates sensor movement commands and triggers movement according using the `arduino` module.

### sensor_movement.py
Handles pubsub calls to `arduino` module.

### sensor_decision.py
Contains logic determining movement of sensor based on tracking data.

#### Decision Methodology
The base pattern for the sensor is a sweeping pattern that travels from -80deg to +80deg at a constant angular rate (defined in config).

When there are tracked objects within this 160deg aperture, `sensor_decision.py` will balance sweeping for new objects and updating positions on these objects. The importance of tracks is determined by a weighting of radial distance from boat, bearing distance from boat heading, bearing distance from current look direction, and time since last seen of object.
