from django.urls import path

from . import views

app_name = 'zinfos'

urlpatterns = [
    path('', views.index, name='index'),
]
