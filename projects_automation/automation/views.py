import json

import telegram

from environs import Env

from pathlib import Path

from django.http import HttpResponseRedirect, HttpResponse

from dotenv import load_dotenv

from .models import PM, Student, Group

from .serve_old import assign_group, candidates_for_telegram_push, send_new_time_for_singles

from trello.trello import create_workspace, create_board, add_members_board

FILES_PATH = Path(__file__).resolve().parent / 'files/'

env = Env()
env.read_env()

trello_apikey = env('TRELLO_API_KEY')
trello_token = env('TRELLO_TOKEN')
telegram_token = env('TELEGRAM_TOKEN')

def handle_uploaded_file(file):
    Path(Path(__file__).resolve().parent / 'files').mkdir(parents=True, exist_ok=True)
    with open(FILES_PATH / 'users.json', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def upload_users(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['users_file'])
        with open(FILES_PATH / 'users.json') as file:
            users = json.load(file)
        managers = [user for user in users if user['role'] == "manager"]
        students = [user for user in users if user['role'] == "student"]
        for manager in managers:
            PM.objects.create(
                tg_id=manager['tg_id'],
                name=manager['name'],
                working_interval_from=manager['working_interval_from'],
                working_interval_to=manager['working_interval_to']
            )
        for student in students:
            Student.objects.create(
                tg_id=student['tg_id'],
                email=student['email'],
                name=student['name'],
                level=student['level'],
                working_interval_from=student['working_interval_from'],
                working_interval_to=student['working_interval_to']
            )
    return HttpResponseRedirect('/admin')


def assign_groups(request, level):
    assign_group(level)
    group_for_single = candidates_for_telegram_push()
    send_new_time_for_singles(group_for_single)
    return HttpResponse('Groups created.')


def create_wrksp(request):
    if request.method == 'POST' and trello_apikey:
        wrksp_name = request.POST.get('project', 'Проект Новый [01.12.2022-07.12.2022]')

        wrksp_id = create_workspace(trello_apikey, trello_token, wrksp_name)

        bot = telegram.Bot(token=telegram_token)

        groups = Group.objects.filter(
            pm__isnull=False,
            start_from__isnull=False,
            students__isnull=False
            ).distinct()
        groups = Group.objects.filter(id=16)
        for group in groups:
            board_name = (
                f'{group.start_from.strftime("%H:%M")} '
                f'{", ".join([str(student.name) for student in group.students.all()])}'
            )

            board_id, board_url = create_board(trello_apikey, trello_token, wrksp_id, board_name, group.pm.board_bg)
            group.board_url = board_url
            group.save()

            for student in group.students.all():
                add_members_board(trello_apikey, trello_token, board_id, student.email)
                #print(f'TODO отправка в TG {student.tg_id} ссылки {board_url}')
                #bot.send_message(chat_id=student.tg_id, text=board_url)
                message = f'Добро пожаловать в "{wrksp_name}" заходи {board_url}'
                try:
                    bot.send_message(chat_id=student.tg_id, text=message)
                    print(f'TODO отправка в TG {student.tg_id} ссылки {board_url}')
                except:
                    pass
    return HttpResponseRedirect('/admin')
