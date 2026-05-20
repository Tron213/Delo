from django.db import models

# Create your models here.
class Persons(models.Model):
    UserName = models.CharField(max_length=15)
    Password = models.CharField(max_length=200)
    def __str__(self):
            return self.UserName