import json
import os

from pathlib import Path

from django.http import HttpResponseRedirect, HttpResponse

from dotenv import load_dotenv

from .models import PM, Student, Group

from .serve_old import assign_group

from trello.trello import create_workspace, create_board, add_members_board

FILES_PATH = Path(__file__).resolve().parent / 'files/'

load_dotenv('./trello/.env')
trello_apikey = os.getenv('TRELLO_API_KEY')
trello_token = os.getenv('TRELLO_TOKEN')


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
    return HttpResponse('Groups created.')


def create_wrksp(request):
    if request.method == 'POST' and trello_apikey:
        wrksp_name = request.POST.get('project', 'Проект Новый [01.12.2022-07.12.2022]')

        wrksp_id = create_workspace(trello_apikey, trello_token, wrksp_name)

        groups = Group.objects.filter(
            pm__isnull=False,
            start_from__isnull=False,
            students__isnull=False
            ).distinct()
        for group in groups:
            board_name = (
                f'{group.start_from.strftime("%H:%M")} '
                f'{", ".join([str(student.name) for student in group.students.all()])}'
            )

            board_id, board_url = create_board(trello_apikey, trello_token, wrksp_id, board_name, group.pm.board_bg)

            for student in group.students.all():
                add_members_board(trello_apikey, trello_token, board_id, student.email)
            
    return HttpResponseRedirect('/admin')
