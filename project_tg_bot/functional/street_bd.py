from start_bd import *
from sqlalchemy.orm import Session
from user_bd import *
import json


def name_street():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT name_street FROM streets"))
        data = [i for row in data for i in row]
    return data


def streets_in_json():
    with open('project_tg_bot/data_streets.json', encoding='utf-8') as fl:
        data = json.load(fl)
    for street in data:
        row = data[street]
        new_street(name_street=street, old_count_rating=len(row), old_rating= round(sum(row) / len(row), 2))


def pazor_street():
    with engine.begin() as conn:
        data = conn.execute(text(f'''SELECT name_street, new_rating
                                 FROM streets
                                 ORDER BY new_rating ASC
                                 LIMIT 5'''))
        result = []
        for i in data:
            result.append(f'{i[0]} - {i[-1]}')
        print(result)
        return result


def id_street(street):
    with Session(engine) as session:
        sql = text('''
            SELECT id
            FROM streets
            WHERE name_street = :street
            ''')
        result = session.execute(sql, {"street": street}).scalar()
        print(result)
    return result


def street_by_id(id_s):
    with Session(engine) as session:
        sql = text('''
            SELECT name_street
            FROM streets
            WHERE id = :id
            ''')
        result = session.execute(sql, {"id": id_s}).scalar()
        print(result)
    return result


def estimation_streets_ball_bd(streets, id_user, ball):
    print(streets, streets in name_street())
    if streets in name_street():
        flag = 'Оценка поставленна.'
        flag1 = look_rating_today(id_user=id_user)
        print(flag1)
        for i in flag1:
            flag1 = i
        if flag1 >= 5:
            return 'Превыщен лимит оценок за сегодня, попробуйте завтра'
        else:
            if flag != new_ratings(id_user=id_user):
                return 'Оценка не поставленна.'
        if flag == 'Оценка поставленна.':
            if id_street(street=streets) != None:
                with Session(engine) as session:
                    id_streets = id_street(street=streets)
                    street = session.get(Street, id_streets)
                    
                    rating = [street.new_rating for _ in range(street.count_rating)]
                    rating.append(ball)

                    street.new_rating = round(sum(rating) / len(rating), 2)
                    street.count_rating += 1
                    street.count_rating_today += 1

                    session.commit()

                    new_change(user_tg_id=id_user, street_id=id_streets, value=ball)
                    return flag
            else:
                return 'Улица не найдена'
        else:
            return 'Оценка не поставленна.'


def proverka_street(street):
    if street in name_street():
        with Session(engine) as session:
            id_streets = id_street(street=street)
            street = session.get(Street, id_streets)
            print(street.new_rating)
            mean_ball = street.new_rating
        return True, mean_ball
    else:
        return False, 0

# print(estimation_streets_ball_bd(streets='1-й Автомобильный проезд', id_user=0, ball=0))


# def estimation_streets_ball_bd(streets, id_user, ball):
#     print(streets, streets in name_street())
#     if streets in name_street():
#         flag = 'Оценка поставленна.'
#         flag1 = look_rating_today(id_user=id_user)
#         print(flag1)
#         for i in flag1:
#             flag1 = i
#         if flag1 >= 5:
#             return 'Превыщен лимит оценок за сегодня, попробуйте завтра'
#         else:
#             if flag != new_ratings(id_user=id_user):
#                 return 'Оценка не поставленна.'
#         if flag == 'Оценка поставленна.':
#             with engine.begin() as conn:
#                 if id_street(street=streets) != None:
#                     user_row = conn.execute(
#                         select(street).where(street.c.id == id_street(street=streets))
#                     ).fetchone()


#                 with Session(engine) as session:
#                     user_row = conn.execute(
#                         select(street).where(street.c.id == id_street(street=streets))
#                     ).fetchone()
#                     print(2992892923, user_row)
#                     if not user_row:
#                         return 'Аккаунт не найден'

#                     rating = [user_row.mean_rating for i in range(user_row.count_rating)]
#                     rating.append(ball)
#                     print(rating, 111)
#                     conn.execute(
#                     update(street)
#                     .where(street.c.id == id_street(street=streets))
#                     .values(
#                         count_rating = user_row.count_rating + 1,
#                         count_rating_today = user_row.count_rating_today,
#                         new_rating = round(sum(rating) / len(rating), 2)
#                     )
#                 )

#                     # user = session.get(User, streets)
#                     # user.count_rating += 1
#                     # user.count_rating_today += 1
#                     # user.mean_rating = round(sum(rating) / len(rating), 2)
#                     # session.commit()
#                     # return flag
#                 return 'Улица не найдена'
#     else:
#         return 'Оценка не поставленна.'
# print(estimation_streets_ball_bd(streets='1-й Автомобильный проезд', id_user=0, ball=0))

# pazor_street()
# delete_streets()
# streets_in_json()
# print(name_street())
# # delete_streets()










# def name_street():
#     with engine.begin() as conn:
#         data = conn.execute(text("SELECT name_street FROM street"))
#         data = [i for row in data for i in row]
#     return data

# def pazor_street_bd():
#     with Session(engine) as session:
#         streets = session.query(User).order_by(User.mean_rating).all()
        
#         min_ball = 7
#         pazor_streets = []
        
#         for user in streets:
#             if user.mean_rating < min_ball:
#                 pazor_streets.append({user.mean_rating: user.name_street})
#                 if len(pazor_streets) >= 5:
#                     break
#     pazor_streets = [f'{i[j]} - {j}' for i in pazor_streets for j in i]
#     print(pazor_streets)
#     return pazor_streets

# def estimation_streets_ball_bd(streets, id_user, ball):
#     print(streets, streets in name_street())
#     if streets in name_street():
#         # with Session(engine) as session:
#         #     user = session.get(User, id_user)
#         flag = 'Оценка поставленна.'
#         flag1 = look_rating_today(id_user=id_user)
#         for i in flag1:
#             flag1 = i
#         if flag1 >= 5:
#             flag = 'Превыщен лимит оценок за сегодня, попробуйте завтра'
#         else:
#             if flag != new_ratings(id_user=id_user):
#                 flag = 'Оценка не поставленна.'
#         if flag == 'Оценка поставленна.':
#             with Session(engine) as session:
#                 user = session.get(User, streets)
#                 rating = [user.mean_rating for i in range(user.count_rating)]
#                 rating.append(ball)
#                 user.count_rating += 1
#                 user.count_rating_today += 1
#                 user.mean_rating = round(sum(rating) / len(rating), 2)
#                 session.commit()
#         return flag
#     else:
#         return 'Оценка не поставленна.'

# def proverka_street(street):
#     if street in name_street():
#         with Session(engine) as session:
#             user = session.get(User, street)
#             mean_ball = user.mean_rating
#         return True, mean_ball
#     else:
#         return False
