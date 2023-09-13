import telebot
import datetime as dt
import datetime
import time
from telebot import types
from telebot.types import Message
from draf_google_sheets import checking_date_for_repeat
from draf_google_sheets import adding_last_event
from draf_google_sheets import writing_date_and_event

bot = telebot.TeleBot('')


def date_check(date):
    try:
        dates = dt.datetime.strptime(date, '%d.%m.%Y')
        if dt.datetime.now() < dates:
            if len(date.split('.')) == 3:
                try:
                    datetime.datetime.strptime(date, '%d.%m.%Y')
                    date = True
                    return date

                except Exception:
                    date = False
                    return date
            else:
                date = False
                return date
        else:
            date = False
            return date
    except:
        return False


users = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}, более подробную информацию обо мне  можешь узнать по команде /help ')


@bot.message_handler(commands=['help'])
def help(message: Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Что я умею', callback_data='get_info'))
    markup.add(types.InlineKeyboardButton(text='Добавлять даты и описания событий', callback_data='create_an_even'))
    markup.add(
        types.InlineKeyboardButton(text='Могу узнать твой персональный ID в телеграм', callback_data='get_my_tgId'))
    bot.send_message(message.chat.id, 'Вот мои возможности', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'get_info':
        bot.send_message(call.message.chat.id,
                         'Меня зовут Бот - Андрей,  я умею добавлять данные в таблицу будь это дата или описание события, также могу сказать тебе твой персональный ID в телеграм.')
    if call.data == 'get_my_tgId':
        bot.send_message(call.message.chat.id, f'Твой телеграм ID: {call.message.from_user.id}')
    if call.data == 'create_an_even':
        msg = bot.send_message(call.message.chat.id,
                               'Давай приступим. На какую дату ты хочешь создать напоминание? Введи, пожалуйста, дату следующего образца "13.06.2023", без ковычек')
        bot.register_next_step_handler(msg, user_answer)

    if call.data == 'YES':
        msg = bot.send_message(call.message.chat.id, 'Что вы хотите добавить к предыдущему описанию')
        bot.register_next_step_handler(msg, adding_last_event)
        time.sleep(15)
        bot.send_message(call.message.chat.id,
                         'Все изменения будут сохранены по этой ссылке. https://docs.google.com/spreadsheets/d/12UxfAdWfWzKTRE49rKLqssKjCU8vcXFe9di6dybDw_I/edit#gid=0')
    if call.data == 'NO':
        msg = bot.send_message(call.message.chat.id, 'Хорошо, на этом тогда закончим')


def user_answer(message):
    if date_check(message.text) == False:
        msg = bot.send_message(message.chat.id,
                               'Извини, тобой введенная дата не соответсвует образцу или она меньше той, которая сейчас, обратити внимание на год. Повтори попытку')
        bot.register_next_step_handler(msg, user_answer)
        time.sleep(3)
    else:
        answer_date = message.text
        if checking_date_for_repeat(answer_date) == True:
            bot.send_message(message.chat.id, 'На данную дату уже заплaнированы дела, желаете добавить описание?')
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Да', callback_data='YES'))
            markup.add(types.InlineKeyboardButton(text='Нет', callback_data='NO'))
            bot.send_message(message.chat.id, 'Выбирите нужный ответ', reply_markup=markup)

        else:
            answer_description = bot.send_message(message.chat.id, 'Запишите описание к дате')
            abs = bot.register_next_step_handler(answer_description, writing_date_and_event, answer_date)
            time.sleep(15)
            bot.send_message(message.chat.id,
                             'Дата и описание события будут успешны занесены в таблицу, вот ссылка https://docs.google.com/spreadsheets/d/12UxfAdWfWzKTRE49rKLqssKjCU8vcXFe9di6dybDw_I/edit#gid=0')


bot.polling(none_stop=True)
