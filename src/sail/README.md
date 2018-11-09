# sail

> Listens for sail commands and affects the servo accordingly

### `sail_trimmer.py`
Contains the instance of the thread that has a consumer and a sail_servo_controller.

### `sail_servo_controller.py`
Class that has an instance of a servo with specifics of the servo and the
mechanical implantation of the servo's connection to the sail.

### `__init.py__`
Indicates that `sail` is a module.
