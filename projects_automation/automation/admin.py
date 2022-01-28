from django.contrib import admin
from .models import PM, Group, Student


class PMAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['tg_id', 'name', 'working_interval_from', 'working_interval_to']


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['tg_id', 'name', 'level',
                    'group', 'working_interval_from',
                    'working_interval_to']


admin.site.register(PM, PMAdmin)
admin.site.register(Group)
admin.site.register(Student, StudentAdmin)
