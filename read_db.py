from db import Session
from models import Group

def read_groups():
    session = Session()
    groups = session.query(Group).all()

    for g in groups:
        print(f"ID: {g.id} | URL: {g.url} | Join at: {g.members_count}")

    session.close()

if __name__ == "__main__":
    read_groups()