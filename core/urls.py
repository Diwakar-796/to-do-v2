from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),

    path('add-task/', views.add_task, name='add-task'),
    path('done-task/', views.done_task, name='done-task'),
    path('edit-task/<int:id>/', views.edit_task, name='edit-task'),
    path('del-task/<int:id>/', views.del_task, name='del-task'),
    path('task/<int:id>/', views.task_detail, name='task-detail'),
    path('search/', views.search_task, name='search-task'),

    path('add-category/', views.add_category, name='add-category'),

    path('about/', views.about_view, name='about'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark_as_read/<int:id>/', views.mark_notification_read, name='mark_notification_read'),
]
