from django.contrib import admin
from .models import Users
from .models import Events
# Register your models here.

admin.site.register(Users)
admin.site.register(Events)