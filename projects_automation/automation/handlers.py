import uuid
from collections import defaultdict
from datetime import datetime
import django

from environs import Env
# from secret_santa.models import Participant
# from secret_santa.models import SantaGame
# from secret_santa.serve import get_random_wishlist
# from secret_santa.serve import get_santas
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

env = Env()
env.read_env()

participants_info = defaultdict()
games_info = defaultdict()
param_value = defaultdict()


START_PROJECT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Участвовать в проекте'),
        ],
    ],
    resize_keyboard=True
)


ASK_TIME_FROM_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='17:00'),
            KeyboardButton(text='17:30'),
        ],
        [
            KeyboardButton(text='18:00'),
            KeyboardButton(text='18:30'),
        ],
        [
            KeyboardButton(text='19:00'),
            KeyboardButton(text='19:30'),
        ],
        [
            KeyboardButton(text='20:00'),
            KeyboardButton(text='20:30'),
        ],
    ],
    resize_keyboard=True
)

ASK_TIME_TO_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='17:30'),
            KeyboardButton(text='18:00'),
        ],
        [
            KeyboardButton(text='18:30'),
            KeyboardButton(text='19:00'),
        ],
        [
            KeyboardButton(text='19:30'),
            KeyboardButton(text='20:00'),
        ],
        [
            KeyboardButton(text='20:30'),
            KeyboardButton(text='21:00'),
        ],
    ],
    resize_keyboard=True
)


def start(update, context):
    message = update.message
    user_name = message.chat.first_name
    user_id = message.chat_id

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Привет, {user_name}.🤚\n\n'
            'Скоро стартует проект! Будешь участвовать?'
        ),
        reply_markup=START_PROJECT_KEYBOARD
    )

    return 1


def ask_student_time_from(update, context):
    message = update.message
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text='Укажи удобное время начала',
        reply_markup=ASK_TIME_FROM_KEYBOARD
    )

    return 2


def test(update, context):
    pass


def stop(update):
    update.message.reply_text("Стоп")
    return ConversationHandler.END


project_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start)],

    states={
        1: [MessageHandler(Filters.text, ask_student_time_from)],
        2: [MessageHandler(Filters.text, test)],
    },

    fallbacks=[CommandHandler('stop', stop)]
)
