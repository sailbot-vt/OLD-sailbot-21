""" Stores Airmar specific exceptions """

class InvalidIDException(Exception):
    "Sentence ID field provided is invalid."
    pass

class UnsupportedIDException(Exception):
    "Program does not support parse of given sentence type."
    pass

class InvalidSentenceException(Exception):
    "Sentence is not a valid nmea sentence."
    pass