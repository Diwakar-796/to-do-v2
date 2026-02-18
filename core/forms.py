from django import forms
from core.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'category', 'priority', 'scheduled_time', 'duration', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'}),
        }