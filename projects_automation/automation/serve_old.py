from .models import Student, Group


def group_students_by_level(level):
    students = Student.objects.all()
    if level == 'junior':
        return students.filter(level='junior')
    return students.exclude(level='junior')


def sort_by_time(student_group):
    return student_group.order_by('-working_interval_to').order_by('working_interval_from')


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
    for student in single_students:
        selected_group =  groups_with_two[0]
        distance = get_min_time_distance(student, selected_group)
        for group in groups_with_two[1:]:
            if get_min_time_distance(student, group) < distance:
                selected_group = group
        group_for_single.append((student, selected_group))

    return group_for_single
