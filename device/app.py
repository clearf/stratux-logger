# -*- coding: utf-8 -*-
from device.settings import ProdConfig, DevConfig
from device.logger import StratuxLogger
from device.db import Db
import logging as lg, sys
import argparse
from twisted.internet import task
from twisted.internet import reactor



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

    def loop(self, delay=1, runs = 0 ):

        self.log.info("Loop delay: {0}".format(delay))

        stl = StratuxLogger(self)
        flight_id = stl.logFlight()
        self.log.info("Flight ID: {0}".format(flight_id))

        def do_loop(): 
            ### XXX Saving the snapshot to the DB doesn't work in an ansynchronous environment
            LoopingCallWithCounter(runs, self, stl.saveSnapshotToDb, flight_id).lc.start(delay)

        class LoopingCallWithCounter:
            def __init__(self, runs, device, f, *a, **kw):
                self.i = 0
                def wrapper():
                    device.log.info("Wrap {0}".format(self.i))
                    if self.i >= runs - 1  and runs > 0:
                        self.lc.stop()
                        reactor.callFromThread(reactor.stop)
                    else:
                        device.log.info("Flight ID {0}".format(a))
                        f(*a, **kw)
                        self.i += 1
                self.lc = task.LoopingCall(wrapper)

        do_loop()
        self.reactor = reactor.run()
        
        
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
    parser.add_argument("-f", "--delay", 
            help="set the logging delay (default = 1s)",
                    type=float, default=1)
    parser.add_argument("-r", "--runs", 
            help="Set a certian amount of runs (default = 0, i.e., unconstrained)",
                    type=float, default=0)
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
        app.loop(delay=args.delay, runs=args.runs)
