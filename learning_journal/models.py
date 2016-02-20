from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    Unicode,
    UnicodeText,
    desc,
    )
from datetime import datetime

from passlib.context import CryptContext

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# then lower down, make a context at module scope:
password_context = CryptContext(schemes=['pbkdf2_sha512'])


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText,default=u'')
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
    def by_id(cls, id, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).get(id)

    @classmethod
    def insight(cls, query_result, session=None):
        #Debug - print the query results for review by developer
        if session == None:  # Assure session will work in pshell
            session = DBSession
        [print('\n', n.id, ' | ', n.title, ' | ', n.body, ' | ',\
         n.created, ' | ', n.modified, '\n') for n in query_result]
        return


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)

    @classmethod
    def by_name(cls, name, session=None):
        if session is None:
            session = DBSession
        return DBSession.query(cls).filter(cls.name == name).first()

    @classmethod
    def verify_password(self, password):
        return password_context.verify(password, self.password)