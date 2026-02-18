from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, text
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, date, time, timedelta
from my_bd import *
from bd_street_rating import *
import json

Base = declarative_base()
engine = create_engine(
    "sqlite:///project_tg_bot/bd/mybd.sqlite3",
    echo=True
)

class User(Base):
    __tablename__ = "street"
    # id = Column(Integer)
    name_street = Column(String, primary_key=True)
    time_street = Column(String)
    old_rating = Column(Float)
    mean_rating = Column(Float)
    count_rating = Column(Integer)
    old_count_rating = Column(Integer)
    count_rating_today = Column(Integer)

Base.metadata.create_all(engine)


def delete():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM streets"))

def new_person_street(street_user='', rating=5, user_count_rating=5):
    with Session(engine) as session:
        time_t = date.today().strftime("%Y-%m-%d")
        time_t = '2026-01-31'
        new_user = User(name_street=street_user, time_street=time_t, old_rating=rating, mean_rating=rating, count_rating=user_count_rating, old_count_rating=user_count_rating, count_rating_today=0)
        session.add(new_user)
        session.commit()


def street_in_json():
    with open('project_tg_bot/data_streets.json', encoding='utf-8') as fl:
        result = json.load(fl)
    for i in result:
        row = result.get(i)
        new_person_street(street_user=i, rating=round(sum(row) / len(row), 2), user_count_rating=len(row))

def name_street():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT name_street FROM street"))
        data = [i for row in data for i in row]
    return data

def pazor_street_bd():
    with Session(engine) as session:
        streets = session.query(User).order_by(User.mean_rating).all()
        
        min_ball = 7
        pazor_streets = []
        
        for user in streets:
            if user.mean_rating < min_ball:
                pazor_streets.append({user.mean_rating: user.name_street})
                if len(pazor_streets) >= 5:
                    break
    pazor_streets = [f'{i[j]} - {j}' for i in pazor_streets for j in i]
    print(pazor_streets)
    return pazor_streets

def estimation_streets_ball_bd(streets, id_user, ball):
    print(streets, streets in name_street())
    if streets in name_street():
        # with Session(engine) as session:
        #     user = session.get(User, id_user)
        flag = 'Оценка поставленна.'
        flag1 = look_rating_today(id_user=id_user)
        for i in flag1:
            flag1 = i
        if flag1 >= 5:
            flag = 'Превыщен лимит оценок за сегодня, попробуйте завтра'
        else:
            if flag != new_ratings(id_user=id_user):
                flag = 'Оценка не поставленна.'
        if flag == 'Оценка поставленна.':
            with Session(engine) as session:
                user = session.get(User, streets)
                rating = [user.mean_rating for i in range(user.count_rating)]
                rating.append(ball)
                user.count_rating += 1
                user.count_rating_today += 1
                user.mean_rating = round(sum(rating) / len(rating), 2)
                session.commit()
        return flag
    else:
        return 'Оценка не поставленна.'

def proverka_street(street):
    if street in name_street():
        with Session(engine) as session:
            user = session.get(User, street)
            mean_ball = user.mean_rating
        return True, mean_ball
    else:
        return False
    
# def new_day():
#     with Session(engine) as session:
#         streets = session.query(User)
#         for user in streets:
#             time_day = user.time_street
#             break
#         if old_day() == time_day:
#             print(1010101010101)
#             with engine.begin() as conn:
#                 data_best = conn.execute(text('''SELECT *
#                                         FROM street
#                                         WHERE (mean_rating - old_rating) > 0'''))

#                 data_best = [i for i in data_best]
#                 data_name = [i[0] for i in data_best]
#                 print(data_best)
#                 data = conn.execute(text('''SELECT *
#                                         FROM street
#                                         WHERE (mean_rating - old_rating) < 0'''))

#                 print(data, 11111111)
#                 data = [i for i in data]
#                 data_name += [i[0] for i in data]
#                 print(data_name)
#                 for street in data_name:
#                     with Session(engine) as session:
#                         user = session.get(User, street)
#                         user.old_rating = user.mean_rating
#                         user.count_rating_today = 0
#                         user.old_count_rating = user.count_rating

#                 dicts = {i[0]: round(100 - round(i[3] / (i[2] / 100), 2), 2) for i in data}
#                 print(data_name)
#                 print(dicts, 111111111)
#         else:
#             return 'День еще не прошел'


# # datetime - дата и время
# now = datetime.now()  # 2024-01-15 14:30:45.123456
# print(now, type(now))

# # date - только дата
# today = date.today()  # 2024-01-15
# print(today)

# # time - только время
# current_time = datetime.now().time()  # 14:30:45.123456

# # timedelta - разница между датами
# delta = timedelta(days=7)  # 7 дней
# # Из строки (парсинг)
# dt1 = datetime.strptime('2024-01-15', '%Y-%m-%d')
# dt2 = datetime.strptime('15.01.2024 14:30', '%d.%m.%Y %H:%M')
# dt3 = datetime.strptime('11-11-11', '%d-%m-%y')  # 11 ноября 2011 года

# # Из отдельных компонентов
# dt4 = datetime(2024, 1, 15)  # год, месяц, день
# dt5 = datetime(2024, 1, 15, 14, 30, 45)  # год, месяц, день, час, минута, секунда