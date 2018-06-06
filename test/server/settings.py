import os 

class Config(object):
    """Base configuration."""
    #SECRET_KEY = os.environ.get('MELTDOWNAPP_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Development configuration."""

    try: 
        from dotenv import load_dotenv
        dotenv_path = os.path.join(Config.PROJECT_ROOT, '.env')
        load_dotenv(dotenv_path)
    except ImportError as e:
        print "We don't actually need this in production", e
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
