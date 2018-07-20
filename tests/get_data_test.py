import os, json, sys
import logging as lg
import unittest
import time
from bs4 import BeautifulSoup
from device.logger import StratuxLogger
from device.processor import ProcessFlight
from device.models import Flight, Situation
from device.settings import TestConfig
from device.app import create_app
from datetime import datetime
from sqlalchemy import inspect


class TestLogStratux(unittest.TestCase):
    def setUp(self):
        
        self.app = create_app(config_object = TestConfig)
        self.app.db.create_tables()
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
        stl = StratuxLogger(self.app)
        ahrs_data = stl.getSituationFromStratux(); 

        
        # Test the whole snapshot is equal
        self.assertEqual(self.static_ahrs_data,ahrs_data)

    def test_we_can_save_a_flight_to_the_database(self):
        stl = StratuxLogger(self.app)
        flight_id = stl.logFlight()
        session = self.app.db.Session()
        flight = session.query(Flight).first()
        self.assertTrue(flight)
        self.assertTrue(flight_id)
        self.app.db.Session.remove()

    def test_we_can_save_a_snapshot_to_the_database(self):
        stl = StratuxLogger(self.app)
        flight_id = stl.logFlight()
        self.log.debug("Flight ID: {0}".format(flight_id))
        stl.saveSnapshotToDb(flight_id)

        session = self.app.db.Session()
        db_snapshot = session.query(Situation).first()

        session = self.app.db.Session()
        flights = session.query(Flight).all()

        self.log.debug("Flights: {0}".format(flights))

        self.app.db.Session.remove()

        # Test that something has been inserted
        self.assertTrue(db_snapshot)
        model_to_dict = lambda obj: {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}        
        db_snapshot_dict = model_to_dict(db_snapshot)
        self.app.db.Session.remove()


        # Do a two-way comparison
        for key, val in self.static_ahrs_data.items(): 
            self.assertEqual(self.static_ahrs_data[key], db_snapshot_dict[key])

        for key, val in db_snapshot_dict.items(): 
            if key != "id" and key != "flight_id" and key != "StratuxTimeStamp":
                self.assertEqual(self.static_ahrs_data[key], db_snapshot_dict[key])

class TestRunApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object = TestConfig)
        self.app.db.create_tables()
        lg.basicConfig( stream=sys.stderr )
        lg.getLogger("TestLogStratux").setLevel(lg.INFO)
        self.log = lg.getLogger("TestLogStratux")

    #def test_we_can_save_a_snapshot(self):
     #   runs = 3
     #   self.app.loop(runs=runs)
     #   time.sleep(5)
#
#        session = self.app.db.Session()
#        logged = count(session.query(Situation).all())
#        self.app.db.Session.remove()
#        self.assertEqual(logged, runs)
        
        


class TestProcessFlight(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object = TestConfig)
        self.app.db.create_tables()

        lg.basicConfig( stream=sys.stderr )
        lg.getLogger("TestProcessFlight").setLevel(lg.INFO)
        self.log = lg.getLogger("TestProcessFlight")

        # Populate test data
        stl = StratuxLogger(self.app)
        flight_id = stl.logFlight()
        self.log.debug("Flight ID: {0}".format(flight_id))
        stl.saveSnapshotToDb(flight_id)

        # Setup our processor
        self.process_flight = ProcessFlight(self.app, flight_id = flight_id)

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
        with open(os.path.join(self.reference_dir, "basic_tracklog.kml"), 'r') as data:
            kml_reference  = BeautifulSoup(data, 'lxml-xml')
        self.assertTrue(kml, kml_reference)

