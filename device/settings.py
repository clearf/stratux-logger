# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DB_PATH = os.path.join(APP_DIR, "data")
    N_NUMBER =  os.environ.get('N_NUMBER')
    KML_HEADER = 'kml_header.kml'

class ProdConfig(Config):
    """Production configuration, i.e., we're running
    on a stratux itself."""
    ENV = 'prod'
    DEBUG = False
    STRATUX_PORT = 80
    STRATUX_HOSTNAME = "localhost" 
    db_name = 'prod.sqlite3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(Config.DB_PATH, 
        db_name))

class DevConfig(Config):
    """Development configuration, i.e., we're running on a laptop
    but connecting to a live stratux
    """
    ENV = 'dev'
    STRATUX_PORT = 80
    STRATUX_HOSTNAME = "192.168.10.1" 
    DEBUG = True
    db_name = 'dev.sqlite3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(Config.DB_PATH, 
        db_name))
    print(SQLALCHEMY_DATABASE_URI)


class TestConfig(Config):
    """Test configuration."""
    STRATUX_PORT = 5000
    STRATUX_HOSTNAME = "localhost" 
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    N_NUMBER =  'N12345'
