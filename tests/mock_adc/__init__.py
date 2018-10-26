import sys
import types


module_name = 'Adafruit_BBIO'

# Create a type module_name
Adafruit_BBIO = types.ModuleType(module_name)
Adafruit_BBIO.ADC = types.ModuleType(module_name + '.ADC')

# Overwrite the default system module path to point to the type we just created
sys.modules[module_name] = Adafruit_BBIO
sys.modules[module_name + '.ADC'] = Adafruit_BBIO.ADC
