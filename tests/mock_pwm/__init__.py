import sys
import types


module_name = 'Adafruit_BBIO'

# Create a type module_name
Adafruit_BBIO = types.ModuleType(module_name)
Adafruit_BBIO.PWM = types.ModuleType(module_name + '.PWM')

# Overwrite the default system module path to point to the type we just created
sys.modules[module_name] = Adafruit_BBIO
sys.modules[module_name + '.PWM'] = Adafruit_BBIO.PWM
