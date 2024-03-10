import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from familybot.db.crud import *
import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.environ.get("BOT_KEY")

bot = telebot.TeleBot(bot_key)

init_tables()

in_family = False  # TODO если in_family = False, то при начале общения с ботом появляется кнопка "Добавиться в семью" и "Создать семью", нужно реализовать проверку на 'состоит ли пользователь в семье'

identificator = 'aaa'  # TODO реализовать генерацию уникального идентификатора для каждой семьи


def gen_markup(btns: list[str]):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(btn) for btn in btns])
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    person = get_person_by_tg(message.from_user.id)
    if person is None or person.family is None:
        if person is None:
            fn = message.from_user.first_name
            ln = message.from_user.last_name
            fname = ' '.join([fn if fn else '', ln if ln else ''])
            insert_persons([Person(telegram_id=message.from_user.id, name=fname)])
        btn1 = KeyboardButton("Добавиться в семью")
        btn2 = KeyboardButton("Создать семью")
        markup.add(btn1, btn2)
    else:
        btn1 = KeyboardButton("Список покупок✍️")
        btn2 = KeyboardButton("Настройки⚙️")
        markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    person = get_person_by_tg(message.from_user.id)
    if person is None:
        bot.send_message(message.from_user.id, text='Сначала напишите /start !')
        return
    match message.text:
        case "Добавить покупку":
            markup = gen_markup(["Очистить список❌"])
            markup = gen_markup(["Главное меню"])
            purchase = message.text

        case 'Список покупок✍️':
            markup = gen_markup(["Добавить покупку", "Очистить список❌"])
            markup.add(KeyboardButton("Главное меню"))
            bot.send_message(message.from_user.id, text="Ваш список покупок:", reply_markup=markup)
        case "Главное меню":
            markup = gen_markup(["Список покупок✍️", "Настройки⚙️"])
            bot.send_message(message.from_user.id, "Привет! Я семейный бот покупок.", reply_markup=markup)
        case "Настройки⚙️":
            markup = gen_markup(["Семья", "Инструкция"])
            markup.add(KeyboardButton('Главное меню'))
            bot.send_message(message.from_user.id, "Раздел настроек:", reply_markup=markup)
        case "Очистить список❌":
            markup = gen_markup(["Да", "Нет"])
            bot.send_message(message.from_user.id, "Вы уверены, что хотите очистить список покупок?", reply_markup=markup)
        case "Нет":
            markup = gen_markup(["Добавить покупку", "Очистить список❌"])
            markup.add(KeyboardButton("Главное меню"))
            bot.send_message(message.from_user.id, text="Ваш список покупок:", reply_markup=markup)
        case "Да": #TODO функция очистки списка покупок.
            markup = gen_markup(["Добавить покупку", "Очистить список❌"])
            markup.add(KeyboardButton("Главное меню"))
            person = get_person_by_tg(message.from_user.id)
            person.purchases = []
            bot.send_message(message.from_user.id, text="Ваш список покупок успешно очищен", reply_markup=markup)
        case "Семья":
            markup = gen_markup(["Главное меню"])
            bot.send_message(message.from_user.id, text=f"Уникальный идентификатор семьи: {identificator}", reply_markup=markup)
        case "Добавиться в семью":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.from_user.id, "Введите уникальный идентификатор семьи, в которую хотите добавиться", reply_markup=markup) #TODO при вводе уникального идентификатора, пользователь добавляется в нужную семью
        case "Создать семью":
            markup = gen_markup(["Главное меню"])
            person = get_person_by_tg(message.from_user.id)
            family = person.create_family()
            bot.send_message(message.from_user.id, "Вы успешно создали семью!\nПосмотреть уникальный идентификатор семьи, чтобы добавить других участников, вы можете в настройках ",reply_markup=markup)
        case "Инструкция":
            markup = gen_markup(["Главное меню"])
            bot.send_message(message.from_user.id,"✔️Чтобы добавить покупку перейдите в главное меню => добавить покупку => введите покупку в чат\n\n"
                                                  "✔️Чтобы удалить купленные товары, нажмите на соответствующий товар или очистите список целиком\n\n"
                                                  "✔️Чтобы добавить нового члена семьи, сообщите ему уникальный идентификатор, взяв его из настроек => семья",reply_markup=markup)


        case _:
            # Ни один не сработал
            pass


bot.polling(none_stop=True, interval=0)
