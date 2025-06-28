from sqlalchemy import Column, String, Integer, Boolean
from database.main import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isComplete = Column(Boolean, default=False)