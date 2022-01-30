from django.contrib import admin
from .models import PM, Group, Student


class PMAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['tg_id', 'name', 'working_interval_from', 'working_interval_to']


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['tg_id', 'name', 'level',
                    'group', 'working_interval_from',
                    'working_interval_to', 'email']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'pm', 'start_from', 'get_group_students', 'board_url']


admin.site.register(PM, PMAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
