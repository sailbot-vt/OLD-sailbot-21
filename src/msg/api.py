from src.msg.cython_subscriber import _Subscriber
from src.msg.cython_publisher import _publish
from src.msg.cython_relay import MsgThread


msg_thread = None


def start():
    """Starts the message system."""
    global msg_thread
    if msg_thread is None:
        msg_thread = MsgThread()
        msg_thread.start()


class Subscriber:
    def __init__(self, channel, callback=lambda data: None):
        """Subscribes to events on a channel. Calls the callback function whenever an event is detected.
        The callback is destroyed when its wrapper Subscriber is destroyed.

        channel -- The channel to subscribe to
        callback -- A callback function with a parameter to capture the data sent by the publisher
        """
        self.sub = _Subscriber()
        self.sub.subscribe(msg_thread.get_relay(), channel, callback)


def publish(channel, data):
    """Publishes data to a channel.

    Keyword arguments:
    channel -- The name of the channel to publish to (a string)
    data -- The data to send along the channel
    """
    _publish(msg_thread.get_relay(), channel, data)
