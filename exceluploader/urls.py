from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_file', views.uploadFile, name='uploadFile')
]