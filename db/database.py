from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Создаем базу SQLite
engine = create_engine("sqlite:///groups.db", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Group(name={self.name}, url={self.url})>"


def init_db():
    Base.metadata.create_all(engine)


def add_group(name, url):
    session = Session()
    group = Group(name=name, url=url)
    try:
        session.add(group)
        session.commit()
    except Exception:
        session.rollback()  # если вдруг дубликат
    finally:
        session.close()


def get_all_groups():
    session = Session()
    groups = session.query(Group).all()
    session.close()
    return groups