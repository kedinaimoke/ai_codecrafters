from django.urls import path
from . import views

app_name = 'codementor_ai'

urlpatterns = [
    path('', views.code_mentor, name='code_mentor'),
]
