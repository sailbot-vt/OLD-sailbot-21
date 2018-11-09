# rudder

> Listens for rudder commands and affects the servo accordingly

### `rudder_driver.py`
Contains the instance of the thread that has a consumer and a RudderServoController.

### `rudder_servo_controller.py`
Class that has an instance of a servo with specifics of the servo and the
mechanical implantation of the servo's connection to the rudder.

### `__init.py__`
Indicates that `rudder` is a module.
