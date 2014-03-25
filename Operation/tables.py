import config

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

import config

engine = create_engine(config.DB_URL, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class FC(Base):
    __tablename__ = "fc" 
    id = Column(Integer, primary_key=True)
    feature = Column(Integer, nullable=False)
    category = Column(String(64), nullable=False)
    count = Column(Integer, nullable=False)
    
class CC(Base):
    __tablename__ = "cc"
    id = Column(Integer, primary_key=True)
    category = Column(String(64), nullable=False)
    count = Column(Integer, nullable=False)

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()