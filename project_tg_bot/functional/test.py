import os
import telebot
from dotenv import load_dotenv
from enum import Enum, auto
from telebot import types
# from my_bd import *
from random import randint
# from bd_streets import *
# from bd_rating_street import *
from start_bd import *
from user_bd import *
from street_bd import *
from changes_bd import *
import json

flag = True

load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created (запущен)')


start_registration = False
start_estimation_streets = False
result = []
streets = ''
start_info = False
start_coments = False

@bot.message_handler(commands=['start', 's'])
def start(message):
    bot.send_message(message.chat.id, '👋 Привет! Я бот, готовый вам помочь.')
    bot.send_message(message.chat.id, 'Для начала можете ознакомиться со всем списком каманд по команде /m или /menu')
    
@bot.message_handler(commands=['cancel', 'c'])
def cancel_registraition(message):
    global result
    result = []
    global start_registration
    if start_registration:
        start_registration = False
        bot.send_message(message.chat.id, 'Регистрация прервана.')
    else:
        bot.send_message(message.chat.id, 'Регистрации на данный момент небыло.')

@bot.message_handler(commands=['registraition', 'r'])
def start(message):
    global start_registration
    if message.chat.id in look_tg_id(): #----------------------------------------------
        bot.send_message(message.chat.id, 'У вас уже есть аккаунт')
        result = []
        start_registration = False
    else:
        start_registration = True
        bot.send_message(message.chat.id, 'Пожалуйста, введите ваше имя пользователя.')


# @bot.message_handler(commands=['d'])
# def start(message):
#     delete_users() #------------------------------------


@bot.message_handler(commands=['stop'])
def start(message):
    global flag
    flag = False
    print(flag)
#--------------------------------------------------------------------------------------

def eco_all_total(message, statys):
    global result
    total_id = look_tg_id() #-----------------------------------
    id = message.chat.id
    print(1, statys)
    if statys not in ('volunteer', 'simple'):
        statys = '-'
        print(2)
    if id not in look_tg_id():  #------------------------------
        name = result[0]
        print({name: type(name), statys:type(statys)})
        print(id)
        new_user(id_user=message.chat.id, name=name, count_ratings=0, status=statys) #---------------------------------
        bot.send_message(message.chat.id, 'Поздравляю, регистрация прошла успешно.')
    else:
        bot.send_message(message.chat.id, 'У вас уже есть аккаунт')

    result = []
    global start_registration
    start_registration = False


@bot.message_handler(func=lambda x: start_registration)
def eco_all(message):
    global result
    print(message.text)
    if message.text.strip() in look_name():
        bot.send_message(message.chat.id, 'Ваш никнейм уже занят придумайте другой.')
    elif message.text[0] != '/' and len(message.text) < 20 and message.text.strip() != '':
        print(1)
        result.append(message.text)
        if len(result) == 1:
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text='Волонтер', callback_data='volunteer')
            button2 = types.InlineKeyboardButton(text='Обычный пользователь', callback_data='simple')
            keyboard.add(button1, button2)
            bot.send_message(message.chat.id, 'Теперь выберите ваш статус',reply_markup=keyboard)
        elif len(result) == 2:
            eco_all_total(message=message)
    else:
        if len(result) == 0:
            bot.send_message(message.chat.id, 'Ваш никнейм не уместен придумайте другой.')
        # else:
        #     bot.send_message(message.chat.id, 'Ваш пароль не уместен придумайте другой.')
        print(result)


@bot.callback_query_handler(func=lambda call: call.data == 'volunteer') 
def save_btn(call):
    message = call.message
    eco_all_total(message=message, statys='volunteer')

@bot.callback_query_handler(func=lambda call: call.data == 'simple') 
def save_btn(call):
    message = call.message
    eco_all_total(message=message, statys='simple')

# def start_opr_statys(message):
#     bot.send_message(message.chat.id, 'Теперь введите ваш пароль.')





