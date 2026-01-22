import os
import telebot
from dotenv import load_dotenv
from enum import Enum, auto
from telebot import types
from my_bd import *

flag = True

load_dotenv()
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created (запущен)')


@bot.message_handler(commands=['start', 's'])
def start(message):
    bot.send_message(message.chat.id, '👋 Привет! Я бот, готовый вам помочь.')
    

@bot.message_handler(commands=['test', 't'])
def start(message):
    id = look_id()
    if id != []:
        id = id[-1] + 1
    else:
        id = 1
    new_person(id_user=id)
    bot.send_message(message.chat.id, 'Все хорошо')


@bot.message_handler(commands=['delete', 'd'])
def start(message):
    delete()


@bot.message_handler(commands=['stop'])
def start(message):
    global flag
    flag = False
    print(flag)

@bot.message_handler(func=lambda x: True)
def eco_all(message):
    bot.send_message(message.chat.id, message.text)

# while flag:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as _e:
#         print(_e)
    
