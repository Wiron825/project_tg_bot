from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import declarative_base, Session
from datetime import date

Base = declarative_base()
engine = create_engine(
    "sqlite:///project_tg_bot/bd/mybd.sqlite3",
    echo=True
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    count_Ratings = Column(Integer)
    statys = Column(String)
    ratings_today = Column(Integer)
    data = Column(String)

Base.metadata.create_all(engine)


def delete():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM user"))

def new_person(id_user=0, name_user='', count_Ratings_user=0, statys_user='simple'):
    print(1)
    if id_user == 0:
        print('sdkidikjjdjddjj')
    with Session(engine) as session:
        data_user = date.today().strftime("%Y-%m-%d")
        print(date.today().strftime("%Y-%m-%d"))
        print(id_user, name_user, count_Ratings_user, statys_user, data_user)
        new_user = User(id=id_user, name=name_user, count_Ratings=count_Ratings_user, statys=statys_user, ratings_today=0, data=data_user)
        print(1)
        print(new_user)
        session.add(new_user)
        session.commit()
    print(1)

def look_id():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT id FROM user"))
        data = [i for row in data for i in row]
        print(data)
    return data

def look_name():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT name FROM user"))
        data = [i for row in data for i in row]
        print(data)
    return data

# def chek_data(id_user):
#     if id_user not in look_id():
#         return 'Аккаунт не найден'
#     else:
#         with Session(engine) as session:
#             user = session.get(User, id_user)
#             data_l = user.data
#             session.commit()
#     return date.today() == data_l


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
            if user.data != date.today().strftime("%Y-%m-%d"):
                user.data = date.today().strftime("%Y-%m-%d")
                user.ratings_today = 1
            else:
                user.ratings_today += 1
            session.commit()
        print('Оценка поставленна.')
        return 'Оценка поставленна.'

def look_person(id_user=0):
    with engine.begin()as conn:
        lists_bd = conn.execute(text("SELECT * FROM user"))
        flag = False
        for i in lists_bd:
            if id_user == i[0]:
                result = i
                with Session(engine) as session:
                    user = session.get(User, id_user)
                    if user.data != date.today():
                        user.data = date.today()
                        user.ratings_today = 0
                break
        else:
            result = 'У вас нет аккаунта'
        return result

def look_rating_today(id_user):
    if id_user not in look_id():
        return 'Аккаунт не найден'
    person = look_person(id_user=id_user)
    return {person[4]: person[1]}

def delet_person(id_user=0):
    flag = look_person(id_user=id_user)
    if type(flag) == str:
        return flag
    else:
        with engine.begin()as conn:
            conn.execute(text(f"DELETE FROM user WHERE id = {id_user}"))
            conn.commit
            return 'Аккаунт успешно удален.'

def day_ended(data=date.today().strftime("%Y-%m-%d")):
    with engine.begin()as conn:
        count_active_peple = conn.execute(text(f"SELECT data FROM user"))
        count_active_peple = [i for row in count_active_peple for i in row]
        count_active_peple = count_active_peple.count(data)
        print(count_active_peple)
        count_peple = conn.execute(text(f"SELECT COUNT() FROM user"))
        count_peple = [i for row in count_peple for i in row][0]
        print(count_peple)
    return count_peple, count_active_peple
print(day_ended())
