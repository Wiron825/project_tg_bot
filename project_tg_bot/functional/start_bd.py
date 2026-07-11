from sqlalchemy import (MetaData, Table, Column, Integer, String, Text, ForeignKey, create_engine,
                         insert, text, Float, DateTime)
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime


Base = declarative_base()

engine = create_engine(
    "sqlite:///project_tg_bot/bd/mybd.sqlite3",
    echo=True
)

metadata = MetaData()


class User(Base):
    __tablename__ = "users"
    tg_id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    count_ratings = Column(Integer)
    status = Column(String)
    ratings_today = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.now)



class Street(Base):
    __tablename__ = "streets"
    id = Column(Integer(), primary_key=True)
    name_street = Column(String, nullable=False)
    old_rating = Column(Float)
    new_rating = Column(Float)
    count_rating = Column(Integer)
    old_count_rating = Column(Integer)
    count_rating_today = Column(Integer, default=0)



class Change(Base):
    __tablename__ = "changes"
    id = Column(Integer(), primary_key=True)
    user_tg_id = Column(ForeignKey("users.tg_id"))
    street_id = Column(ForeignKey("streets.id"))
    value = Column(Integer)
    date = Column(DateTime, default=datetime.now)

class Coment(Base):
    __tablename__ = 'coments'
    id = Column(Integer(), primary_key=True)
    street_id = Column(ForeignKey("streets.id"))
    coment = Column(String)

Base.metadata.create_all(engine)



def delete_users():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM users"))

def delete_streets():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM streets"))

def delete_changes():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM changes"))

def delete_coment():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM coments"))



def new_user(id_user: int =0, name: str ='', count_ratings: int =0, status: str =''):
    with Session(engine) as session:
        new_user = User(tg_id=id_user, name=name, count_ratings=count_ratings, status=status)
        session.add(new_user)
        session.commit()

def new_street(name_street: str ='', old_rating: float =5, old_count_rating: int =3):
    with Session(engine) as session:
        new_street = Street(name_street=name_street, old_rating=old_rating,
                           new_rating=old_rating, count_rating=old_count_rating, old_count_rating=old_count_rating)
        session.add(new_street)
        session.commit()

def new_change(user_tg_id: int = 0, street_id: int = 1, value:int = 5):
    with Session(engine) as session:
        new_change = Change(user_tg_id=user_tg_id, street_id=street_id, value=value)
        session.add(new_change)
        session.commit()

def new_coment(street_id: int, coment: str):
    with Session(engine) as session:
        new_coment = Coment(street_id=street_id, coment=coment)
        session.add(new_coment)
        session.commit()


# delete_users()
# delete_streets()
# delete_changes()

# new_user()
# new_street()
# new_change()
