import sys
import types


module_name = 'Adafruit_BBIO'

# Create a type module_name
Adafruit_BBIO = types.ModuleType(module_name)
Adafruit_BBIO.GPIO = types.ModuleType(module_name + '.GPIO')

# Overwrite the default system module path to point to the type we just created
sys.modules[module_name] = Adafruit_BBIO
sys.modules[module_name + '.GPIO'] = Adafruit_BBIO.GPIO
