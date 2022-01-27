import json

from pathlib import Path

from django.http import HttpResponseRedirect

from .models import PM, Student


FILES_PATH = Path(__file__).resolve().parent / 'files/'


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
                name=student['name'],
                level=student['level'],
                working_interval_from=student['working_interval_from'],
                working_interval_to=student['working_interval_to']
            )
    return HttpResponseRedirect('/admin')
