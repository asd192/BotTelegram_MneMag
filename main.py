import telebot

with open("API-Token.txt", "r", encoding="UTF8") as token:
    token = token.readline().strip()

bot = telebot.TeleBot(token)