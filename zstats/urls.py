from django.urls import path

from . import views

app_name = 'zstats'

urlpatterns = [
    path('', views.index, name='index'),
]
