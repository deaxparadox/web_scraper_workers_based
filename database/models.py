from sqlalchemy import (
    create_engine,
    Column, Integer, String, DateTime
)
from sqlalchemy.orm import (
    declarative_base, sessionmaker
)
from datetime import datetime


Base = declarative_base()



class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    @property
    def get_url(self):
        return self.url