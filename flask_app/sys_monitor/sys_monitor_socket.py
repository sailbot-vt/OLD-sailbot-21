import psutil
from flask_socketio import Namespace, emit


class SysMonitorSocket(Namespace):

    def __init__(self, Namespace=None):
        super().__init__(Namespace)

    def cpu_usage(self):
	"""
	Returns:
	A string containing the cpu usage percent.
	"""
        return psutil.cpu_percent(interval=1)

     def cpu_temperature(self, degF):
	"""
	parameters:
	degF: boolean, specifies units of temperature: true for fahrenheit, false for celcius.
	Returns:
	A string that returns hardware temperatures in celcius.
	For Farenheit, specify fahrenheit as true.
	"""
	sensorTemp = psutil.sensors_temperatures(fahrenheit= degF)
	return sensorTemp

     def memory_usage(self):
	"""
	Returns:
	A string that contains information on total and available memory, as 		well as other memory info.
	"""
	memoryUse = psutil.virtual_memory()
	return memoryUse[2]
