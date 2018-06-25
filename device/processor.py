from device.models import Situation, Flight
from bs4 import BeautifulSoup

class ProcessFlight(): 
    def __init__(self, app, flight_id):
        self.app = app
        self.flight_id = flight_id
        self.flight = self.app.db.session.query(Flight).filter_by(id = 
                self.flight_id).first()
        self.max_g = None
        self.min_g = None
        import os
        # XXX Todo make this configurable
        kml_header = app.config['KML_HEADER']
        current_dirname = os.path.dirname(__file__)
        self.header_filename = os.path.join(current_dirname, 'static_data', kml_header)
        
        

    def set_max_min_g(self, AHRSGLoad): 
        if self.max_g is None or self.max_g < AHRSGLoad:
            self.max_g = AHRSGLoad
        if self.min_g is None or self.min_g > AHRSGLoad:
            self.min_g = AHRSGLoad

    def get_max_min_g(self):
        for situation in self.flight.situations:
            self.set_max_min_g(situation.AHRSGLoad)
        return self.max_g, self.min_g



    def write_kml_file(self):
        def append_value(section, tag='gx:value', value=''):
            new_tag = kml_header.new_tag(tag)
            new_tag.string = str(value)
            section.append(new_tag)

        with open(self.header_filename, 'r') as data:
            kml_header = BeautifulSoup(data, 'lxml-xml')

        start_placemark = kml_header.Document.Placemark.find_next("Placemark").Point
        first_situation = self.flight.situations[0]
        initial_coords = "{0} {1}".format(first_situation.GPSLongitude, 
                first_situation.GPSLatitude)
        append_value(start_placemark, 'coordinates', initial_coords)
        
        for situation in self.flight.situations:
            self.set_max_min_g(situation.AHRSGLoad)

            track_log = kml_header.Document.Placemark.find("gx:Track")

            ts = situation.StratuxTimeStamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            coordinate = "{0} {1} {2}".format(situation.GPSLongitude, 
                    situation.GPSLatitude, situation.GPSAltitudeMSL / 3.28084)

            append_value(track_log, 'when', value=ts)
            append_value(track_log, 'gx:coord', value=coordinate)
            
            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "acc_horiz"}), value=situation.GPSHorizontalAccuracy)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "acc_vert"}), value=situation.GPSVerticalAccuracy)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "speed_kts"}), value=situation.GPSGroundSpeed)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "altitude"}), value=situation.GPSAltitudeMSL)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "bank"}), value=situation.AHRSRoll)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "pitch"}), value=situation.AHRSPitch)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "g_load"}), value=situation.AHRSGLoad)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "baro_altitude"}), value=situation.BaroPressureAltitude)

            append_value(kml_header.Document.find('gx:SimpleArrayData', 
                attrs={"name": "mag_heading"}), value=situation.AHRSMagHeading)

        return kml_header
            
            
