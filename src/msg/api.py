from src.msg.cython_subscriber import _Subscriber
from src.msg.cython_publisher import _publish


class Subscriber:
    def __init__(self, channel, callback=lambda data: None):
        """Subscribes to events on a channel. Calls the callback function whenever an event is detected.
        The callback is destroyed when its wrapper Subscriber is destroyed.

        channel -- The channel to subscribe to
        callback -- A callback function with a parameter to capture the data sent by the publisher
        """
        self.sub = _Subscriber()
        self.sub.subscribe(channel, callback)


def publish(channel, data):
    """Publishes data to a channel.

    Keyword arguments:
    channel -- The name of the channel to publish to (a string)
    data -- The data to send along the channel
    """
    _publish(channel, data)
