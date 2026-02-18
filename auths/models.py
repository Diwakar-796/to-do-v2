from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    uid = ShortUUIDField(max_length=20, length=5, prefix='u', alphabet='0123456789', unique=True)
    
    bio = models.TextField(max_length=500)
    phone = models.CharField(null=True, blank=True)
    address = models.CharField(null=True, blank=True)
    country = models.CharField(null=True, blank=True)
    coins_earned = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def img(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    def __str__(self):
        return self.username or self.email or "Unnamed User"
