from django.contrib import admin
#todoappアプリケーションのmodels.pyを指し、その中で定義したTaskを呼び出している
from todoapp.models import Task

# Register your models here.
admin.site.register(Task)