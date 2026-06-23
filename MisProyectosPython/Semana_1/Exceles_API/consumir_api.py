# ============================================================
# INSTALAR LIBRERIAS (copia y pega esta linea en la terminal):
#   pip install pandas
#   (urllib y json ya vienen incluidos en Python)
# ============================================================

# consumir_api.py
# Semana 1 - Consumir una API gratuita de internet y mostrar los datos como tabla
# Usamos urllib (viene incluido en Python, no hay que instalar nada) para pedir
# los datos, json para entenderlos y pandas para mostrarlos como tabla.
# Para ejecutar:  python consumir_api.py  (necesitas conexion a internet)
#
# API usada: JSONPlaceholder -> https://jsonplaceholder.typicode.com/users
# Es gratuita, publica y no necesita clave (API key).

import json
import urllib.request
import pandas as pd


# 1) Pedir los datos a la API y convertirlos a una lista de Python
def consultar_api(url):
    with urllib.request.urlopen(url) as respuesta:
        contenido = respuesta.read()           # bytes que devuelve la API
        datos = json.loads(contenido)          # convertir el texto JSON a Python
    return datos


# 2) Quedarnos solo con las columnas que nos interesan
#    (la API trae muchos datos anidados; elegimos algunos)
def preparar_tabla(usuarios):
    filas = []
    for usuario in usuarios:
        filas.append({
            "id": usuario["id"],
            "nombre": usuario["name"],
            "usuario": usuario["username"],
            "email": usuario["email"],
            "ciudad": usuario["address"]["city"],   # dato anidado
            "empresa": usuario["company"]["name"],   # dato anidado
        })
    df = pd.DataFrame(filas)
    return df


# 3) Mostrar la tabla
def mostrar_tabla(df):
    print("\n--- Usuarios obtenidos de la API ---")
    print(df.to_string(index=False))
    print("\nTotal de usuarios:", len(df))


# 4) Funcion principal
def ejecutar():
    url = "https://jsonplaceholder.typicode.com/users"
    print("Consultando:", url)
    try:
        usuarios = consultar_api(url)
        tabla = preparar_tabla(usuarios)
        mostrar_tabla(tabla)
    except urllib.error.URLError:
        print("No se pudo conectar. Revisa tu conexion a internet.")


# Iniciar el programa
ejecutar()
