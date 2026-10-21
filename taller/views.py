import io
 
import segno
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse





from .models import Mecanico, Vehiculo, Orden, Punto, Evento
 
 
def ordenes(request):
    mecanico_id = request.GET.get("mecanico")
    lista = Orden.objects.exclude(estado="Entregado").order_by("fecha_ingreso")
    if mecanico_id:
        lista = lista.filter(mecanico_id=mecanico_id)
    contexto = {"ordenes": lista, "mecanicos": Mecanico.objects.all()}
    return render(request, "taller/ordenes.html", contexto)
 
 
def ficha(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    historial = vehiculo.ordenes.order_by("-fecha_ingreso")
    contexto = {"vehiculo": vehiculo, "historial": historial}
    return render(request, "taller/ficha.html", contexto)

def seguimiento_buscar(request):
    codigo = request.GET.get("codigo", "").strip().upper()
    if codigo:
        return redirect("seguimiento", codigo=codigo)
    return render(request, "taller/seguimiento_buscar.html")
 
 
def seguimiento(request, codigo):
    orden = Orden.objects.filter(codigo=codigo.upper()).first()
    contexto = {"orden": orden, "codigo": codigo.upper()}
    estado = 200 if orden else 404
    return render(request, "taller/seguimiento.html", contexto, status=estado)

def escanear(request, codigo):
    orden = Orden.objects.filter(codigo=codigo.upper()).first()
    if orden is None:
        return render(request, "taller/escanear.html",
                      {"codigo": codigo.upper()}, status=404)
    if request.method == "POST":
        punto = Punto.objects.filter(pk=request.POST.get("punto")).first()
        if punto:
            Evento.objects.create(orden=orden, punto=punto)
        return redirect("escanear", codigo=orden.codigo)
    contexto = {"orden": orden, "codigo": orden.codigo,
                "puntos": Punto.objects.all()}
    return render(request, "taller/escanear.html", contexto)

def tablero(request):
    lista = Orden.objects.exclude(estado="Entregado").order_by("fecha_ingreso")
    return render(request, "taller/tablero.html", {"ordenes": lista})

def qr(request, codigo):
    direccion = request.build_absolute_uri(reverse("escanear", args=[codigo]))
    imagen = segno.make(direccion)
    salida = io.BytesIO()
    imagen.save(salida, kind="svg", scale=6)
    return HttpResponse(salida.getvalue(), content_type="image/svg+xml")
 
 
def etiqueta(request, codigo):
    orden = get_object_or_404(Orden, codigo=codigo.upper())
    return render(request, "taller/etiqueta.html", {"orden": orden})

