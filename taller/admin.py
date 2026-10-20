from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Mecanico, Vehiculo, Orden
 
 

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ("codigo", "vehiculo", "descripcion", "mecanico", "estado", "fecha_ingreso")
    list_filter = ("estado", "mecanico")
    readonly_fields = ("codigo",)

 
 
admin.site.register(Mecanico)
admin.site.register(Vehiculo)
