from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Mecanico, Vehiculo, Orden, Punto, Evento
 
 

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ("codigo", "vehiculo", "descripcion", "mecanico", "estado", "fecha_ingreso")
    list_filter = ("estado", "mecanico")
    readonly_fields = ("codigo",)

 
 
admin.site.register(Mecanico)
admin.site.register(Vehiculo)

admin.site.register(Punto)
 
 
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("orden", "punto", "hora")
    list_filter = ("punto",)
