from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.engine.url import URL

from .models import Base

class Db():
    def __init__(self, app):
        """
        Performs database connection using database settings 
        from settings.py.
        Returns sqlalchemy engine instance
        Could do this too: 
            return create_engine(URL(**settings.DATABASE))
        """
        self.engine = create_engine(
           app.config['SQLALCHEMY_DATABASE_URI'],
                echo=app.config['DEBUG'],)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def create_tables(self):
        """"""
        Base.metadata.create_all(self.engine)
