from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class AhrsSnapshot(Base):
    __tablename__ = 'ahrs_snapshot'
    id = Column(Integer, autoincrement=True, primary_key=True)
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
    GPSLastFixLocalTime             = Column(DateTime)
    GPSTrueCourse                   = Column(Float)
    GPSTurnRate                     = Column(Float)
    GPSGroundSpeed                  = Column(Float)
    GPSLastGroundTrackTime          = Column(DateTime)
    GPSTime                         = Column(DateTime)
    GPSLastGPSTimeStratuxTime       = Column(DateTime)
    GPSLastValidNMEAMessageTime     = Column(DateTime)
    GPSLastValidNMEAMessage         = ColumN(String)
    GPSPositionSampleRate           = Column(Float)
    BaroTemperature                 = Column(Float)
    BaroPressureAltitude            = Column(Float)
    BaroVerticalSpeed               = Column(Float)
    BaroLastMeasurementTime         = Column(DateTime)
    AHRSPitch                       = Column(Float)
    AHRSRoll                        = Column(Float)
    AHRSGyroHeading                 = Column(Float)
    AHRSMagHeading                  = Column(Float)
    AHRSSlipSkid                    = Column(Float)
    AHRSTurnRate                    = Column(Float)
    AHRSGLoad                       = Column(Float)
    AHRSGLoadMin                    = Column(Float)
    AHRSGLoadMax                    = Column(Float)
    AHRSLastAttitudeTime            = Column(DateTime)
    AHRSStatus                      = Column(Integer)

    def __repr__(self):
        return '<AhrsSnapshot {0}: {1}>'.format(self.id, self.GPSVerticalSpeed)


