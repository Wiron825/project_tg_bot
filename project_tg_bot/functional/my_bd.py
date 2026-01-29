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
    count_Ratings = Column(Integer)
    statys = Column(String)

Base.metadata.create_all(engine)


def delete():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM user"))

def new_person(id_user=0, name_user='', count_Ratings_user=0, statys_user='simple'):
    with Session(engine) as session:
        new_user = User(id=id_user, name=name_user, count_Ratings=count_Ratings_user, statys=statys_user)
        session.add(new_user)
        session.commit()

def look_id():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT id FROM user"))
        data = [i for row in data for i in row]
        print(data)
    return data

def look_statys():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT statys FROM user"))
        data = [i for row in data for i in row]
        print(data)
    return data

def look_count_Ratings():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT count_Ratings FROM user"))
        data = [i for row in data for i in row]
        print(data)
    return data

def new_ratings(id_user):
    if id_user not in look_id():
        return 'Аккаунт не найден'
    else:
        with Session(engine) as session:
            user = session.get(User, id_user)
            user.count_Ratings += 1
            session.commit()
        return 'Оценка поставленна.'
    
def look_person(id_user=0):
    with engine.begin()as conn:
        lists_bd = conn.execute(text("SELECT * FROM user"))
        flag = False
        for i in lists_bd:
            if id_user == i[0]:
                result = i
                break
        else:
            result = 'У вас нет аккаунта'
        return result

def delet_person(id_user=0):
    flag = look_person(id_user=id_user)
    if type(flag) == str:
        return flag
    else:
        with engine.begin()as conn:
            conn.execute(text(f"DELETE FROM user WHERE id = {id_user}"))
            conn.commit
            return 'Аккаунт успешно удален.'
