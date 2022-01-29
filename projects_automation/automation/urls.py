from django.urls import path

from . import views

urlpatterns = [
    path('/upload_users', views.upload_users, name='upload_users'),
    path('/assign_groups/<str:level>', views.assign_groups, name='assign_groups'),
    path('/create_wrksp', views.create_wrksp, name='create_wrksp'),
]
