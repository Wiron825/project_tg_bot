from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine(
    "sqlite:///project_tg_bot/mybd.sqlite3",
    echo=True
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

Base.metadata.create_all(engine)


def delete():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM user"))

def new_person(id_user=0, name_user='', password_user=''):
    with Session(engine) as session:
        new_user = User(id=id_user, name=name_user, password=password_user)
        session.add(new_user)
        session.commit()

def look_id():
    with engine.begin()as conn:
        data = conn.execute(text("SELECT id FROM user"))
        data = [i for row in data for i in row]
        print(data)
    return data
