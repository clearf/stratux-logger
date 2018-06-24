import os, json, sys
import logging as lg, unittest
from bs4 import BeautifulSoup
from device.logger import StratuxLogger
from device.processor import ProcessFlight
from device.models import Flight, Situation
from device.db import Db
from datetime import datetime
from sqlalchemy import inspect


class TestLogStratux(unittest.TestCase):
    def setUp(self):
        self.db = Db()
        self.db.create_tables()
        self.stratux_port = 5000 
        lg.basicConfig( stream=sys.stderr )
        lg.getLogger("TestLogStratux").setLevel(lg.INFO)
        self.log = lg.getLogger("TestLogStratux")

        # Static AHRS file
        ahrs_file = os.path.join(os.path.dirname(__file__), "emulator", 
            "emulator", "static", "situation.json")

        with open(ahrs_file, 'r') as f:
          self.static_ahrs_data=json.load(f)
          f.close()
        
    def test_we_can_get_a_snapshot_from_webserver(self):
        stl = StratuxLogger(db=self.db, stratux_port=self.stratux_port)
        ahrs_data = stl.getSituationFromStratux(); 

        
        # Test the whole snapshot is equal
        self.assertEqual(self.static_ahrs_data,ahrs_data)

    def test_we_can_save_a_flight_to_the_database(self):
        stl = StratuxLogger(db=self.db, stratux_port=self.stratux_port)
        flight_id = stl.logFlight()
        flight = self.db.session.query(Flight).first()
        self.assertTrue(flight)
        self.assertTrue(flight_id)

    def test_we_can_save_a_snapshot_to_the_database(self):
        stl = StratuxLogger(db=self.db, stratux_port=self.stratux_port)
        flight_id = stl.logFlight()
        self.log.debug("Flight ID: {0}".format(flight_id))
        stl.saveSnapshotToDb(flight_id)

        db_snapshot = self.db.session.query(Situation).first()

        flights = self.db.session.query(Flight).all()

        self.log.debug("Flights: {0}".format(flights))

        # Test that something has been inserted
        self.assertTrue(db_snapshot)
        model_to_dict = lambda obj: {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}        
        db_snapshot_dict = model_to_dict(db_snapshot)


        # Do a two-way comparison
        for key, val in self.static_ahrs_data.items(): 
            self.assertEqual(self.static_ahrs_data[key], db_snapshot_dict[key])

        for key, val in db_snapshot_dict.items(): 
            if key != "id" and key != "flight_id" and key != "StratuxTimeStamp":
                self.assertEqual(self.static_ahrs_data[key], db_snapshot_dict[key])

class TestProcessFlight(unittest.TestCase):
    def setUp(self):
        self.db = Db()
        self.db.create_tables()
        self.stratux_port = 5000 

        lg.basicConfig( stream=sys.stderr )
        lg.getLogger("TestProcessFlight").setLevel(lg.INFO)
        self.log = lg.getLogger("TestProcessFlight")

        # Populate test data
        stl = StratuxLogger(db=self.db, stratux_port=self.stratux_port)
        flight_id = stl.logFlight()
        self.log.debug("Flight ID: {0}".format(flight_id))
        stl.saveSnapshotToDb(flight_id)

        # Setup our processor
        self.process_flight = ProcessFlight(db=self.db, flight_id = flight_id)

        current_dirname = os.path.dirname(__file__)
        self.reference_dir = os.path.join(current_dirname, 'reference_data')
        self.output_dir = os.path.join(current_dirname, 'output')
        

    def test_we_can_get_g_forces(self):
        (max_g, min_g) = self.process_flight.get_max_min_g()
        self.assertEqual(max_g,0.99847599584255)
        self.assertEqual(min_g,0.99847599584255)

        
    def test_we_can_write_kml_file(self):
        kml = self.process_flight.write_kml_file()
        now = datetime.now().strftime('%Y-%m-%dT%H_%M_%SZ')
        with open(os.path.join(self.reference_dir, "situationTracklog.kml"), 'r') as data:
            kml_reference  = BeautifulSoup(data, 'lxml-xml')
        self.assertTrue(kml, kml_reference)

