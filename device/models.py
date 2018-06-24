from sqlalchemy import Column, Integer, BigInteger, \
    Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flight'
    id = Column(Integer, autoincrement=True, primary_key=True)
    situations = relationship("Situation", 
            back_populates="flight")
    
    flight_start = Column(DateTime)
    n_number = Column(String)

    def __repr__(self):
        return '<Flight {0}: {1}, {2}>'.format(self.id, 
                self.flight_start, self.n_number)

class Situation(Base):
    __tablename__ = 'situation'
    id = Column(Integer, autoincrement=True, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    flight = relationship("Flight", back_populates="situations")
    GPSLastFixSinceMidnightUTC      = Column(Float)
    GPSLatitude                     = Column(Float)
    GPSLongitude                    = Column(Float)
    GPSFixQuality                   = Column(Integer)
    GPSHeightAboveEllipsoid         = Column(Float)
    GPSGeoidSep                     = Column(Float)
    GPSSatellites                   = Column(Integer)
    GPSSatellitesTracked            = Column(Integer)
    GPSSatellitesSeen               = Column(Integer)
    GPSHorizontalAccuracy           = Column(Integer)
    GPSNACp                         = Column(Integer)
    GPSAltitudeMSL                  = Column(Float)
    GPSVerticalAccuracy             = Column(Integer)
    GPSVerticalSpeed                = Column(Float)
    GPSLastFixLocalTime             = Column(String)
    GPSTrueCourse                   = Column(Float)
    GPSTurnRate                     = Column(Float)
    GPSGroundSpeed                  = Column(Float)
    GPSLastGroundTrackTime          = Column(String)
    GPSTime                         = Column(String)
    GPSLastGPSTimeStratuxTime       = Column(String)
    GPSLastValidNMEAMessageTime     = Column(String)
    GPSLastValidNMEAMessage         = Column(String)
    GPSPositionSampleRate           = Column(Float)
    BaroTemperature                 = Column(Float)
    BaroPressureAltitude            = Column(Float)
    BaroVerticalSpeed               = Column(Float)
    BaroLastMeasurementTime         = Column(String)
    AHRSPitch                       = Column(Float)
    AHRSRoll                        = Column(Float)
    AHRSGyroHeading                 = Column(Float)
    AHRSMagHeading                  = Column(Float)
    AHRSSlipSkid                    = Column(Float)
    AHRSTurnRate                    = Column(Float)
    AHRSGLoad                       = Column(Float)
    AHRSGLoadMin                    = Column(Float)
    AHRSGLoadMax                    = Column(Float)
    AHRSLastAttitudeTime            = Column(String)
    AHRSStatus                      = Column(Integer)
    StratuxTimeStamp                = Column(DateTime)

    def __repr__(self):
        return '<Situation {0}: ({1}, {2})>'.format(self.id, 
                self.GPSLatitude, self.GPSLongitude)


