from sqlalchemy import Column, Integer, String, Float, Enum, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    name = Column(String, nullable=False, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    size = Column(ARRAY(String), nullable=False)
    unit_price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)
    color = Column(ARRAY(String), nullable=False)
