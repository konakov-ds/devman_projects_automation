import datetime

from .models import Student, Group, PM


def group_students_by_level(level):
    students = Student.objects.all()
    return students.filter(level=level)


def get_students_by_time(student_group):
    return student_group.order_by('working_interval_from')


def find_pm_for_group(time_from, time_to):
    managers = PM.objects.all()
    for manager in managers:
        if (manager.working_interval_from <= time_from) \
                and (manager.working_interval_to >= time_to):
            return manager
    return None


def create_new_group(students):
    pm = find_pm_for_group(students[0].working_interval_from, students[0].working_interval_to)
    start_date = datetime.datetime.now()
    start_date = start_date.replace(
        hour=students[0].working_interval_from.hour,
        minute=students[0].working_interval_from.minute,
        second=0
    )
    if pm is None:
        return False
    Group.objects.create(
        pm=pm,
        start_from=start_date
    )
    return True


def assign_group(level):
    students_in_group = 3
    students_by_level = group_students_by_level(level)
    students_by_time = get_students_by_time(students_by_level)
    failed_groups = []
    previous_student = None
    students_group = []
    for student in students_by_time:
        if previous_student is None:
            previous_student = student
            students_group.append(student)
            continue
        if (student.working_interval_from == previous_student.working_interval_from) \
                or (student.working_interval_from < previous_student.working_interval_to):
            students_group.append(student)
            if len(students_group) == students_in_group:
                if create_new_group(students_group):
                    previous_student = None
                    students_group.clear()
                else:
                    failed_groups.append(students_group)
            continue
        failed_groups.append(students_group)
        students_group.clear()
        students_group.append(student)
        previous_student = student
    if len(students_group) > 0:
        failed_groups.append(students_group)
