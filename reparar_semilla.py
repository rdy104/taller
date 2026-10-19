from pathlib import Path

ruta = Path("taller/fixtures/semilla.json")
datos = ruta.read_bytes()
try:
    texto = datos.decode("utf-8")
except UnicodeDecodeError:
    if datos[:2] in (b"\xff\xfe", b"\xfe\xff"):
        texto = datos.decode("utf-16")
    else:
        texto = datos.decode("cp1252")
ruta.write_text(texto, encoding="utf-8")
print("semilla.json convertido a UTF-8")