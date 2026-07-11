from start_bd import *
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import select, update

def look_tg_id():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT tg_id FROM users"))
        data = [i for row in data for i in row]
        print(data)
    return data

def look_name():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT name FROM users"))
        data = [i for row in data for i in row]
        print(data)
    return data


def look_statys():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT status FROM users"))
        data = [i for row in data for i in row]
        print(data)
    return data

def look_count_Ratings():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT count_ratings FROM users"))
        data = [i for row in data for i in row]
        print(data)
    return data


def new_ratings(id_user):
    if id_user not in look_tg_id():
        return 'Аккаунт не найден'
    else:
        with Session(engine) as session:
            user = session.get(User, id_user)
            print(user.date, 1111, '-' * 30)
            # if user.ratings_today >= 5:
            #     return 'Превышен лимит оценок за сегодня.' 
            # user.count_ratings += 1
            print(user.date.strftime("%Y-%m-%d"), date.today().strftime("%Y-%m-%d"))
            if user.date.strftime("%Y-%m-%d") != date.today().strftime("%Y-%m-%d"):
                user.date = date.today()
                user.ratings_today = 1
                user.count_ratings += 1
            else:
                if user.ratings_today >= 5:
                    print(11111111111111111111)
                    return 'Превышен лимит оценок за сегодня.' 
                user.count_ratings += 1
                user.ratings_today += 1
            session.commit()
        print('Оценка поставленна.')
        return 'Оценка поставленна.'


def look_person(tg_id=0):
    with engine.begin()as conn:
        lists_bd = conn.execute(text(f"SELECT * FROM users WHERE tg_id = {tg_id}"))
        data = [*lists_bd]
        if data == []:
            return 'У вас нет аккаунта'
        print(data[0])
        with Session(engine) as session:
            print('ashyshhssh'* 10)
            user = session.get(User, tg_id)
            print(user.date, 1111, '-' * 30)
            # if user.ratings_today >= 5:
            #     return 'Превышен лимит оценок за сегодня.' 
            # user.count_ratings += 1
            print(user.date.strftime("%Y-%m-%d"), date.today().strftime("%Y-%m-%d"))
            if user.date.strftime("%Y-%m-%d") != date.today().strftime("%Y-%m-%d"):
                user.date = date.today()
                user.ratings_today = 0
                data[0] = data[0][:4] + (0,) + data[0][5:]
            
            print(data[0])
            session.commit()
        return data[0]
    

def look_rating_today(id_user):
    if id_user not in look_tg_id():
        return 'Аккаунт не найден'
    person = look_person(tg_id=id_user)
    return {person[4]: person[1]}


def delete_person(id_user=0):
    flag = look_person(tg_id=id_user)
    if type(flag) == str:
        return flag
    else:
        with engine.begin()as conn:
            conn.execute(text(f"DELETE FROM users WHERE tg_id = {id_user}"))
            conn.commit
            return 'Аккаунт успешно удален.'

def look_status_person(tg_id: int) -> str:
    if tg_id not in look_tg_id():
        return 'У вас нет аккаунта'
    with engine.begin()as conn:
        status = conn.execute(text(f"SELECT status FROM users WHERE tg_id = {tg_id}"))
        status = [i for row in status for i in row][0]
        dicts = {'volunteer': 'Волонтер', 'simple': 'Обычный пользователь'}
        status = dicts.get(status)
        if not status:
            return 'Ошибка статуса'
        print(status)
    return status


def day_ended(data=date.today().strftime("%Y-%m-%d")):
    with engine.begin()as conn:
        count_active_peple = conn.execute(text(f"SELECT date FROM users"))
        count_active_peple = [i for row in count_active_peple for i in row]
        count_active_peple = count_active_peple.count(data)
        print(count_active_peple)
        count_peple = conn.execute(text(f"SELECT COUNT() FROM users"))
        count_peple = [i for row in count_peple for i in row][0]
        print(count_peple)
    return count_peple, count_active_peple
