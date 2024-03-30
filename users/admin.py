from django.contrib import admin
from .models import User

models_list = [User]
admin.site.register(models_list)