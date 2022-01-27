from datetime import datetime
from environs import Env
from automation.models import Student, Group
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

env = Env()
env.read_env()

TIME_FROM, TIME_TO, SAVE_INPUT = range(3)

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
    context.user_data['user_id'] = user_id
    context.user_data['name'] = user_name
    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Привет, {user_name}.🤚\n\n'
            'Скоро стартует проект! Будешь участвовать?'
        ),
        reply_markup=START_PROJECT_KEYBOARD
    )

    return TIME_FROM


def ask_student_time_from(update, context):
    message = update.message
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text='Укажи удобный для тебя интервал начала созвона',
        reply_markup=ASK_TIME_FROM_KEYBOARD
    )

    return TIME_TO


def ask_student_time_to(update, context):
    message = update.message
    user_id = message.chat_id
    context.user_data['working_interval_from'] = message.text
    context.bot.send_message(
        chat_id=user_id,
        text='Укажи удобный для тебя интервал конца созвона',
        reply_markup=ASK_TIME_TO_KEYBOARD
    )
    return SAVE_INPUT


def save_student_input(update, context):
    message = update.message
    user_id = message.chat_id
    context.user_data['working_interval_to'] = message.text
    if not Student.objects.filter(tg_id=context.user_data['user_id']):
        Student.objects.create(
            tg_id=context.user_data['user_id'],
            name=context.user_data['name'],
            level='new',
            working_interval_from=context.user_data['working_interval_from'],
            working_interval_to=context.user_data['working_interval_to']
        )
    else:
        Student.objects.update(
            working_interval_from=context.user_data['working_interval_from'],
            working_interval_to=context.user_data['working_interval_to']
        )
    context.bot.send_message(
        chat_id=user_id,
        text=f'Отлично! Данные сохранены',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def stop(update):
    update.message.reply_text("Стоп")
    return ConversationHandler.END


project_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start)],

    states={
        TIME_FROM: [MessageHandler(Filters.text, ask_student_time_from)],
        TIME_TO: [MessageHandler(Filters.text, ask_student_time_to)],
        SAVE_INPUT: [MessageHandler(Filters.text, save_student_input)]
    },

    fallbacks=[CommandHandler('stop', stop)]
)
