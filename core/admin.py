from django.contrib import admin
from core.models import Task, Category, Feedback, Notification

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_editable = ['is_done']
    list_display = ['title', 'user', 'category', 'priority', 'scheduled_time', 'duration', 'is_done']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_editable = ['is_default']
    list_display = ['title', 'user', 'is_default']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'message']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['user', 'message', 'is_read']