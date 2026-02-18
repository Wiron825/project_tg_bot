from start_bd import *
from user_bd import *
from street_bd import *
from datetime import date


def look_changes_today():
    with engine.begin() as conn:
        data = conn.execute(text('''SELECT *
                                  FROM changes
                                  WHERE date >= DATE('now', 'localtime') 
                                 AND date < DATE('now', 'localtime', '+1 day')'''))
        data = [i for i in data]
    return data



def look_change_street_today(street: int, time_limit: str):
    if street not in name_street():
        return 'Улица не найдена'
    def f(value):
        if time_limit == 'day':
            with engine.begin() as conn:
                data = conn.execute(text(f'''SELECT COUNT()
                                        FROM changes
                                        WHERE date >= DATE('now', 'localtime') 
                                        AND date < DATE('now', 'localtime', '+1 day')
                                        AND value = {value}
                                        AND street_id = {id_street(street=street)}'''))
                changes = [i for row in data for i in row]
                return changes[0]
        elif time_limit == 'month':
            with engine.begin() as conn:
                data = conn.execute(text(f'''SELECT COUNT()
                                        FROM changes
                                        WHERE date >= DATE('now', 'localtime', '-30 day') 
                                        AND date < DATE('now', 'localtime', '+1 day')
                                        AND value = {value}
                                        AND street_id = {id_street(street=street)}'''))
                changes = [i for row in data for i in row]
                return changes[0]
        
    change_0 = f(0)
    change_1 = f(1)
    change_2 = f(2)
    change_3 = f(3)
    change_4 = f(4)
    change_5 = f(5)
    
    total_mean_ball = [0 for _ in range(change_0)] + [1 for _ in range(change_1)] + [2 for _ in range(change_2)]
    total_mean_ball += [3 for _ in range(change_3)] + [4 for _ in range(change_4)] + [5 for _ in range(change_5)]
    print(total_mean_ball, 111111)

    if time_limit == 'day':
        with engine.begin() as conn:
                data = conn.execute(text(f'''SELECT COUNT() 
                                        FROM changes
                                        WHERE date >= DATE('now', 'localtime') 
                                        AND date < DATE('now', 'localtime', '+1 day')
                                        AND street_id = {id_street(street=street)}'''))
                mean_ball_today = [i for row in data for i in row][0]
    elif time_limit == 'month':
        with engine.begin() as conn:
                data = conn.execute(text(f'''SELECT COUNT() 
                                        FROM changes
                                        WHERE date >= DATE('now', 'localtime', '-30 day') 
                                        AND date < DATE('now', 'localtime', '+1 day')
                                        AND street_id = {id_street(street=street)}'''))
                mean_ball_today = [i for row in data for i in row][0]

    if mean_ball_today == 0:
        return change_0, change_1, change_2, change_3, change_4, change_5, 0
    mean_ball_today = round(sum(total_mean_ball) / mean_ball_today, 2)
    print(change_0, change_1, change_2, change_3, change_4, change_5, mean_ball_today)
    return change_0, change_1, change_2, change_3, change_4, change_5, mean_ball_today



def old_ratinge_in_mounth(id_street: int):
    with engine.begin() as conn:
        data = conn.execute(text(f'''SELECT value
                                FROM changes
                                WHERE date >= DATE('now', 'localtime', '-30 day') 
                                AND date < DATE('now', 'localtime', '+1 day')
                                AND street_id = {id_street}'''))
        change_in_mounth = [i for row in data for i in row]

        date_street = conn.execute(text(f'''SELECT new_rating, count_rating
                                FROM streets
                                WHERE id = {id_street}'''))
        
        new_rating, count_rating = [i for row in date_street for i in row]

        total_sum = new_rating * count_rating
        removed_sum = sum(change_in_mounth)

        new_count = count_rating - len(change_in_mounth)
        old_rating = (total_sum - removed_sum) / new_count
        return round(old_rating, 2)
        


def info_change(id_street: int):
    with engine.begin() as conn:
        data = conn.execute(text(f'''SELECT COUNT()
                                FROM changes
                                WHERE date >= DATE('now', 'localtime') 
                                AND date < DATE('now', 'localtime', '+1 day')
                                AND street_id = {id_street}'''))

        count_change_month = conn.execute(text(f'''SELECT COUNT()
                                FROM changes
                                WHERE date >= DATE('now', 'localtime', '-30 day') 
                                AND date < DATE('now', 'localtime', '+1 day')
                                AND street_id = {id_street}''')) 

        new_rating = conn.execute(text(f'''SELECT new_rating
                                FROM streets
                                WHERE id = {id_street}'''))

        count_change_today = [i for row in data for i in row][0]
        count_change_month = [i for row in count_change_month for i in row][0]
        mean_ball_today = look_change_street_today(street=(street_by_id(id_s=id_street)), time_limit='day')[-1]
        mean_ball_month = look_change_street_today(street=(street_by_id(id_s=id_street)), time_limit='month')[-1]
        new_rating = [i for row in new_rating for i in row][0]
        rating_mounth = old_ratinge_in_mounth(id_street=id_street)
        return count_change_month, count_change_today, mean_ball_month, mean_ball_today, rating_mounth, new_rating
    


# print(look_change_street_today(street='Хрустальная улица'))

# def look_changes():
#     with engine.begin() as conn:
#         data = conn.execute(text('''SELECT *
#                                   FROM changes'''))
#         data = [i for i in data]
#         print(data)
#     return data

# print(look_changes()[-1])