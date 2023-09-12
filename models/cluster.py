from sqlalchemy import Column, String, Integer

from database.connect import Base


class Cluster(Base):
    __tablename__ = 'cluster'

    name = Column(String(length=50), primary_key=True, nullable=False)
    description = Column(String(length=300), nullable=True)
    division = Column(String(length=50), nullable=False)
    previous_sold_quantity = Column(Integer, nullable=False, default=0)
