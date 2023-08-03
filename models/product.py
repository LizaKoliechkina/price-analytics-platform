from sqlalchemy import Column, String, Float, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from database import Base, generate_uuid


class Product(Base):
    __tablename__ = 'product'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=generate_uuid)
    name = Column(String(length=100), nullable=False)
    description = Column(String(length=300), nullable=True)
    global_price = Column(Float, nullable=False)
    local_price = Column(Float, nullable=False)
    sold_quantity = Column(Integer, nullable=False)
    cluster = Column(String(length=50), nullable=False)
    division = Column(String(length=50), nullable=False)
    country = Column(String(length=50), nullable=False)

    UniqueConstraint('name', 'cluster', 'division', 'country')
