# `autopilot`

The autopilot package defines an autopilot that will keep the boat heading along a particular route.

### `autopilot`

The `autopilot` module defines an `Autopilot` class which listens for waypoint events. It updates the `route` module as necessary and calls the `helmsman` module at intervals.

The `helmsman` module calculates rudder angles and sends commands to the rudder.

The `route` module wraps a FIFO queue to store waypoints.

