import telebot
from telebot import types

from db_queries import link_shops_read_db
from db_queries import log_errors

# добываем токен
try:
    with open("API-Token.txt", "r", encoding="UTF8") as token:
        token = token.readlines()[2].strip()
except:
    log_errors("Не могу получить доступ к файлу для получения токена")
    
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def menu_down(message):
    """Крафт и отправка нижнего меню"""
    keyboard_down = types.ReplyKeyboardMarkup(True, False)

    keyboard_down.row('Магазины')
    keyboard_down.row('На сайт')
    keyboard_down.row('Помощь')

    bot.send_message(message.chat.id, "Привет. Выбирай.", reply_markup=keyboard_down)


@bot.message_handler(content_types=['text'])
def get_menu_shops(message):
    """Крафт и отправка чат-меню"""
    if message.text == 'Магазины':

        shops_dict = {
            'Детские': 'Детские',
            'Дом\Сад\Дача': 'Для дома и сада',
            'Косметика\Здоровье': 'Косметика и здоровье',
            'Игры\Софт': 'Игры \ Софт',
            'Одежда\Обувь': 'Одежда \ Обувь',
            'Книги': 'Книги',
            'Спорт\Активный отдых': 'Спорт \ Активный отдых',
            'Обучение': 'Обучение',
            'Ювелирные': 'Ювелирные',
            'Строительство\Ремонт': 'Строительство \ Ремонт',
            'Техника\Электроника': 'Техника \ Электроника',
            'Транспорт\Запчасти': 'Транспорт \ Запчасти',
            'Подарки\Сувениры': 'Подарки \ Сувениры',
            'Искусство': 'Искусство',
            'Животные\Растения': 'Животные\Растения',
            'Мегамаркеты': 'МегаМаркеты'
        }

        # выбираем тип клавиатуры
        keyboard_shops = types.InlineKeyboardMarkup()

        # крафтим кнопоки
        shop_list, columns, = [], 3
        for name_button, name_db in shops_dict.items():
            line_buttons = types.InlineKeyboardButton(text=name_button, callback_data=name_db)
            shop_list.append(line_buttons)
            if len(shop_list) == columns:
                keyboard_shops.add(shop_list[0], shop_list[1], shop_list[2])
                shop_list.clear()
        if len(shop_list) == 2:
            keyboard_shops.add(shop_list[0], shop_list[1])
        else:
            keyboard_shops.add(shop_list[0])

        # отправляем кнопки пользователю
        bot.send_message(message.from_user.id, text='Выбирай категорию', reply_markup=keyboard_shops)

    if message.text == 'На сайт':
        # выбираем тип клавиатуры
        keyboard_site = types.InlineKeyboardMarkup()

        # крафтим кнопоку
        key_url_main = types.InlineKeyboardButton(text='MneMag.ru', url='https://mnemag.ru')
        keyboard_site.add(key_url_main)

        # отправляем кнопку пользователю
        bot.send_message(message.chat.id, "Нажми на кнопку для перехода на сайт", reply_markup=keyboard_site)

    if message.text == 'Помощь':
        bot.send_message(message.chat.id, "Магазины - меню магазинов\nНа сайт - ссылка на сайт\nПомощь - помощь")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Если сообщение поступило из чата с ботом, запросить ссылки"""
    if call.message:
        shop_urls = link_shops_read_db(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=shop_urls)

    # Если сообщение из инлайн-режима
    # elif call.inline_message_id:
    #     print('inline message')


bot.polling(none_stop=True, interval=0)
