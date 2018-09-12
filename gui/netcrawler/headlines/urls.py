from django.urls import path

from . import views

app_name = 'headlines'
urlpatterns = [
    path('index', views.index, name='index'),
    path('overview', views.overview, name='overview')
]
