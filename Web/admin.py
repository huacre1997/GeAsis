from django.contrib import admin
from .models import Usuario,Persona
from ModelTracker.Tracker import TrackerAdmin
class UsuarioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario,UsuarioAdmin)
class PersonaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Persona,TrackerAdmin)