from datetime import datetime
from environs import Env
from .models import Student, Group, PM
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
TIME_FROM_PM, TIME_TO_PM, SAVE_INPUT_PM = range(3, 6)

START_PROJECT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Участвовать в проекте'),
        ],
    ],
    resize_keyboard=True
)

START_PROJECT_KEYBOARD_PM = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Приступить к управлению'),
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

ASK_TIME_FROM_KEYBOARD_PM = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='17:00'),
            KeyboardButton(text='17:30'),
        ],
        [
            KeyboardButton(text='18:00'),
            KeyboardButton(text='18:30'),
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

ASK_TIME_TO_KEYBOARD_PM = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='20:00'),
            KeyboardButton(text='20:30'),
        ],
        [
            KeyboardButton(text='21:00'),
            KeyboardButton(text='21:30'),
        ],
    ],
    resize_keyboard=True
)


def start(update, context):
    message = update.message
    user_name = message.chat.first_name
    user_id = message.chat_id

    pms = PM.objects.all()
    pm_id = [pm.tg_id for pm in pms]

    context.user_data['user_id'] = user_id
    context.user_data['name'] = user_name

    if user_id not in pm_id:
        context.bot.send_message(
            chat_id=user_id,
            text=(
                f'Привет, {user_name}.🤚\n\n'
                'Скоро стартует проект! Будешь участвовать?'
            ),
            reply_markup=START_PROJECT_KEYBOARD
        )

        return TIME_FROM
    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Привет, PM! How progress?\n\n'
            'Скоро стартуют проекты! Нужно твое чуткое управление'
        ),
        reply_markup=START_PROJECT_KEYBOARD_PM
    )
    return TIME_FROM_PM


def ask_student_time_from(update, context):
    message = update.message
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text='Укажи удобный для тебя интервал начала созвона',
        reply_markup=ASK_TIME_FROM_KEYBOARD
    )

    return TIME_TO


def ask_pm_time_from(update, context):
    message = update.message
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text='Укажи удобный для тебя интервал начала работы',
        reply_markup=ASK_TIME_FROM_KEYBOARD_PM
    )

    return TIME_TO_PM


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


def ask_pm_time_to(update, context):
    message = update.message
    user_id = message.chat_id
    context.user_data['working_interval_from'] = message.text
    context.bot.send_message(
        chat_id=user_id,
        text='Укажи удобный для тебя интервал конца работы',
        reply_markup=ASK_TIME_TO_KEYBOARD_PM
    )
    return SAVE_INPUT_PM


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


def save_pm_input(update, context):
    message = update.message
    user_id = message.chat_id
    context.user_data['working_interval_to'] = message.text
    PM.objects.update(
        tg_id=context.user_data['user_id'],
        name=context.user_data['name'],
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
        SAVE_INPUT: [MessageHandler(Filters.text, save_student_input)],
        TIME_FROM_PM: [MessageHandler(Filters.text, ask_pm_time_from)],
        TIME_TO_PM: [MessageHandler(Filters.text, ask_pm_time_to)],
        SAVE_INPUT_PM: [MessageHandler(Filters.text, save_pm_input)]
    },

    fallbacks=[CommandHandler('stop', stop)]
)
