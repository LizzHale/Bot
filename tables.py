from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, scoped_session

import config

engine = create_engine(config.DB_URL, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class featurecount(Base):
    """ Tracks the feature and category combinations """

    __tablename__ = "featurecount" 


    id = Column(Integer, primary_key=True)
    feature = Column(String, nullable=False)
    category = Column(String(64), nullable=False)
    count = Column(Float, nullable=False)
    
class categorycount(Base):
    """ Tracks the features in each category """

    __tablename__ = "categorycount"
    
    id= Column(Integer, primary_key=True)
    category = Column(String(64), nullable=False)
    count = Column(Float, nullable=False)

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()