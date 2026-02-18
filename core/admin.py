from django.contrib import admin
from core.models import Task, Category, Feedback

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
class Feedback(admin.ModelAdmin):
    list_display = ['user']