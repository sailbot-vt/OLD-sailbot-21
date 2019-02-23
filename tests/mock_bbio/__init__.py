import sys
import types


module_name = 'Adafruit_BBIO'

# Create a type module_name
Adafruit_BBIO = types.ModuleType(module_name)
Adafruit_BBIO.GPIO = types.ModuleType(module_name + '.GPIO')
Adafruit_BBIO.ADC = types.ModuleType(module_name + '.ADC')
Adafruit_BBIO.PWM = types.ModuleType(module_name + '.PWM')
Adafruit_BBIO.UART = types.ModuleType(module_name + '.UART')

# Overwrite the default system module path to point to the type we just created
sys.modules[module_name] = Adafruit_BBIO
sys.modules[module_name + '.GPIO'] = Adafruit_BBIO.GPIO
sys.modules[module_name + '.ADC'] = Adafruit_BBIO.ADC
sys.modules[module_name + '.PWM'] = Adafruit_BBIO.PWM
sys.modules[module_name + '.UART'] = Adafruit_BBIO.UART
