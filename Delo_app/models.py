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
    Title = models.CharField(max_length=35)
    Description = models.CharField(max_length=200, null=True)
    goald_date = models.DateField(null=True)
    Badge=models.CharField(null=True,max_length=310)
    class Meta:
        ordering =['User','-id']
    def __str__(self):
            return str(f"{self.Title}  id: {self.User.id}  пользователь: {self.User}")


class Stages(models.Model):
    Roadmap = models.ForeignKey(Roadmaps, 
        on_delete=models.CASCADE)
    Stagetitle = models.CharField(max_length=130)
    goald_date = models.DateField(null=True)
    status = models.CharField(null=True, max_length=35)
    progres = models.IntegerField(null=True, max_length=35)

    class Meta:
        ordering =['Roadmap', 'id']
    def __str__(self):
        return str(f"{self.Stagetitle}рОАДМАПА № {self.Roadmap.id} ")

class Tasks(models.Model):
    Stage = models.ForeignKey(Stages, on_delete=models.CASCADE)
    Tasktitle = models.CharField(max_length=35)
    status = models.CharField(null=True, max_length=35)
    class Meta:
        ordering =['Stage', 'id']
    def __str__(self):
        return str(f"рОАДМАПА № {self.Tasktitle} ")

class Steps(models.Model):
    Task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    Steptitle = models.CharField(max_length=35)
    status = models.CharField(null=True, max_length=35)
    class Meta:
        ordering =['Task', 'id']
    def __str__(self):
        return str(f"рОАДМАПА № {self.Steptitle} ")