@bot.message_handler(commands=['m', 'menu'])
def rename(message):
    bot.send_message(message.chat.id, 'Вот все команды доступные на данный момент:')
    bot.send_message(message.chat.id, '''/s ,  /start  — Запустить бота
/m ,  /menu  — Показать меню комманд
/r ,  /registration  — Регистрация профиля
/c ,  /cancel  — Остановить регистрацию профиля
/l ,  /look  — Посмотреть свой профиль
/del ,  /delete  — Удалить свой аккаунт
/p,  /pazor — Вывод самых загрязненных улиц
/e,  /estimation — Оценить улицу 
/b,  /best — Вывод самых активных пользователей
/d,  /dop — Дополнительные возможности''')


@bot.message_handler(commands=['delete', 'del'])
def replacement_akk(message):
    flag = delete_person(id_user=message.chat.id) #----------------------------------------
    bot.send_message(message.chat.id, flag)    


@bot.message_handler(commands=['look', 'l'])
def replacement_akk(message):
    look = look_person(tg_id=message.chat.id)
    print(look, 43674356743565463756347)
    if type(look) == str:
        bot.send_message(message.chat.id, look)
    else:
        dicts = {'simple': 'Обычный пользователь', 'volunteer': 'Волонтер'}
        statys = dicts.get(look[3])
        if statys == None:
            statys = '-'
        bot.send_message(message.chat.id, f'''Ваш никнейм ——> {look[1]}
Ваше колличество оценок за все время ——> {look[2]}
Ваше колличество оценок за сегодня ——> {look[4]}
Ваш статус ——> {statys}''')



@bot.message_handler(commands=['pazor', 'p'])
def pazor_street_1(message):
    streets = pazor_street() #---------------------------------------------------------------
    print(streets)
    bot.send_message(message.chat.id, f'''Вот топ 5 самых загрязнённых улиц на данный момент: 
1. {streets[0]}
2. {streets[1]}
3. {streets[2]}
4. {streets[3]}
5. {streets[4]}''')


@bot.message_handler(commands=['estimation', 'e'])
def estimation_streets(message):
    if type(look_person(tg_id=message.chat.id)) == str:
        bot.send_message(message.chat.id, 'Для того чтобы оценивать загрязнённость улиц, создайте аккаунт')
    else:
        global start_estimation_streets
        start_estimation_streets = True
        bot.send_message(message.chat.id, 'Введите название улицы, которую хотите оценить.')


@bot.message_handler(func=lambda x: start_estimation_streets)
def estimation_streets_2(message):
    row = proverka_street(street=message.text) #---------------------------------------------------------
    print(row)
    if row[0]:
        bot.send_message(message.chat.id, f'Вот средний балл {message.text} на данный момент: {row[1]}')
        global streets
        streets = message.text
        print(streets, 101010110101010101)
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='0', callback_data='button0')
        button2 = types.InlineKeyboardButton(text='1', callback_data='button1')
        button3 = types.InlineKeyboardButton(text='2', callback_data='button2')
        button4 = types.InlineKeyboardButton(text='3', callback_data='button3')
        button5 = types.InlineKeyboardButton(text='4', callback_data='button4')
        button6 = types.InlineKeyboardButton(text='5', callback_data='button5')
        button7 = types.InlineKeyboardButton(text='Не ставить оценку', callback_data='button6')
        keyboard.add(button1, button2, button3, button4, button5, button6, button7)
        bot.send_message(message.chat.id, 'Нажмите на оценку, которую хотите поставить этой улице', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Улица не найдена.')
    global start_estimation_streets
    start_estimation_streets = False


@bot.callback_query_handler(func=lambda call: call.data == 'button0') 
def save_btn(call):
    message = call.message
    text = estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=0)
    bot.send_message(message.chat.id, text)
    if text == 'Оценка поставленна.':
        bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
        global start_coments
        start_coments = True

@bot.callback_query_handler(func=lambda call: call.data == 'button1') 
def save_btn(call):
    message = call.message
    text = estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=1)
    bot.send_message(message.chat.id, text)
    # bot.send_message(message.chat.id, estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=1))
    if text == 'Оценка поставленна.':
        bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
        global start_coments
        start_coments = True

@bot.callback_query_handler(func=lambda call: call.data == 'button2') 
def save_btn(call):
    message = call.message
    text = estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=2)
    bot.send_message(message.chat.id, text)
    # bot.send_message(message.chat.id, estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=2))
    if text == 'Оценка поставленна.':
        bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
        global start_coments
        start_coments = True

