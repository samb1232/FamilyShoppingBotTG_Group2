import telebot
from key import bot_key
from telebot import types

bot = telebot.TeleBot(bot_key)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Список покупок✍️")
    btn2 = types.KeyboardButton("Настройки⚙️")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Список покупок✍️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить покупку")
        btn2 = types.KeyboardButton("Очистить список❌")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2)
        markup.add(back)
        bot.send_message(message.chat.id, text="Ваш список покупок:", reply_markup=markup)
    elif message.text == "Главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Список покупок✍️")
        btn2 = types.KeyboardButton("Настройки⚙️")
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)
    elif message.text == "Настройки⚙️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Семья")
        btn2 = types.KeyboardButton("Оповещения") #через оповещения можно реализовать напоминания о покупке
        back = types.KeyboardButton('Главное меню')
        markup.add(btn1, btn2)
        markup.add(back)
        bot.send_message(message.from_user.id, "Раздел настроек:", reply_markup=markup)
    elif message.text == "Очистить список❌":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "Вы уверены, что хотите очистить список покупок?", reply_markup=markup)
    elif message.text == "Нет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить покупку")
        btn2 = types.KeyboardButton("Очистить список❌")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2)
        markup.add(back)
        bot.send_message(message.chat.id, text="Ваш список покупок:", reply_markup=markup)
    elif message.text == "Да":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить покупку")
        btn2 = types.KeyboardButton("Очистить список❌")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2)
        markup.add(back)
        bot.send_message(message.chat.id, text="Ваш список покупок успешно очищен", reply_markup=markup)
    elif message.text == "Семья":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить члена семьи")
        btn2 = types.KeyboardButton("Создать семью")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2)
        markup.add(back)
        bot.send_message(message.chat.id, text="Создать семью или добавить пользователя?", reply_markup=markup)


bot.polling(none_stop=True, interval=0)