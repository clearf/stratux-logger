import urllib, json
from device.models import AhrsSnapshot

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

    def getSituation(self): 
        parameters = {}
        url = self.base_url + "getSituation"
        print(url)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        self.current_snapshot = data;
        return data

    def saveSnapshotToDb(self): 
        if not self.current_snapshot:
            self.getSituation()

        ahrs_snapshot = AhrsSnapshot()
        ahrs_snapshot.GPSVerticalSpeed = \
            self.current_snapshot['GPSVerticalSpeed']
        self.db.session.add(ahrs_snapshot)

    
