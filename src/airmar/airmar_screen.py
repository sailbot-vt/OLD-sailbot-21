import os
from time import sleep

from src.airmar.airmar_input_thread import AirmarInputThread
from src.broadcaster.broadcaster import BroadcasterType

airmar = AirmarInputThread(broadcaster_type=BroadcasterType.Testable)

output = airmar.broadcaster

def clear_screen():
    os.system('clear')
    os.system('cls')


airmar.run()

timeout = 4
while True:
    clear_screen()
    print("wind heading: ", output.read_data("wind heading"))
    print("wind speed: ", output.read_data("wind speed"))
    print("boat latitude: ", output.read_data("boat latitude"))
    print("boat longitude: ", output.read_data("boat longitude"))
    print("boat heading: ", output.read_data("boat heading"))
    print("boat speed: ", output.read_data("boat speed"))
    sleep(timeout)