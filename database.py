from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Engine helps in connecting to the database
# create_engine function requires the database URL


db_url="postgresql://postgres:Vineet08@localhost:5432/mydatabase1"
engine=create_engine(db_url)

# sessionmaker helps in creating a session to interact with the database
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)