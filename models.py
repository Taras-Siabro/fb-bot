# models.py
from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    members_count = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)
