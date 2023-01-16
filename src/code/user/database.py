from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///enferno/enferno.db', \
                    convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from sqlalchemy.orm import declarative_base

Base = declarative_base()  

