from django.shortcuts import render, redirect, get_object_or_404
from .models import Mecanico, Vehiculo, Orden
 
 
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
