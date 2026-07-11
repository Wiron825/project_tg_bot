import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from password import PASSWORD
from analys_bd import *

#для тех кто поместил токен в config.py
from config import TOKEN
import os
from enum import Enum, auto
# from my_bd import *
from random import randint
# from bd_streets import *
# from bd_rating_street import *
from start_bd import *
from user_bd import *
from street_bd import *
from changes_bd import *
import json

vk_session = vk_api.VkApi(token=TOKEN) #для людей поместивших токен в config
vk_api.VkApi(token='Ваш токен') #Для остальных
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

start_registration = False
start_estimation_streets = False
start_estimation_streets_2 = False
result = []
streets = ''
start_info = False
start_coments = False

dicts_person = {}


def sender(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0)


def start(id):
    vk.messages.send(user_id=id, message='👋 Привет! Я бот, готовый вам помочь.', random_id=0)
    vk.messages.send(user_id=id, message='Для начала можете ознакомиться со всем списком каманд, для этого напишите m или menu', random_id=0)


def cancel_registraition(id=id):
    global dicts_person
    dicts_person[id]['result'] = []
    if dicts_person[id]['start_registration']:
        dicts_person[id]['start_registration'] = False
        sender(id=id, text='Регистрация прервана.')
        # bot.send_message(message.chat.id, 'Регистрация прервана.')
    else:
        sender(id=id, text='Регистрации на данный момент небыло.')
        # bot.send_message(message.chat.id, 'Регистрации на данный момент небыло.')


def start_registraithion(id):
    global dicts_person
    if id in look_tg_id(): #----------------------------------------------
        # bot.send_message(message.chat.id, 'У вас уже есть аккаунт')
        sender(id=id, text='У вас уже есть аккаунт')
        result = []
        if dicts_person.get(id):
            dicts_person[id]['start_registration'] = False
    else:
        if dicts_person.get(id):
            dicts_person[id]['start_registration'] = True
        # start_registration = True
        sender(id=id, text='Пожалуйста, введите ваше имя пользователя.')
        # bot.send_message(message.chat.id, 'Пожалуйста, введите ваше имя пользователя.')


def eco_all_total(id, statys):
    global dicts_person
    total_id = look_tg_id() #-----------------------------------
    if statys not in ('volunteer', 'simple'):
        statys = '-'
        print(2)
    if id not in look_tg_id():  #------------------------------
        name = dicts_person[id]['result'][0]
        print({name: type(name), statys:type(statys)})
        print(id)
        new_user(id_user=id, name=name, count_ratings=0, status=statys) #---------------------------------
        sender(id=id, text='Поздравляю, регистрация прошла успешно.')
        # bot.send_message(message.chat.id, 'Поздравляю, регистрация прошла успешно.')
    else: 
        sender(id=id, text='У вас уже есть аккаунт')
        # bot.send_message(message.chat.id, 'У вас уже есть аккаунт')
   
    # result = []
    dicts_person[id]['result'] = []
    dicts_person[id]['start_registration'] = False
    # global start_registration
    # start_registration = False


def eco_all(id, text):
    global dicts_person
    print(text)
    print(dicts_person[id]['result'])
    if text.strip() in look_name():
        sender(id=id, text='Ваш никнейм уже занят придумайте другой.')
    elif text[0] != '/' and len(text) < 20 and text.strip() != '':
        print(1)
        if len(dicts_person[id]['result']) == 0:
            dicts_person[id]['result'] += [text]
            print(text, 123)
        else:
            text = text.lower().strip()
            dicts = {'волонтер': 'volunteer', 'обычный пользователь': 'simple'}
            if text not in dicts:
                sender(id=id, text='Статус может быть либо волонтер либо обычный пользователь, укажтье кто вы')
            else:
                # dicts_person[id]['result'] += [text]
                dicts_person[id]['result'] += [dicts[text]]
                # result.append(dicts[text])
        if len(dicts_person[id]['result']) == 1:
            print(dicts_person[id]['result'])
            sender(id=id, text='Теперь выберите ваш статус: Волонтер или обычный пользователь')
            # keyboard = types.InlineKeyboardMarkup()
            # button1 = types.InlineKeyboardButton(text='Волонтер', callback_data='volunteer')
            # button2 = types.InlineKeyboardButton(text='Обычный пользователь', callback_data='simple')
            # keyboard.add(button1, button2)
            # bot.send_message(message.chat.id, 'Теперь выберите ваш статус',reply_markup=keyboard)
        elif len(dicts_person[id]['result']) == 2:
            eco_all_total(id=id, statys=dicts_person[id]['result'][1])
        print(23767)
    else:
        if len(dicts_person[id]['result']) == 0:
            sender(id=id, text='Ваш никнейм не уместен придумайте другой.')
            # bot.send_message(message.chat.id, 'Ваш никнейм не уместен придумайте другой.')
        # else:
        #     bot.send_message(message.chat.id, 'Ваш пароль не уместен придумайте другой.')
        print(dicts_person[id]['result'])


