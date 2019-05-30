`nav`

> Takes waypoints and builds paths between them based on the conditions and the boat configuration.

`captain`

The `captain` module is the high-level API for the `nav` package. Methods available are:

- `waypoints_between(start, end, boat, wind)`

This will return a queue of waypoints between `start` and `end`. `start` and `end` must be `Waypoint`s.