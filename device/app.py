# -*- coding: utf-8 -*-
from device.settings import ProdConfig, DevConfig
from device.logger import StratuxLogger
from device.db import Db
import logging as lg, sys
import argparse


class MyDevice(object):
    def __init__(self):
        self.config = {};
        lg.basicConfig( stream=sys.stderr )
        lg.getLogger("App").setLevel(lg.INFO)
        self.log = lg.getLogger("App")
        
        

    ## This is taken from Flask
    def config_from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self.config[key] = getattr(obj, key)
                self.log.info("{0}: {1}".format(key, 
                    self.config[key]))

    def loop(self, frequency=1):

        self.log.info("Loop frequency: {0}".format(frequency))

        stl = StratuxLogger(self)
        flight_id = stl.logFlight()
        self.log.info("Flight ID: {0}".format(flight_id))

        # XXX Add a loop here
        stl.saveSnapshotToDb(flight_id)

        
        

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    """
    app = MyDevice()
    app.config_from_object(config_object)
    app.db = Db(app)
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", help="Development mode",
            action="store_true")
    #parser.add_argument("-r", "--run", 
    #        help="Instead of looping, just run once", 
    #        action="store_true")
    parser.add_argument("-f", "--frequency", 
            help="set the logging frequency (default = 1s)",
                    type=float, default=1)
    parser.add_argument("--create_db", 
            help="Create the database and exit", 
            action="store_true")
    parser.add_argument("-s", "--stratux-hostname", 
            help="set the hostname")
    parser.add_argument("-p", "--stratux-port", 
            help="set the port")
    
    args = parser.parse_args()


    if args.dev:
        config = DevConfig
    else:
        config = ProdConfig

    app = create_app(config)

    if args.stratux_hostname:
        app.config['STRATUX_HOSTNAME'] = args.stratux_hostname

    if args.stratux_port:
        app.config['STRATUX_PORT'] = args.stratux_port


    if args.create_db:
        app.db.create_tables()
    else:
        app.loop(frequency=args.frequency)
