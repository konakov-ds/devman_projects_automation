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
        while counter < 3:
            group = Group.objects.create
