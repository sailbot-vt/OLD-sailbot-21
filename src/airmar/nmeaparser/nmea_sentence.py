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
        nmea_map["<sentence-id>_<data-description>"] = str(data)

        Side-effects:
        nmea_map will be updated with sentence key value pairs
        """
        pass

class GPDTM(NmeaSentence):
    def update_data(nmea_map, fields):
        # GPDTM
        sid = fields[0]
        # 3 letter alphabetical code for local datum
        nmea_map["dtm_local_datum_code"] = fields[1]
        # 1 letter subdivision datum code (when available)
        nmea_map["dtm_subdivision_datum_code"] = fields[2]
        # Latitude offset to the nearest .0001 minute
        nmea_map["dtm_latitude_offset"] = fields[3]
        # N/S if dtm_latitude_offset is North/South latitude
        nmea_map["dtm_latitiude_cardinality"] = fields[4]
        # Longitude offset to the nearest .0001 minute
        nmea_map["dtm_longitude_offset"] = fields[5]
        # E/W if dtm_longitude_offset is East/West longitude
        nmea_map["dtm_longitude_cardinality"] = fields[6]
        # Signed (+/-) altitude offset, to the nearest meter
        nmea_map["dtm_altitude_offset"] = fields[7]
        # 3 character reference datum code
        nmea_map["dtm_reference_datum_code"] = fields[8]

class GPGGA(NmeaSentence):
    def update_data(nmea_map, fields):
        # GPGGA
        sid = fields[0]
        # UTC of position, in the form hhmmss
        nmea_map["gga_utc_position"] = fields[1]
        # Latitude to the nearest .0001 minute
        nmea_map["gga_latitude"] = fields[2]
        # N/S if gga_latitude is North/South latitude
        nmea_map["gga_latitude_cardinality"] = fields[3]
        # Longitude to the nearest .0001 minute
        nmea_map["gga_longitude"] = fields[4]
        # E/W if gga_longitude is East/West longitude
        nmea_map["gga_longitude_cardinality"] = fields[5]
        # GPS quality indicator - refer to manual
        nmea_map["gga_gps_quality_indicator"] = fields[6]
        # Number of satelites in use, 0-12
        nmea_map["gga_number_satelites"] = fields[7]
        # Horizontal dilution of precision (hdop)
        nmea_map["gga_hdop"] = fields[8]
        # Altitude relatie to mean-sea-level (geoid), to the nearest meter
        nmea_map["gga_geoid"] = fields[9]

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
        # Wind direction True 0-359.9 degrees
        nmea_map["mwd_wind_direction_true"] = fields[1]
        # Wind direction Magnetic, 0-359.9 degrees
        nmea_map["mwd_wind_direction_magnetic"] = fields[3]
        # Wind speed knots
        nmea_map["mwd_wind_speed_knots"] = fields[5]
        # Wind speed meters per seconds
        nmea_map["mwd_wind_speed_mps"] = fields[7]

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
        sid = fields[0]
        # Course over ground, degrees True, to the nearest 0.1 degree
        nmea_map["vtg_course_over_ground_true"] = fields[1]
        # Course over ground, degrees Magnetic, to the nearest 0.1 degree
        nmea_map["vtg_course_over_ground_magnetic"] = fields[3]
        # Speed over ground, knots, to the nearest 0.1 knot
        nmea_map["vtg_speed_over_ground_knots"] = fields[5]
        # Speed over ground km/hr to the nearest 0.1 km/hr
        nmea_map["vtg_speed_over_ground_kph"] = fields[7]
        # Mode indicator - refer to manual
        nmea_map["vtg_mode_indicator"] = fields[9]

class WIVWR(NmeaSentence):
    def update_data(nmea_map, fields):
        sid = fields[0]
        # Wind angle relative to the vessel, 0-180, to the nearest degree
        nmea_map["vwr_wind_angle_degree"] = fields[1]
        # L/R (left/right) of vessel heading
        nmea_map["vwr_wind_angle_direction"] = fields[2]
        # Wind speed in knots, to the nearest 0.1 knot
        nmea_map["vwr_wind_speed_knots"] = fields[3]
        # Wind speed, meters per second
        nmea_map["vwr_wind_speed_mps"] = fields[5]
        # Wind speed, km/hr
        nmea_map["vwr_wind_speed_kph"] = fields[7]

        
class WIVWT(NmeaSentence):
    def update_data(nmea_map, fields):
        sid = fields[0]
        # True wind angle, 0-180, to the nearest degree
        nmea_map["vwt_wind_angle_degree"] = fields[1]
        # L/R (left/right) of vessel heading
        nmea_map["vwt_wind_angle_direction"] = fields[2]
        # Wind speed, knots
        nmea_map["vwt_wind_speed_knots"] = fields[3]
        nmea_map["vwt_wind_speed_mps"] = fields[5]
        nmea_map["vwt_wind_speed_kph"] = fields[7]
        

class YXXDR(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

class GPZDA(NmeaSentence):
    def update_data(nmea_map, fields):
        pass

