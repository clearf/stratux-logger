from datetime import datetime
import urllib.request
import json
from device.models import Flight, Situation

class StratuxLogger(): 
    def __init__(self, app): 
        self.app = app
        self.base_url = "http://%s:%s/" % (app.config['STRATUX_HOSTNAME'],
                app.config['STRATUX_PORT'])
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
        # XXX add exception handling
        self.getSituationFromStratux()
        situation = Situation(**self.current_snapshot)
        situation.StratuxTimeStamp = datetime.now()
        situation.flight_id = flight_id
        self.app.db.session.add(situation)

    def logFlight(self): 
        # Setup flight
        # So we're going to just store everything in a 
        # TZ ignorant object now; we can convert later to
        # a TZ Aware object with pytz if we need to
        flight_start = datetime.now()

        flight = Flight()
        flight.flight_start = flight_start
        flight.n_number = self.app.config.get('N_NUMBER')
        self.app.db.session.add(flight)
        self.app.db.session.flush()
        
        return flight.id
        

        #self.getSituationFromStratux()
        #self.saveSnapshotToDb()


    
