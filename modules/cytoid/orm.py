from sqlalchemy import Column, String

from database.orm import Session
from database.orm_base import Base

table_prefix = 'module_cytoid_'
db = Session
session = db.session
engine = db.engine


class CytoidBindInfo(Base):
    __tablename__ = table_prefix + 'CytoidBindInfo'
    targetId = Column(String(512), primary_key=True)
    username = Column(String(512))


Session.create()
