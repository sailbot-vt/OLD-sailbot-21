# nmeaparser

> Stores factory methods to parse NMEA 0183 standard sentences.

## API

To start parsing NMEA sentences use the following code:
```python
from src.airmar.nmeaparser.nmea_parser import NmeaParser

p = NmeaParser()
```

### `nmea_parser.py`
Contains functions used to parse NMEA sentence, and construct NMEA sentence for transmission.

### `nmea_sentence.py`
Contains classes correlating to NMEA sentence identifiers (sid). Can use factory method provided to obtain class object for parsing purposes:
```python 
get_sentence_interface(sentence_id:str) -> sentence_id(NmeaSentence)
``` 
