import os
import telebot
from dotenv import load_dotenv
from enum import Enum, auto
from telebot import types
from my_bd import *
from random import randint
from bd_streets import *
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
    start_registration = True
    bot.send_message(message.chat.id, 'Пожалуйста, введите ваше имя пользователя.')


@bot.message_handler(commands=['d'])
def start(message):
    delete()


@bot.message_handler(commands=['stop'])
def start(message):
    global flag
    flag = False
    print(flag)
#--------------------------------------------------------------------------------------

def eco_all_total(message, statys):
    global result
    total_id = look_id()
    id = message.chat.id
    print(1, statys)
    if statys not in ('volunteer', 'simple'):
        statys = '-'
        print(2)
    if id not in total_id:
        id = message.chat.id
        name = result[0]
        print({name: type(name), statys:type(statys)})
        new_person(id_user=id, name_user=name, count_Ratings_user=0, statys_user=statys)
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
    if message.text[0] != '/' and len(message.text) < 20 and message.text.strip() != '':
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
/e,  /estimation — Оценить улицу ''')


@bot.message_handler(commands=['delete', 'del'])
def replacement_akk(message):
    flag = delet_person(id_user=message.chat.id)
    bot.send_message(message.chat.id, flag)    


@bot.message_handler(commands=['look', 'l'])
def replacement_akk(message):
    look = look_person(id_user=message.chat.id)
    if type(look) == str:
        bot.send_message(message.chat.id, look)
    else:
        bot.send_message(message.chat.id, f'''Ваш никнейм ——> {look[1]}
Ваше колличество оценок ——> {look[2]}
Ваш статус ——> {look[-1]}''')



@bot.message_handler(commands=['pazor', 'p'])
def pazor_street(message):
    with open('project_tg_bot/data_streets.json', encoding='utf-8') as fl:
        result = json.load(fl)
    min_ball = 6
    streets = {}
    for i in result:
        if round(sum(result[i]) / len(result[i]), 2) < min_ball:
            row = pazor_street_result(streets=streets, street={i: result[i]})
            streets, min_ball = row[0], row[1]
    streets_1 = sorted(streets, key=lambda x: streets[x])
    print(streets_1)
    streets = [f'{i} - {streets[i]}' for i in streets_1]
    print(streets)
    bot.send_message(message.chat.id, f'''Вот топ 5 самых загрязнённых улиц на данный момент: 
1. {streets[0]}
2. {streets[1]}
3. {streets[2]}
4. {streets[3]}
5. {streets[4]}''')


@bot.message_handler(commands=['estimation', 'e'])
def estimation_streets(message):
    if type(look_person(id_user=message.chat.id)) == str:
        bot.send_message(message.chat.id, 'Для того чтобы оценивать загрязнённость улиц, создайте аккаунт')
    else:
        global start_estimation_streets
        start_estimation_streets = True
        bot.send_message(message.chat.id, 'Введите название улицы, которую хотите оценить.')


@bot.message_handler(func=lambda x: start_estimation_streets)
def estimation_streets_2(message):
    row = proverka_streets(street=message.text)
    if row[0]:
        bot.send_message(message.chat.id, f'Вот средний балл {message.text} на данный момент: {round(sum(row[1]) / len(row[1]), 2)}')
        global streets
        streets = message.text
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
    bot.send_message(message.chat.id, estimation_streets_ball(streets=streets, id_user=message.chat.id, ball=0))

@bot.callback_query_handler(func=lambda call: call.data == 'button1') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, estimation_streets_ball(streets=streets, id_user=message.chat.id, ball=1))

@bot.callback_query_handler(func=lambda call: call.data == 'button2') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, estimation_streets_ball(streets=streets, id_user=message.chat.id, ball=2))

@bot.callback_query_handler(func=lambda call: call.data == 'button3') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, estimation_streets_ball(streets=streets, id_user=message.chat.id, ball=3))

@bot.callback_query_handler(func=lambda call: call.data == 'button4') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, estimation_streets_ball(streets=streets, id_user=message.chat.id, ball=4))

@bot.callback_query_handler(func=lambda call: call.data == 'button5') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, estimation_streets_ball(streets=streets, id_user=message.chat.id, ball=5))

@bot.callback_query_handler(func=lambda call: call.data == 'button6') 
def save_btn(call):
    message = call.message
    bot.send_message(message.chat.id, 'Оценка не поставленна.')

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

