from sqlalchemy import Column, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.mysql import LONGTEXT

from database.orm import Session
from database.orm_base import Base

table_prefix = 'module_wiki_'
db = Session
session = db.session
engine = db.engine


class WikiTargetSetInfo(Base):
    __tablename__ = table_prefix + 'TargetSetInfo'
    targetId = Column(String(512), primary_key=True)
    link = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    iws = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    headers = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    prefix = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)


class WikiInfo(Base):
    __tablename__ = table_prefix + 'WikiInfo'
    apiLink = Column(String(512), primary_key=True)
    siteInfo = Column(LONGTEXT if session.bind.dialect.name == 'mysql' else Text)
    timestamp = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))


class WikiAllowList(Base):
    __tablename__ = table_prefix + 'WikiAllowList'
    apiLink = Column(String(512), primary_key=True)
    operator = Column(String(512))


class WikiBlockList(Base):
    __tablename__ = table_prefix + 'WikiBlockList'
    apiLink = Column(String(512), primary_key=True)
    operator = Column(String(512))


Session.create()
