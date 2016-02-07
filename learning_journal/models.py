from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    Unicode,
    desc
    )
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


#title - unicode char to 255, unique, must be present
#body - unicode any length including zero
#create field - time of generation, default value is now
#edited field - time of last edit, default value is now
#class method of "all" that returns all the entries in the database, ordered so that the most recent entry is first
#class method of "by_id" that returns a single entry, given an id
#modified = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
#     created = Column(DateTime(timezone=True), default = datetime.utcnow())  calll each time


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(Unicode)
    created = Column(DateTime(timezone=True), default = datetime.utcnow)
    modified = Column(DateTime(timezone=True),onupdate = datetime.utcnow)

    @classmethod
    def alls(cls, session=None):
        print('class', cls)
        if session == None:
            session = DBSession
        q1 = session.query(cls)
        all_entries = q1.order_by(desc(cls.id))
        [print(n.title) for n in all_entries] 
        print('\n\nall entries value - \n', all_entries, '\n')
        return all_entries

    @classmethod
    def by_id(cls):
        q1 = DBSession.query(cls, session = None)
        if session == None:
            session = DBSession
        id_entry = q1.query(cls).order_by(desc(cls.id))
        return id_entry


Index('my_index', Entry.title, unique=True, mysql_length=255)
