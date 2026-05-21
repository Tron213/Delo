from django.db import models

# Create your models here.
class Persons(models.Model):
    UserName = models.CharField(max_length=15)
    Password = models.CharField(max_length=200)
    def __str__(self):
            return self.UserName

class Roadmaps(models.Model):
    artist = models.ForeignKey(Users, on_delete=models.Users)
    Title = models.CharField(max_length=15)
    Description = models.CharField(max_length=200)
    goald_date = models.DateField()
    def __str__(self):
            return self.UserName