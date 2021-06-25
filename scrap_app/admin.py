from django.contrib import admin
from .models import User,Project, Holidays

admin.site.register(Project)

admin.site.register(Holidays)