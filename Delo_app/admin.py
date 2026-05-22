from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Persons)
admin.site.register(Roadmaps)
admin.site.register(Stages)
admin.site.register(Tasks)