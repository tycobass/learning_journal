from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    Unicode,
    desc,
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


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(Unicode)
    created = Column(DateTime, default = datetime.utcnow)
    modified = Column(DateTime, default = datetime.utcnow,\
         onupdate = datetime.utcnow)

    @classmethod
    def all(cls, insight=None, session=None):
        #return the all entries sorted (desc) by id
        if session == None:  # Assure session will work in pshell
            session = DBSession
        q1 = session.query(cls)   # alias "session.query"
        all_entries = q1.order_by(desc(cls.id)) #create select all query
        if insight is not None:  # print results of query
            cls.insight(all_entries)
        return all_entries


    @classmethod
    def by_id(cls, id_num, insight=None, session=None):
        #return the entry by the given id
        if session == None:  # Assure session will work in pshell
            session = DBSession
        q1 = DBSession.query(cls)  # alias "session.query"
        id_entry = q1.get(id_num)  #create select by id query
        if insight is not None:  # print results of query
            cls.insight(id_entry)
        return id_entry

    @classmethod
    def insight(cls, query_result, session=None):
        #Debug - print the query results for review by developer
        if session == None:  # Assure session will work in pshell
            session = DBSession
        [print('\n', n.id, ' | ', n.title, ' | ', n.body, ' | ',\
         n.created, ' | ', n.modified, '\n') for n in query_result]
        return

Index('my_index', Entry.title, unique=True, mysql_length=255)
