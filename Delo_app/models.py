from django.db import models
from django.conf import settings

# Create your models here.
class Persons(models.Model):
    UserName = models.CharField(max_length=15)
    Password = models.CharField(max_length=200)
    def __str__(self):
            return self.UserName

class Roadmaps(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    Title = models.CharField(max_length=15)
    Description = models.CharField(max_length=200)
    goald_date = models.DateField()
    def __str__(self):
            return str(f"id: {self.User.id}  пользователь: {self.User}")

