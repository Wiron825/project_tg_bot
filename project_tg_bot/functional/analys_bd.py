from start_bd import *
from sqlalchemy.orm import Session
from datetime import date, datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import select, update
from street_bd import *


def count_person_in_time():
    with Session(engine) as session:
        date_old_mouth = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m-%d')
        date_today = date.today().strftime("%Y-%m-%d")

        sql = text('''SELECT COUNT()
                FROM users
                WHERE date >= :my_date''')
        count_peple_today = session.execute(sql, {"my_date": date_today}).scalar()

        sql = text('''SELECT COUNT()
                FROM users
                WHERE date >= :my_date''')
        count_peple_old_mounth = session.execute(sql, {"my_date": date_old_mouth}).scalar()

        print(count_peple_today, count_peple_old_mounth)
        return count_peple_today, count_peple_old_mounth


def most_old_date():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT MIN(date) FROM users"))
        data = [i for row in data for i in row][0]
        print(data[:10])
    return data[:10]


def count_person_in_week():
    with Session(engine) as session:
        total_result = []
        for i in range(10):
            current_day = date.today() - timedelta(days=i)
            date_str = current_day.strftime('%Y-%m-%d')

            sql = text('''SELECT COUNT()
                    FROM users
                    WHERE strftime('%Y-%m-%d', date) = :my_date''')
            total_result.append(session.execute(sql, {"my_date": date_str}).scalar())

        my_day = total_result[0]
        sort_result = sorted(total_result, reverse=True)
        if sort_result.index(my_day) <= 5:
            text_result = 'Сегодня больше чем в среднем за неделю людей посетило данный бот'
        else:
            text_result = 'Сегодня меньше чем в среднем за неделю людей посетило данный бот'

        print(total_result, sort_result, text_result)
        return total_result, my_day, text_result


def most_estimation_street():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT street_id FROM changes"))
        data = [i for row in data for i in row]
        
        dicts = {}
        for i in data:
            if i not in dicts:
                dicts[i] = 1
            else:
                dicts[i] += 1
        
        max_estimations = [-1]
        max_estimations_keys = [-1]
        for key, value in dicts.items():
            if len(max_estimations) < 3:
                max_estimations.append(value)
                max_estimations_keys.append(key)
            elif value > min(max_estimations):
                index = max_estimations.index(min(max_estimations))
                max_estimations[index] = value
                max_estimations_keys[index] = key
        
        max_estimations_keys = [street_by_id(id_s=i) for i in max_estimations_keys]
        total_lists = sorted(list(zip(max_estimations, max_estimations_keys)), reverse=True)
        # max_estimations, max_estimations_keys = zip(*lists)
        # max_estimations, max_estimations_keys = list(max_estimations), list(max_estimations_keys)
    
        print(total_lists)
    return total_lists


most_estimation_street()
# most_old_date()     
# count_person_in_week()
# count_person_in_time()

