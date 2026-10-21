import random
from datetime import date
from django.db import models
from django.utils import timezone
 
# Sin 0/O ni 1/I para que el código no se confunda al leerlo o dictarlo
ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
 
 
def generar_codigo():
    while True:
        codigo = "".join(random.choices(ALFABETO, k=6))
        if not Orden.objects.filter(codigo=codigo).exists():
            return codigo

from django.db import models
 
 
class Mecanico(models.Model):
    nombre = models.CharField(max_length=80)
    especialidad = models.CharField(max_length=80)
 
    class Meta:
        verbose_name = "Mecánico"
        verbose_name_plural = "Mecánicos"
 
    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"
 
 
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name="Año")
    propietario = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
 
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
 
    def __str__(self):
        return f"{self.placa} — {self.marca} {self.modelo}"
 
 
class Orden(models.Model):
    ESTADOS = [
        ("Recibido", "Recibido"),
        ("En reparación", "En reparación"),
        ("Listo", "Listo"),
        ("Entregado", "Entregado"),
    ]
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, related_name="ordenes")
    mecanico = models.ForeignKey(
        Mecanico, on_delete=models.PROTECT, related_name="ordenes")
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Recibido")
    fecha_ingreso = models.DateField(default=date.today)
    codigo = models.CharField(max_length=8, editable=False, verbose_name="Código")  # NUEVO
 
    class Meta:
        verbose_name_plural = "Órdenes"
 
    def save(self, *args, **kwargs):  # NUEVO
        if not self.codigo:  # NUEVO
            self.codigo = generar_codigo()  # NUEVO
        super().save(*args, **kwargs)  # NUEVO
        
    def historial(self):
        return self.eventos.order_by("-hora")
 
    def ultimo_evento(self):
        return self.historial().first()

 
    def __str__(self):
        return f"{self.vehiculo.placa}: {self.descripcion}"

class Punto(models.Model):
    nombre = models.CharField(max_length=60)
 
    class Meta:
        verbose_name = "Punto de control"
        verbose_name_plural = "Puntos de control"
 
    def __str__(self):
        return self.nombre
 
 
class Evento(models.Model):
    orden = models.ForeignKey(
        Orden, on_delete=models.CASCADE, related_name="eventos")
    punto = models.ForeignKey(
        Punto, on_delete=models.PROTECT, related_name="eventos")
    hora = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return f"{self.orden.codigo} en {self.punto.nombre}"

