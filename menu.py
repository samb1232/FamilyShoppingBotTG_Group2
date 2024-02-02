import telebot
from key import bot_key
from telebot import types

bot = telebot.TeleBot(bot_key)

in_family = False #TODO если in_family = False, то при начале общения с ботом появляется кнопка "Добавиться в семью" и "Создать семью", нужно реализовать проверку на 'состоит ли пользователь в семье'
identificator = 'aaa' #TODO реализовать генерацию уникального идентификатора для каждой семьи
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if in_family:
        btn1 = types.KeyboardButton("Список покупок✍️")
        btn2 = types.KeyboardButton("Настройки⚙️")
        markup.add(btn1, btn2)
    else:
        btn1 = types.KeyboardButton("Добавиться в семью")
        btn2 = types.KeyboardButton("Создать семью")
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
        btn2 = types.KeyboardButton("Оповещения") #через оповещения можно реализовать напоминания о покупке, либо можно бросить это дело
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
        back = types.KeyboardButton("Главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text=f"Уникальный идентификатор семьи: {identificator}", reply_markup=markup)
    elif message.text == "Добавиться в семью":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.from_user.id, "Введите уникальный идентификатор семьи, в которую хотите добавиться", reply_markup=markup)
    elif message.text == "Создать семью":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        bot.send_message(message.from_user.id, "Вы успешно создали семью!\nПосмотреть уникальный идентификатор семьи, чтобы добавить других участников, вы можете в настройках ",reply_markup=markup)


bot.polling(none_stop=True, interval=0)