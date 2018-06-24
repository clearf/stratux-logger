from datetime import datetime
import urllib, json
from device.models import Flight, Situation

class StratuxLogger(): 
    def __init__(self, db, stratux_hostname="localhost", 
            stratux_port="80"): 
        self.stratux_hostname=stratux_hostname
        self.stratux_port = stratux_port
        self.db = db
        self.base_url = "http://%s:%s/" % (self.stratux_hostname, 
                self.stratux_port)
        self.current_snapshot = {}
        return

    def getSituationFromStratux(self): 
        parameters = {}
        url = self.base_url + "getSituation"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        self.current_snapshot = data;
        return data

    def saveSnapshotToDb(self, flight_id): 
        if not self.current_snapshot:
            self.getSituationFromStratux()


        situation = Situation(**self.current_snapshot)
        situation.StratuxTimeStamp = datetime.now()
        situation.flight_id = flight_id
        self.db.session.add(situation)

    def logFlight(self): 
        # Setup flight
        # So we're going to just store everything in a 
        # TZ ignorant object now; we can convert later to
        # a TZ Aware object with pytz if we need to
        flight_start = datetime.now()

        flight = Flight()
        flight.flight_start = flight_start
        flight.n_number = "N12345" # XXX Make a config option
        self.db.session.add(flight)
        self.db.session.flush()
        
        return flight.id
        

        #self.getSituationFromStratux()
        #self.saveSnapshotToDb()


    
