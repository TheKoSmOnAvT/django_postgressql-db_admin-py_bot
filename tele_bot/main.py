import telebot
from telebot import types
import psycopg2
#import sys

bot = telebot.TeleBot("515898591:AAFw4zoWuzDgtj19v9u8OVSbXG8xAlGBPvY")
menu_bool = False



@bot.message_handler(commands=['stop'])
def start(message):
    sys.exit(0)



@bot.message_handler(commands=['menu'])
def start(message):
    global menu_bool
    if menu_bool == False:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['laba1_person', 'Stop']])
        msg = bot.send_message(message.chat.id, 'open menu',  reply_markup=keyboard)
        bot.register_next_step_handler(msg, pick_menu)
        menu_bool = True
    else:
        menu_bool = False

        bot.send_message(message.chat.id, 'close menu', reply_markup=types.ReplyKeyboardRemove())

def pick_menu(message):

    if message.text == 'laba1_person':
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.send_message(message.chat.id, 'TABLE:', reply_markup=keyboard)
        query_st(message, 'select * from laba1_person')
    if message.text == '/menu':
        global menu_bool
        menu_bool = False
        bot.send_message(message.chat.id, 'close menu', reply_markup=types.ReplyKeyboardRemove())
    if message.text == 'Stop':
        msg = bot.send_message(message.chat.id, 'stoping')
        bot.stop_bot()

    # elif message.text == 'Список задач':
    #     state = 'Список задач'
    #     keyboard = types.ReplyKeyboardRemove()
    #
    #     goals = core.get_goals(message.chat.id)




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello user: " + message.from_user.first_name +"\n"+
                                      "Work done, write query.")
    

def print_db(attrib, mas, message):
    if(len(attrib)<1 or len(mas)<1 ):
        bot.send_message(message.chat.id, "Table is empty.")
    else:
        strs =' '
        for i in attrib:
            strs = strs +' || ' + str(i)
        strs = strs +' || ' +'\n'
        for i in mas:
            for j in i:
                strs = strs + ' || ' + str(j)
            strs = strs + ' || ' + '\n' + '*********' + '\n'
        bot.send_message(message.chat.id, strs)

def query(message):
    try:
        connection = psycopg2.connect(dbname='BaseToBD', user='postgres', password='12345', host='localhost')
        with connection.cursor() as cursor:
            cursor.execute(message.text) #выполняем запрос
            connection.commit()
            try:
                desc = cursor.description    #берем заголовки
                attrib = [col[0] for col in desc]
                mas = cursor.fetchall()    #берем массив данных (результаты запроса)
                print_db(attrib, mas, message)

            except:
                bot.send_message(message.chat.id, str("Do somethings"), reply_markup=types.ReplyKeyboardRemove())

    except psycopg2.Error as e:
        bot.send_message(message.chat.id, str(e),reply_markup=types.ReplyKeyboardRemove())

def query_st(message, str):
    try:
        connection = psycopg2.connect(dbname='BaseToBD', user='postgres', password='12345', host='localhost')
        with connection.cursor() as cursor:
            cursor.execute(str) #выполняем запрос
            connection.commit()
            try:
                desc = cursor.description    #берем заголовки
                attrib = [col[0] for col in desc]
                mas = cursor.fetchall()    #берем массив данных (результаты запроса)
                print_db(attrib, mas, message)

            except:
                bot.send_message(message.chat.id, str("Do somethings"),reply_markup=types.ReplyKeyboardRemove())

    except psycopg2.Error as e:
        bot.send_message(message.chat.id, str(e),reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'])
def start(message):
    query(message)

def start_bot():

    bot.polling()

start_bot()

