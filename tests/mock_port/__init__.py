import sys
import types


module_name = 'serial'

# Create a type module_name
serial = types.ModuleType(module_name)
serial.Serial = types.ModuleType(module_name + '.Serial')

# Overwrite the default system module path to point to the type we just created
sys.modules[module_name] = serial
sys.modules[module_name + '.Serial'] = serial.Serial