def rename(id):
    sender(id=id, text='Вот все команды доступные на данный момент:')
    sender(id=id, text='''/s ,  /start  — Запустить бота
m ,  menu  — Показать меню комманд
r ,  registration  — Регистрация профиля
c ,  cancel  — Остановить регистрацию профиля
l ,  look  — Посмотреть свой профиль
del ,  delete  — Удалить свой аккаунт
p,  pazor — Вывод самых загрязненных улиц
e,  estimation — Оценить улицу 
b,  best — Вывод самых активных пользователей
d,  dop — Дополнительные возможности''')
    sender(id=id, text='Для того чтоб активировать команду просто напишите ее название')


def replacement_akk(id=id):
    flag = delete_person(id_user=id) #----------------------------------------
    sender(id=id, text=flag) 


def look_akk(id=id):
    look = look_person(tg_id=id)
    print(look, 43674356743565463756347)
    if type(look) == str:
        sender(id=id, text=look)
    else:
        dicts = {'simple': 'Обычный пользователь', 'volunteer': 'Волонтер'}
        statys = dicts.get(look[3])
        if statys == None:
            statys = '-'
        sender(id=id, text= f'''Ваш никнейм ——> {look[1]}
Ваше колличество оценок за все время ——> {look[2]}
Ваше колличество оценок за сегодня ——> {look[4]}
Ваш статус ——> {statys}''')
#         bot.send_message(message.chat.id, f'''Ваш никнейм ——> {look[1]}
# Ваше колличество оценок за все время ——> {look[2]}
# Ваше колличество оценок за сегодня ——> {look[4]}
# Ваш статус ——> {statys}''')


def pazor_street_1(id=id):
    streets = pazor_street() #---------------------------------------------------------------
    print(streets)
    sender(id=id, text=f'''Вот топ 5 самых загрязнённых улиц на данный момент: 
1. {streets[0]}
2. {streets[1]}
3. {streets[2]}
4. {streets[3]}
5. {streets[4]}''')


def estimation_streets(id=id):
    if type(look_person(tg_id=id)) == str:
        # bot.send_message(message.chat.id, 'Для того чтобы оценивать загрязнённость улиц, создайте аккаунт')
        sender(id=id, text='Для того чтобы оценивать загрязнённость улиц, создайте аккаунт')
    else:
        global dicts_person
        dicts_person[id]['start_estimation_streets'] = True
        # start_estimation_streets = True
        sender(id=id, text='Введите название улицы, которую хотите оценить.')
        # bot.send_message(message.chat.id, 'Введите название улицы, которую хотите оценить.')   


def estimation_streets_2(id, text):
    text = text[0].upper() + text[1:]
    row = proverka_street(street=text) #---------------------------------------------------------
    print(text, 123)
    print(row)
    global dicts_person
    if row[0]:
        sender(id=id, text=f'Вот средний балл {text} на данный момент: {row[1]}')
        # bot.send_message(message.chat.id, f'Вот средний балл {message.text} на данный момент: {row[1]}')
        dicts_person[id]['streets'] = text
        # streets = text
        print(dicts_person[id]['streets'], 101010110101010101)
        # keyboard = types.InlineKeyboardMarkup()
        # button1 = types.InlineKeyboardButton(text='0', callback_data='button0')
        # button2 = types.InlineKeyboardButton(text='1', callback_data='button1')
        # button3 = types.InlineKeyboardButton(text='2', callback_data='button2')
        # button4 = types.InlineKeyboardButton(text='3', callback_data='button3')
        # button5 = types.InlineKeyboardButton(text='4', callback_data='button4')
        # button6 = types.InlineKeyboardButton(text='5', callback_data='button5')
        # button7 = types.InlineKeyboardButton(text='Не ставить оценку', callback_data='button6')
        # keyboard.add(button1, button2, button3, button4, button5, button6, button7)
        # bot.send_message(message.chat.id, 'Нажмите на оценку, которую хотите поставить этой улице', reply_markup=keyboard)
        sender(id=id, text='Напишите оценку от 0 до 5, которую хотите поставить этой улице.')
        dicts_person[id]['start_estimation_streets_2'] = True
    else:
        dicts_person[id]['streets'] = text
        sender(id=id, text='Улица не найдена.')
        # bot.send_message(message.chat.id, 'Улица не найдена.')
    # global start_estimation_streets, start_estimation_streets_2
    dicts_person[id]['start_estimation_streets'] = False
    # start_estimation_streets = False
    # start_estimation_streets_2 = True


