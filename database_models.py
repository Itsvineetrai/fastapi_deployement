from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

# how tables will be connected to the database
# Creating a base class for our models
Base=declarative_base()

# Defining the Product model which maps to the 'product' table in the database
class Product(Base):

    __tablename__='product'
 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)