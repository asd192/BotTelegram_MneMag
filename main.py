import telebot
from telebot import types

with open("API-Token.txt", "r", encoding="UTF8") as token:
    token = token.readlines()[2].strip()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def menu_down(message):
    keyboard_down = types.ReplyKeyboardMarkup(True, False)

    keyboard_down.row('Магазины')
    keyboard_down.row('Перейти на сайт')
    keyboard_down.row('Помощь')

    bot.send_message(message.chat.id, "Привет. Выбирай.", reply_markup=keyboard_down)


@bot.message_handler(content_types=['text'])
def get_menu_shops(message):
    if message.text == 'Магазины':
        get_menu_shops(message)
    if message.text == 'Перейти на сайт':
        get_url_site(message)
    if message.text == 'Помощь':
        get_help(message)


@bot.message_handler(commands=['shop'])
def get_menu_shops(message):
    keyboard_shops = types.InlineKeyboardMarkup()

    key_megamarkets = types.InlineKeyboardButton(text='Мегамаркеты', callback_data='megamarkets')
    key_electronics = types.InlineKeyboardButton(text='Электроника', callback_data='electronics')
    keyboard_shops.add(key_megamarkets, key_electronics)

    bot.send_message(message.from_user.id, text='Выбирай категорию', reply_markup=keyboard_shops)


@bot.message_handler(commands=['site'])
def get_url_site(message):
    keyboard_site = types.InlineKeyboardMarkup()

    key_my_site = types.InlineKeyboardButton(text='MneMag.ru', url='https://mnemag.ru')
    keyboard_site.add(key_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку для перехода на сайт", reply_markup=keyboard_site)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, "/shop - меню магазинов\n/site - ссылка на сайт\n/help - помощь")


bot.polling(none_stop=True, interval=0)