def estimation_streets_3(id, text):
    global dicts_person
    text = text.lower().strip()
    if text == 'нет':
        sender(id=id, text='Оценка не поставленна.')
        dicts_person[id]['start_estimation_streets_2'] = False
        # start_estimation_streets_2 = False
    elif not text.isdigit() or (not '0' <= text <= '5') or len(text) != 1:
        sender(id=id, text='Оценка улици должна быть от 0 до 5, если не хотите оценивать улицу напишите нет')
    else:
        text1 = estimation_streets_ball_bd(streets=dicts_person[id]['streets'], id_user=id, ball=int(text))
        print(text1, 282828)
        sender(id=id, text=text1)
        # bot.send_message(message.chat.id, estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=1))
        if text1 == 'Оценка поставленна.':
            # bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
            sender(id=id, text='Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
            # global start_coments
            # start_coments = True
            dicts_person[id]['start_coments'] = True
        dicts_person[id]['start_estimation_streets_2'] = False


def start_com(id, text):
    if text.lower().strip() == 'нет':
        # bot.send_message(message.chat.id, 'Коментарий не отправлен')
        sender(id=id, text='Коментарий не отправлен')
    else:
        street = id_street(street=streets)
        new_coment(street_id=street, coment=text)
        sender(id=id, text='Коментарий успешно добавлен, спасибо за обоснование своей оценки, нам это очень помагает')
        # bot.send_message(message.chat.id, 'Коментарий успешно добавлен, спасибо за обоснование своей оценки, нам это очень помагает')
    global dicts_person
    dicts_person[id]['start_coments'] = False


def best_users(id):
    users_id = look_tg_id() #-------------------------------------
    print(1)
    users_rating = [look_rating_today(id_user=ids) for ids in users_id]
    print(2)
    users_rating = [{look_person(tg_id=i)[1]: look_person(tg_id=i)[2]} for i in look_tg_id()] #---------------------------------
    print(users_rating, 1111)
    best_rating = []
    n = 5 if len(users_rating) >= 5 else len(users_rating)
    print(222, n)
    for _ in range(n):
        max_r = [-1, -1, {-1: -1}]
        for j in users_rating:
            for x in j:
                print(j, x)
                if j[x] > max_r[0]:
                    max_r[0] = j[x]
                    max_r[1] = users_rating.index(j)
                    max_r[2] = j
        print(max_r)
        best_rating.append(max_r[2])
        # print(users_rating.index(max(users_rating)))
        x = users_rating.pop(max_r[1])
    s = ''
    for i in range(len(best_rating)):
        for j in best_rating[i]:
            s += f'{i + 1}. {j} - {best_rating[i][j]}\n'
    sender(id=id, text=f'''Вот самые актывные пользователи:
Имя пользователя - Количество оценок:
{s}''')


def proverka_status(id):
    status = look_status_person(tg_id=id)
    if status == 'Ошибка статуса':
        sender(id=id, text='Извините, выскочила не большая ошибка, но мы постараемся ее исправить как можно быстрее.')
    elif status == 'Обычный пользователь':
        sender(id=id, text='Извините, вы обычный полозователь и вам не доступны особые возможности.')
    elif status == 'У вас нет аккаунта':
        sender(id=id, text=status)
    else:
        return True


def dop_options(id):
    if proverka_status(id=id):
        sender(id=id, text='''Вот доп возможности:
i,  info — вывод улиц результата сканирования улицы''')


def worse_streets(id):
    if proverka_status(id=id):
        sender(id=id, text='Введите название улицы, которую хотите просмотреть:')
        global dicts_person
        dicts_person[id]['start_info'] = True


def start_info_change(id, text):
    if proverka_status(id=id):
        if text in name_street():
            result = info_change(id_street=id_street(street=text))
            #count_change_month, count_change_today, mean_ball_month, mean_ball_today, rating_mounth, new_rating
            sender(id=id, text=f'''Вот результат сканирования оценок:       
Количество оценок за этот месяц — {result[0]}
Количество оценок за сегодня — {result[1]}
Средний балл оценок за этот месяц — {result[2]}
Средний балл оценок за сегодня — {result[3]}
Ретинг улицы месяц назад — {result[4]}
Ретинг улицы на данный момент — {result[5]}''')
#             bot.send_message(message.chat.id, f'''Вот результат сканирования оценок:       
# Количество оценок за этот месяц — {result[0]}
# Количество оценок за сегодня — {result[1]}
# Средний балл оценок за этот месяц — {result[2]}
# Средний балл оценок за сегодня — {result[3]}
# Ретинг улицы месяц назад — {result[4]}
# Ретинг улицы на данный момент — {result[5]}''')
        else:
            sender(id=id, text='Улица не найдена.')
    global dicts_person
    dicts_person[id]['start_info'] = False


def most_dop_option_2(id):
    sender(id=id, text='Здраствуйте, после анализа данных выяснилось следующее:')
    count_peple_today, count_peple_old_mounth = count_person_in_time()
    sender(id=id, text=f'''Количество людей посетивших бот сегодня - {count_peple_today},
Количество людей посетивших бот за этот месяц - {count_peple_old_mounth}''')

    total_result, my_day, total_text = count_person_in_week()
    sender(id=id, text=total_text)

    total_list = most_estimation_street()
    s = ''
    for i in total_list:
        s += f'{i[1]} - {i[0]}\n'
    sender(id=id, text=f'''Вот топ 3 самых посещаемых улиц:
{s}''')


def most_dop_option(id, text):
    global dicts_person
    if text.lower().strip() == PASSWORD:
        most_dop_option_2(id=id)
    else:
        sender(id=id, text='Пароль не верный')
    dicts_person[id]['most_dop'] = False


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text
            id = event.user_id

            if id not in dicts_person:
                dicts_person[id] = {'start_registration': False, 
                'start_estimation_streets': False,
                'start_estimation_streets_2': False,
                'result': [],
                'streets': '',
                'start_info': False,
                'start_coments': False,
                'most_dop': False}
                start(id)
            print(dicts_person[id]['result'])

            if msg.lower().strip() == 'c' or msg.lower().strip() == 'cancel':
                cancel_registraition(id=id)
            elif dicts_person[id]['start_registration']:
                eco_all(id=id, text=msg)
            elif dicts_person[id]['start_estimation_streets']:
                estimation_streets_2(id=id, text=msg)
            elif dicts_person[id]['start_estimation_streets_2']:
                estimation_streets_3(id=id, text=msg)
            elif dicts_person[id]['start_coments']:
                start_com(id=id, text=msg)
            elif dicts_person[id]['start_info']:
                start_info_change(id=id, text=msg)
            elif dicts_person[id]['most_dop']:
                most_dop_option(id=id, text=msg)
            elif msg.lower().strip() == 'most':
                sender(id=id, text='Введите пароль.')
                dicts_person[id]['most_dop'] = True
            elif msg.lower().strip() == 'i' or msg.lower().strip() == 'info':
                worse_streets(id=id)
            elif msg.lower().strip() == 'd' or msg.lower().strip() == 'dop':
                dop_options(id=id)
            elif msg.lower().strip() == 'b' or msg.lower().strip() == 'best':
                best_users(id=id)
            elif msg.lower().strip() == 'del' or msg.lower().strip() == 'delete':
                replacement_akk(id=id)
            elif msg.lower().strip() == 'l' or msg.lower().strip() == 'look':
                look_akk(id=id)
            elif msg.lower().strip() == 'p' or msg.lower().strip() == 'pazor':
                pazor_street_1(id=id)
            elif msg.lower().strip() == 'e' or msg.lower().strip() == 'estimation':
                estimation_streets(id=id)
            elif msg == 'hi':
                sender(id, 'hello')
            elif msg.lower().strip() == 's' or msg.lower().strip() == 'start':
                start(id)
            elif msg.lower().strip() == 'm' or msg.lower().strip() == 'menu':
                rename(id)
            elif msg.lower().strip() == 'r' or msg.lower().strip() == 'registraition':
                start_registraithion(id=id)