@bot.callback_query_handler(func=lambda call: call.data == 'button3') 
def save_btn(call):
    message = call.message
    text = estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=3)
    bot.send_message(message.chat.id, text)
    # bot.send_message(message.chat.id, estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=3))
    if text == 'Оценка поставленна.':
        bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
        global start_coments
        start_coments = True

@bot.callback_query_handler(func=lambda call: call.data == 'button4') 
def save_btn(call):
    message = call.message
    text = estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=4)
    bot.send_message(message.chat.id, text)
    # bot.send_message(message.chat.id, estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=4))
    if text == 'Оценка поставленна.':
        bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
        global start_coments
        start_coments = True

@bot.callback_query_handler(func=lambda call: call.data == 'button5') 
def save_btn(call):
    message = call.message
    text = estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=5)
    bot.send_message(message.chat.id, text)
    # bot.send_message(message.chat.id, estimation_streets_ball_bd(streets=streets, id_user=message.chat.id, ball=5))
    if text == 'Оценка поставленна.':
        bot.send_message(message.chat.id, 'Хототе оставить коментарий (если да, то напишите его если нет, то напишите нет)')
        global start_coments
        start_coments = True

@bot.callback_query_handler(func=lambda call: call.data == 'button6') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, 'Оценка не поставленна.')

@bot.message_handler(func=lambda x: start_coments)
def start_com(message):
    if message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Коментарий не отправлен')
    else:
        street = id_street(street=streets)
        new_coment(street_id=street, coment=message.text)
        bot.send_message(message.chat.id, 'Коментарий успешно добавлен, спасибо за обоснование своей оценки, нам это очень помагает')
    global start_coments
    start_coments = False

@bot.message_handler(commands=['best', 'b'])
def dest_users(message):
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
    bot.send_message(message.chat.id, f'''Вот самые актывные пользователи:
Имя пользователя - Количество оценок:
{s}''')


def proverka_status(message):
    status = look_status_person(tg_id=message.chat.id)
    if status == 'Ошибка статуса':
        bot.send_message(message.chat.id, 'Извините, выскочила не большая ошибка, но мы постараемся ее исправить как можно быстрее.')
    elif status == 'Обычный пользователь':
        bot.send_message(message.chat.id, 'Извините, вы обычный полозователь и вам не доступны особые возможности.')
    elif status == 'У вас нет аккаунта':
        bot.send_message(message.chat.id, status)
    else:
        return True


@bot.message_handler(commands=['dop', 'd'])
def dop_options(message):
    if proverka_status(message=message):
        bot.send_message(message.chat.id, '''Вот доп возможности:
/i,  /info — вывод улиц результата сканирования улицы''')


@bot.message_handler(commands=['i', 'info'])
def worse_streets(message):
    if proverka_status(message=message):
        bot.send_message(message.chat.id, 'Введите название улицы, которую хотите просмотреть:')
        global start_info
        start_info = True

@bot.message_handler(func=lambda x: start_info)
def start_info_change(message):
    if proverka_status(message=message):
        if message.text in name_street():
            result = info_change(id_street=id_street(street=message.text))
            #count_change_month, count_change_today, mean_ball_month, mean_ball_today, rating_mounth, new_rating
            bot.send_message(message.chat.id, f'''Вот результат сканирования оценок:       
Количество оценок за этот месяц — {result[0]}
Количество оценок за сегодня — {result[1]}
Средний балл оценок за этот месяц — {result[2]}
Средний балл оценок за сегодня — {result[3]}
Ретинг улицы месяц назад — {result[4]}
Ретинг улицы на данный момент — {result[5]}''')
        else:
            bot.send_message(message.chat.id, 'Улица не найдена.')
    global start_info
    start_info = False

@bot.message_handler(func=lambda x: True)
def eco_all(message):
    bot.send_message(message.chat.id, message.text)

while flag:
    try:
        bot.polling(none_stop=True)
    except Exception as _e:
        print(_e)

# while 1:
#     bot.polling(none_stop=True)

