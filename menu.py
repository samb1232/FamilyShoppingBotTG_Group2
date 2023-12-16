import telebot
from key import bot_key
from telebot import types

bot = telebot.TeleBot(bot_key)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Список покупок")
    btn2 = types.KeyboardButton("Настройки")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)

bot.polling(none_stop=True, interval=0)
