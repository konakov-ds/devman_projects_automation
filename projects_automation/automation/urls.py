from django.urls import path

from . import views

urlpatterns = [
    path('/upload_users', views.upload_users, name='upload_users'),
]
