import json 
from my_bd import *

def pazor_street_result(streets, street):
    def start(result):
        max_ball = -1
        flag = ''
        for i in result:
            if result[i]  > max_ball:
                max_ball = result[i]
                flag = i
        return flag, max_ball
    
    if len(streets) <= 4:
        for i in street:
            streets[i] = round(sum(street[i]) / len(street[i]), 2)
        flag, max_ball = start(result=streets)
        return streets, max_ball
    else:
        flag, max_ball = start(result=streets)
        for i in street:
            if round(sum(street[i]) / len(street[i]), 2) < max_ball:
                print(streets[flag])
                del streets[flag]
                streets[i] = round(sum(street[i]) / len(street[i]), 2)
        if len(streets) > 5 and streets.get(flag) != None:
            del streets[flag]
        flag, max_ball = start(result=streets)
        return streets, max_ball

def proverka_streets(street):
    with open('project_tg_bot/data_streets.json', encoding='utf-8') as fl:
        result = json.load(fl)
    return street in result, result.get(street)

def estimation_streets_ball(streets, id_user, ball):
    with open('project_tg_bot/data_streets.json', encoding='utf-8') as fl:
        result = json.load(fl)
    if result.get(streets) != None:
        result[streets].append(ball)
        with open('project_tg_bot/data_streets.json', 'w' , encoding='utf-8') as fl:
            json.dump(result, fl, ensure_ascii=False)
        flag = 'Оценка поставленна.'
        print(1)
        flag1 = look_rating_today(id_user=id_user)
        print(2)
        for i in flag1:
            flag1 = i
        print(flag1, type(flag1))
        if flag1 >= 5:
            flag = 'Превыщен лимит оценок за сегодня, попробуйте завтра'
        else:
            print(flag)
            if flag != new_ratings(id_user=id_user):
                flag = 'Оценка не поставленна.'
        return flag
    else: 
        return 'Оценка не поставленна.'
