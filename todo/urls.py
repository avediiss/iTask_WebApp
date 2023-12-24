from django.urls import path
from . import views
from .views import HomeView, create_task, update_task, deleteTask, todo_list, todo_list_with_tasks, task_description


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('testing', views.testing, name='testing'),
    path('calendar', views.calendar, name='calendar'),
    path('list/', create_task, name='list'),
    path('update_task/<str:pk>/', update_task, name="update_task"),
    path('list/', todo_list, name='todo_list'),
    path('delete/<str:pk>/', deleteTask, name="delete"),
    path('', todo_list_with_tasks, name = "tasklist"),
    path('task/<int:task_id>/', task_description, name='task_description'),
]

