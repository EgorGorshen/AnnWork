from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message

import os
import analysis


load_dotenv()
bot = TeleBot(token=os.environ['TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def start(message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=
        f"""
Привет, я помогу тебе сделать аналитику вопросов Теста спилберга, вот мои команды:

1.  /start или /help - показывает команды этого бота

2.  /load - команда для загрузки двух файлов в формате JSON до и поле опроса

3.  /analytics - команда для аналитики по вопросам 

4.  /qr - команда для отправки ссылок и qr кода на Yandex form

5. /conclusion - команда для вывода среднего уровня тревожности 

Если будут просьбы чтобы добавить какие либо команды {os.environ['PHONE']}
        """
    )


@bot.message_handler(commands=['qr'])
def qr(message: Message):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=open('qr_before.jpg', 'rb'),
        caption="""
        Опрос до посещения

        https://forms.yandex.ru/u/637a20e7eb614681a83f9b86/
        """
    )

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open('qr_after.jpg', 'rb'),
        caption="""
        Опрос после посещения

        https://forms.yandex.ru/u/637a1f2feb6146818e3f9b86/
        """
    )



@bot.message_handler(commands=['load'])
def load(message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Отправьте файл с опросом до начала консультации'
    )
    bot.register_next_step_handler(message, load_before)


def load_before(message: Message):
    try:
        analysis.loading_db(message=message, bot=bot, type_db='before')
        bot.send_message(
            chat_id=message.chat.id,
            text='Отправьте файл с опросом после консультации'
        )
        bot.register_next_step_handler(message, load_after)
    except Exception as ex:
        bot.send_message(
            chat_id=message.chat.id,
            text='Извините произошла ошибка попробуйте загрузить файл заново.'
        )
        bot.send_message(
            chat_id=os.getenv('ADMIN'),
            text=ex.__str__()
        )


def load_after(message: Message):
    try:
        analysis.loading_db(message=message, bot=bot, type_db='after')
        bot.send_message(chat_id=message.chat.id, text='Файлы загружены, запустите команду /analytics для получения результата.')
        analysis.analysis()
    except Exception as ex:
        bot.send_message(
            chat_id=message.chat.id,
            text='Извините произошла ошибка попробуйте загрузить файлы заново. (/load)'
        )
        bot.send_message(
            chat_id=os.getenv('ADMIN'),
            text=ex.__str__()
        )


@bot.message_handler(commands=['analytics'])
def analytics(message: Message):
    analysis.analysis()
    photo = open('./db.png', 'rb')
    text = analysis.text()

    bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=text
    )


@bot.message_handler(commands=['conclusion'])
def conclusion(message: Message):

    conclusion = analysis.mean()
    bot.send_message(
        message.chat.id,
        text=f"""
        Общий уровень тревожности в группе тестируемых {"уменьшился" if conclusion > 0 else "увеличился"} на {round(abs(conclusion) * 100 / 3)}%
        """
    )


def print_admin(ex: Exception):
    bot.send_message(
        chat_id=os.getenv('ADMIN'),
        text=str(ex)
    )



if __name__ == "__main__":
    try:
        bot.polling(logger_level=2)
    except Exception as ex:
        print_admin(ex)

