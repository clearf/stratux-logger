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
        try:
            parameters = {}
            url = self.base_url + "getSituation"
            self.app.log.debug("URL " + url)
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            self.current_snapshot = data;
            return data
        except Exception as e: 
            print("Cannot getSituation: {0}".format(e))
            return None

    def saveSnapshotToDb(self, flight_id, *args, **kwargs): 
        if self.getSituationFromStratux(): 
            situation = Situation(**self.current_snapshot)
            situation.StratuxTimeStamp = datetime.now()
            situation.flight_id = flight_id
            try:
                session = self.app.db.Session()
                session.add(situation)
                session.commit()
                self.app.db.Session.remove()
            except Exception as e: 
                print(e)

    def logFlight(self): 
        # Setup flight
        # So we're going to just store everything in a 
        # TZ ignorant object now; we can convert later to
        # a TZ Aware object with pytz if we need to
        flight_start = datetime.now()

        flight = Flight()
        flight.flight_start = flight_start
        flight.n_number = self.app.config.get('N_NUMBER')
        session = self.app.db.Session()
        session.add(flight)
        session.flush()
        session.commit()
        flight_id = flight.id
        self.app.db.Session.remove()
        
        return flight_id
