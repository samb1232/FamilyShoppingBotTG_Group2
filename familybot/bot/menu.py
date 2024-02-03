import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.environ.get("BOT_KEY")

bot = telebot.TeleBot(bot_key)

in_family = False  # TODO если in_family = False, то при начале общения с ботом появляется кнопка "Добавиться в семью" и "Создать семью", нужно реализовать проверку на 'состоит ли пользователь в семье'

identificator = 'aaa'  # TODO реализовать генерацию уникального идентификатора для каждой семьи


def gen_markup(btns: list[str]):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(btn) for btn in btns])
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if in_family:
        btn1 = KeyboardButton("Список покупок✍️")
        btn2 = KeyboardButton("Настройки⚙️")
        markup.add(btn1, btn2)
    else:
        btn1 = KeyboardButton("Добавиться в семью")
        btn2 = KeyboardButton("Создать семью")
        markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    match message.text:
        case 'Список покупок✍️':
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Добавить покупку")
            btn2 = KeyboardButton("Очистить список❌")
            back = KeyboardButton("Главное меню")
            markup.add(btn1, btn2)
            markup.add(back)
            bot.send_message(message.chat.id, text="Ваш список покупок:", reply_markup=markup)
        case "Главное меню":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Список покупок✍️")
            btn2 = KeyboardButton("Настройки⚙️")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)
        case "Настройки⚙️":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Семья")
            btn2 = KeyboardButton("Оповещения")  #TODO через оповещения можно реализовать напоминания о покупке, либо можно бросить это дело (??)
            back = KeyboardButton('Главное меню')
            markup.add(btn1, btn2)
            markup.add(back)
            bot.send_message(message.from_user.id, "Раздел настроек:", reply_markup=markup)
        case "Очистить список❌":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Да")
            btn2 = KeyboardButton("Нет")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Вы уверены, что хотите очистить список покупок?", reply_markup=markup)
        case "Нет":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Добавить покупку")
            btn2 = KeyboardButton("Очистить список❌")
            back = KeyboardButton("Главное меню")
            markup.add(btn1, btn2)
            markup.add(back)
            bot.send_message(message.chat.id, text="Ваш список покупок:", reply_markup=markup)
        case "Да":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Добавить покупку")
            btn2 = KeyboardButton("Очистить список❌")
            back = KeyboardButton("Главное меню")
            markup.add(btn1, btn2)
            markup.add(back)
            bot.send_message(message.chat.id, text="Ваш список покупок успешно очищен", reply_markup=markup)
        case "Семья":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            back = KeyboardButton("Главное меню")
            markup.add(back)
            bot.send_message(message.chat.id, text=f"Уникальный идентификатор семьи: {identificator}", reply_markup=markup)
        case "Добавиться в семью":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.from_user.id, "Введите уникальный идентификатор семьи, в которую хотите добавиться", reply_markup=markup) #TODO при вводе уникального идентификатора, пользователь добавляется в нужную семью
        case "Создать семью":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Главное меню")
            markup.add(btn1)
            bot.send_message(message.from_user.id, "Вы успешно создали семью!\nПосмотреть уникальный идентификатор семьи, чтобы добавить других участников, вы можете в настройках ",reply_markup=markup)
        case _:
            # Ни один не сработал
            pass


bot.polling(none_stop=True, interval=0)
