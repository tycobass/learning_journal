from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    Unicode,
    desc,
    funcfilter   #### for filter method
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
    modified = Column(DateTime(timezone=True),\
        default = datetime.utcnow, onupdate = datetime.utcnow)

    @classmethod
    def all(cls, insight=None, session=None):
        #return the all entries sorted (desc) by id
        if session == None:
            session = DBSession
        q1 = session.query(cls)
        all_entries = q1.order_by(desc(cls.id))
        [print('\n', n.id, ' | ', n.title, ' | ', n.body, ' | ',\
         n.created, ' | ', n.modified, '\n') for n in all_entries]
        return all_entries


    @classmethod
    def by_id(cls, id_num, session=None):
        #return the entry by the given id
        if session == None:
            session = DBSession
        q1 = DBSession.query(cls)
        ### session.query(MyModel).filter(MyModel.value < 20)]
        print('\nid_num value - ', id_num, '\n')
        id_entry = q1.filter(cls.id==id_num)
        [print('\n', n.id, ' | ', n.title, ' | ', n.body, ' | ',\
         n.created, ' | ', n.modified, '\n', 'now method\n') for n in id_entry]
        cls.insight(id_entry)
        return id_entry

    @classmethod
    def insight(cls, query_result, session=None):
        #return the all entries sorted (desc) by id
        if session == None:
            session = DBSession
        [print('\n', n.id, ' | ', n.title, ' | ', n.body, ' | ',\
         n.created, ' | ', n.modified, '\n') for n in query_result]
        return

Index('my_index', Entry.title, unique=True, mysql_length=255)
