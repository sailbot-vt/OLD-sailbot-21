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

     def cpu_temperature(self):
	"""
	Returns:
	A string that returns hardware temperatures in celcius.
	For Farenheit, specify fahrenheit as true.
	"""
	return psutil.sensors_temperatures(fahrenheit=False)

     def memory_usage(self):
	"""
	Returns:
	A string that contains information on total and available memory, as 		well as other memory info.
	"""
	return psutil.virtual_memory()
