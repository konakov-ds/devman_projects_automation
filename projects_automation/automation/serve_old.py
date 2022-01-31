import telegram
from environs import Env
from telegram import KeyboardButton, ReplyKeyboardMarkup
from .models import Student, Group


env = Env()
env.read_env()

tg_token = env('TELEGRAM_TOKEN')

STUDENT_UPDATE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подтвердить новое время'),
        ],
[
            KeyboardButton(text='Не смогу участвовать в проекте'),
        ],
    ],
    resize_keyboard=True
)


def group_students_by_level(level):
    students = Student.objects.all()
    if level == 'junior':
        return students.filter(level='junior')
    return students.exclude(level='junior')


def sort_by_time(student_group):
    return student_group.order_by('-working_interval_to').order_by('working_interval_from')


def assign_pm_for_group(group, managers):
    max_manager_groups = 3
    group_time_from, group_time_to = get_group_work_interval(group)
    for manager in managers:
        manager_groups = Group.objects.filter(pm_id=manager.id)
        if (float(str(manager.working_interval_from)[:-3].replace(':', '.')) <= group_time_from) \
                and (float(str(manager.working_interval_to)[:-3].replace(':', '.')) >= group_time_to) \
                and len(manager_groups) < max_manager_groups:
            group.pm = manager
            group.save()
            return True
    return False


def assign_group(level):
    students = group_students_by_level(level)
    students = sort_by_time(students)
    counter = 0
    for student in students:
        if counter == 0:
            group = Group.objects.create()
            student.group = group
            first_in_group = student
        elif student.working_interval_from < first_in_group.working_interval_to and counter < 3:
            student.group = group
        else:
            group = Group.objects.create()
            student.group = group
            first_in_group = student
            counter = 0
        student.save()
        counter += 1
        if counter > 2:
            counter = 0


def get_incomplete_groups():
    incomplete_groups = []
    groups = Group.objects.all()
    for group in groups:
        if len(group.students.all()) < 3:
            incomplete_groups.append(group)
    return incomplete_groups


def get_group_work_interval(group):
    time_from = max(
        [student.working_interval_from for student in group.students.all()]
    )
    time_to = min(
        [student.working_interval_to for student in group.students.all()]
    )
    time_from = float(str(time_from)[:-3].replace(':', '.'))
    time_to = float(str(time_to)[:-3].replace(':', '.'))
    return time_from, time_to


def get_min_time_distance(student, group):
    student_time_from = float(
        str(student.working_interval_from)[:-3].replace(':', '.')
    )
    student_time_to = float(
        str(student.working_interval_to)[:-3].replace(':', '.')
    )
    group_time_from, group_time_to = get_group_work_interval(group)

    min_dist = min(
        abs(student_time_from - group_time_from), abs(student_time_to - group_time_to)
    )
    return min_dist


def candidates_for_telegram_push():
    incomplete_groups = get_incomplete_groups()
    groups_with_one = [
        group for group in incomplete_groups if len(group.students.all()) < 2
    ]
    if len(groups_with_one) < 1:
        return None
    groups_with_two = [
        group for group in incomplete_groups if len(group.students.all()) == 2
    ]
    if len(groups_with_two) < 1:
        return None
    single_students = [
        group.students.all().first() for group in groups_with_one
    ]
    group_for_single = []
    for student in single_students[:len(groups_with_two)]:
        selected_group = groups_with_two[0]
        distance = get_min_time_distance(student, selected_group)
        for group in groups_with_two[1:]:
            if get_min_time_distance(student, group) < distance:
                selected_group = group
        group_for_single.append((student, selected_group))

    return group_for_single, single_students[len(groups_with_two):]


def send_message_to_student(user_id, time_from, time_to):
    bot = telegram.Bot(token=tg_token)
    bot.send_message(
        chat_id=user_id,
        text='Привет девманец!\nК сожалению, выбранное тобой время созвона'
             ' не согласуется с остальными участниками. Мы можем предложить группу'
             f' со следующим интервалом {time_from} - {time_to}',
        reply_markup=STUDENT_UPDATE_KEYBOARD,
    )


def send_new_time_for_singles(group_for_single):
    if not group_for_single:
        pass
    for item in group_for_single:
        student, group = item
        group_time_from, group_time_to = get_group_work_interval(group)
        send_message_to_student(
            student.tg_id,
            str(group_time_from).replace('.', ':') + '0',
            str(group_time_to).replace('.', ':') + '0',
        )
        student.group = group
        student.save()
