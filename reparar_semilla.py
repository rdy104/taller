ruta = "taller/fixtures/semilla.json"
datos = open(ruta, "rb").read()
try:
    texto = datos.decode("utf-8")
except UnicodeDecodeError:
    texto = datos.decode("utf-16" if datos[:2] in (b"\xff\xfe", b"\xfe\xff") else "cp1252")
open(ruta, "w", encoding="utf-8").write(texto)
print("Listo, semilla en UTF-8")