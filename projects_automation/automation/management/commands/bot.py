import os
from django.core.management.base import BaseCommand
from environs import Env
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Updater
from automation.handlers import project_handler



env = Env()
env.read_env()

tg_token = env('TELEGRAM_TOKEN')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        updater = Updater(tg_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(project_handler)

        updater.start_polling()
        updater.idle()
