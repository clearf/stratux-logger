import unittest, os, json
from device.logger import StratuxLogger
from device.models import AhrsSnapshot
from device.db import Db


class TestLogStratux(unittest.TestCase):

    def setUp(self):
        self.db = Db()
        self.db.create_tables()
        self.stl = StratuxLogger(db=self.db, stratux_port=5000)
        self.ahrs_data = self.stl.getSituation(); 
        
    def test_we_can_get_a_snapshot_from_webserver(self):
        ahrs_file = os.path.join(os.path.dirname(__file__), "emulator", 
            "emulator", "static", "situation.json")
        # Test one thing
        self.assertEqual(self.ahrs_data['GPSVerticalSpeed'], -0.6135171)

        with open(ahrs_file, 'r') as f:
          static_ahrs_data=json.load(f)
          f.close()
        
        # Test the whole snapshot is equal
        self.assertEqual(static_ahrs_data,self.ahrs_data)


    def test_we_can_save_a_snapshot_to_the_database(self):
        self.stl.saveSnapshotToDb()
        # Test the whole snapshot is equal
        self.assertTrue(self.db.session.query(AhrsSnapshot).first())
