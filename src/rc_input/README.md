# rc_input

> Detects RC inputs, scales them appropriately, and publishes events notifying the system of new inputs.

### `rc_input_thread.py`
Starts the event listening in RC receiver. Maybe this should go in `__init__.py`? Except that `__init__.py` is usually reserved for special purposes, and I don't know if this qualifies.

### `rc_receiver.py`
Contains functionality of an RC receiver, including a factory method to get configuration-specific receiver models.

### `rc_broadcasting.py`
Generates and publishes events based on inputs.

### `__init.py__`
Indicates that `rc_input` is a module.