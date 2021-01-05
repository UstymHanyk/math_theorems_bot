"""
Telegram bot designed for learning math analysis theorems
"""
import time
import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


theorems_list = []
current_theorem = []
users = {}
quotes = []

def read_quotes():
    with open('quotes.txt', "r") as file:
        for line in file.readlines():
            quotes.append(line)

read_quotes()

def read_theorems():
    with open('theorems.txt', "r") as file:
        theorem = file.readline()
        while theorem:
            name = file.readline().strip()
            theorem = file.readline().strip()
            theorems_list.append((name, 'images/' + theorem))
    theorems_list.pop(-1)  # delete blank object
read_theorems()
print(theorems_list)

def on_chat_message(usr_msg):
    """
    Reads user messages and responds to them
    :param usr_msg: user's telegram message object
    """
    content_type, chat_type, chat_id = telepot.glance(usr_msg)

    if content_type != 'text':
        bot.sendMessage(chat_id, "*Вибач,я розумію тільки текстові повідомлення😢*", parse_mode='Markdown')
        return
    usr_text = usr_msg['text']

    if usr_text == '/start':

        # users[f'{usr_msg["from"]["first_name"]}_{usr_msg["from"]["id"]}'] = 0j5
        # print('new user', users)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='🗞️ Випадкова теорема')]
            ], resize_keyboard=True)
        bot.sendMessage(chat_id, '*СІХ!* Якщо хочете стати розумнішими 🧠, зробити свої знання ' 
                                 'з *математичного аналізу* ґрунтовнішими, то натисніть на кнопку "🗞️ Випадкова теорема". '
                                 ' Побачивши назву теореми, постарайтеся згадати її означення',
                        reply_markup=markup, parse_mode='Markdown')

    elif usr_text == '🗞️ Випадкова теорема':

        current_theorem.append(random.choice(theorems_list))
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='📄 Означення', callback_data=current_theorem[-1][1])],
        ])
        bot.sendMessage(chat_id, current_theorem[-1][0], reply_markup=keyboard)

        print(current_theorem)

def on_callback_query(usr_msg):
    query_id, from_id, query_data = telepot.glance(usr_msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.sendPhoto(from_id, photo=open(query_data, 'rb'))
    bot.answerCallbackQuery(query_id, text=random.choice(quotes))

TOKEN = "1586720115:AAF6XIyHgm05sfe6K_WVlhkvRVVnyq_iEK8"
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print('Listening ...')
while 1:
    time.sleep(10)
