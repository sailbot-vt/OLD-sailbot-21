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
    print("wind speed apparent: ", output.read_data("wind speed apparent"))
    print("wind speed true: ", output.read_data("wind speed true"))
    print("wind angle apparent: ", output.read_data("wind angle apparent"))
    print("wind angle true: ", output.read_data("wind angle true"))
    print("boat latitude: ", output.read_data("boat latitude"))
    print("boat longitude: ", output.read_data("boat longitude"))
    print("boat heading: ", output.read_data("boat heading"))
    print("boat speed: ", output.read_data("boat speed"))
    sleep(timeout)