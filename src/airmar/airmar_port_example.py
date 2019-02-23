from src.airmar.airmar_input_thread import AirmarInputThread
from src.airmar.airmar_broadcaster import AirmarBroadcasterType

from time import sleep

airmar_reader = AirmarInputThread(broadcaster_type=AirmarBroadcasterType.Messenger)
broadcaster = airmar_reader.broadcaster

airmar_reader.start()
sleep(10000) # 10 seconds
airmar_reader.stop()

for x in broadcaster.boat_heads:
    print(x)

for x in broadcaster.boat_lats:
    print(x)

for x in broadcaster.boat_longs:
    print(x)

for x in broadcaster.boat_heads:
    print(x)

for x in broadcaster.boat_speeds:
    print(x)