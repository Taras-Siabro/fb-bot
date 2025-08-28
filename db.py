from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///groups.db", echo=True)  # echo=True чтобы видеть SQL
Session = sessionmaker(bind=engine)