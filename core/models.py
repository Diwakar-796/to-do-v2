from django.db import models
from auths.models import User
from django.utils import timezone

# Create your models here.

PRIORITY = (
    ('1', 'Low'),
    ('2', 'Medium'),
    ('3', 'High'),
)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY, default='1', null=True, blank=True)
    scheduled_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    coins = models.PositiveIntegerField(default=0, null=True, blank=True)
    duration = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    