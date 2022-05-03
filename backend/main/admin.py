from django.contrib import admin
from main.models import Event, Day, Calendar

# Archivo para gestionar el panel de administración

admin.site.register(Event)
admin.site.register(Day)
admin.site.register(Calendar)

