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
    print("wind speed apparent: ", output.update_key("wind speed apparent"))
    print("wind speed true: ", output.update_key("wind speed true"))
    print("wind angle apparent: ", output.update_key("wind angle apparent"))
    print("wind angle true: ", output.update_key("wind angle true"))
    print("boat latitude: ", output.update_key("boat latitude"))
    print("boat longitude: ", output.update_key("boat longitude"))
    print("boat heading: ", output.update_key("boat heading"))
    print("boat speed: ", output.update_key("boat speed"))
    sleep(timeout)