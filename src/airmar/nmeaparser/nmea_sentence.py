from abc import ABC, abstractmethod
import sys

class NmeaSentence(ABC):
    """ Interface for interpretting all transmitted NMEA 0183 Sentences 
    
    Refer to 300 WX User Technical Manual_0183 for descriptions of fields
    """
    @abstractmethod
    def update_data(nmea_map, fields):
        """ Adds/updates this sentence Key-Value pair to nmea_map 
        
        Note: 
        Values will be of NoneType or StringType, type conversions 
        is left to client.

        Dictionary format: 
        nmea_map["<sentence-id>"] = { "data_description" : "<sentence-fields>" }

        Side-effects:
        nmea_map will be updated with sentence key value pairs
        """
        pass

class GPDTM(NmeaSentence):
    def update_data(nmea_map, fields):
        nmea_map[fields[0]] = {
            # 3 letter alphabetical code for local datum
            "local_datum_code" : fields[1],
            # 1 letter subdivision datum code (when available)
            "subdivision_datum_code" : fields[2],
            # Latitude offset to the nearest .0001 minute
            "latitude_offset" : fields[3],
            # N/S if dtm_latitude_offset is North/South latitude
            "latitiude_cardinality" : fields[4],
            # Longitude offset to the nearest .0001 minute
            "longitude_offset" : fields[5],
            # E/W if dtm_longitude_offset is East/West longitude
            "longitude_cardinality" : fields[6],
            # Signed (+/-) altitude offset, to the nearest meter
            "altitude_offset" : fields[7],
            # 3 character reference datum code
            "reference_datum_code" : fields[8]
        } 


class GPGGA(NmeaSentence):
    def update_data(nmea_map, fields):
        nmea_map[fields[0]] = { 
            # UTC of position, in the form hhmmss
            "utc_position" : fields[1],
            # Latitude to the nearest .0001 minute
            "latitude" : fields[2],
            # N/S if gga_latitude is North/South latitude
            "latitude_cardinality" : fields[3],
            # Longitude to the nearest .0001 minute
            "longitude" : fields[4],
            # E/W if gga_longitude is East/West longitude
            "longitude_cardinality" : fields[5],
            # GPS quality indicator - refer to manual
            "gps_quality_indicator" : fields[6],
            # Number of satelites in use, 0-12
            "number_satelites" : fields[7],
            # Horizontal dilution of precision (hdop)
            "hdop" : fields[8],
            # Altitude relative to mean-sea-level (geoid), to the nearest meter
            "geoid" : fields[9]
        }


class GPGLL(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class GPGSA(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class GPGSV(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class HCHDG(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class HCHDT(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class WIMDA(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class WIMWD(NmeaSentence):
    def update_data(nmea_map, fields):
        nmea_map[fields[0]] = {
            # Wind direction True 0-359.9 degrees
            "wind_direction_true" : fields[1],
            # Wind direction Magnetic, 0-359.9 degrees
            "wind_direction_magnetic" : fields[3],
            # Wind speed knots
            "wind_speed_knots" : fields[5],
            # Wind speed meters per seconds
            "wind_speed_mps" : fields[7]
        } 


class WIMWV(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class GPRMC(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class TIROT(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class HCTHS(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class GPVTG(NmeaSentence):
    def update_data(nmea_map, fields):
        nmea_map[fields[0]] = {
            # Course over ground, degrees True, to the nearest 0.1 degree
            "course_over_ground_true" : fields[1],
            # Course over ground, degrees Magnetic, to the nearest 0.1 degree
            "course_over_ground_magnetic" : fields[3],
            # Speed over ground, knots, to the nearest 0.1 knot
            "speed_over_ground_knots" : fields[5],
            # Speed over ground km/hr to the nearest 0.1 km/hr
            "speed_over_ground_kph" : fields[7],
            # Mode indicator - refer to manual
            "mode_indicator" : fields[9]
        }


class WIVWR(NmeaSentence):
    def update_data(nmea_map, fields):
        nmea_map[fields[0]] = {
            # (Apparent) Wind angle relative to the vessel, 0-180 degree
            "wind_angle_degree" : fields[1],
            # L/R (left/right) of vessel heading
            "wind_angle_direction" : fields[2],
            # Wind speed in knots, to the nearest 0.1 knot
            "wind_speed_knots" : fields[3],
            # Wind speed, meters per second
            "wind_speed_mps" : fields[5],
            # Wind speed, km/hr
            "wind_speed_kph" : fields[7]
        }


        
class WIVWT(NmeaSentence):
    def update_data(nmea_map, fields):
        nmea_map[fields[0]] = {
            # True wind angle, 0-180, to the nearest degree
            "wind_angle_degree" : fields[1],
            # L/R (left/right) of vessel heading
            "wind_angle_direction" : fields[2],
            # Wind speed, knots, mps, kph
            "wind_speed_knots" : fields[3],
            "wind_speed_mps" : fields[5],
            "wind_speed_kph" : fields[7]
        }

        

class YXXDR(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class GPZDA(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

def get_sentence_interface(sentence_id):
    """ Returns the class interface for sentence id"""
    return getattr(sys.modules[__name__], sentence_id)