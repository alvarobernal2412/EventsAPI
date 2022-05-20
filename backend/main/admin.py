from django.contrib import admin
from main.models import Event, Calendar, GlobalEvent

# Archivo para gestionar el panel de administración

admin.site.register(Event)
admin.site.register(Calendar)
admin.site.register(GlobalEvent)
