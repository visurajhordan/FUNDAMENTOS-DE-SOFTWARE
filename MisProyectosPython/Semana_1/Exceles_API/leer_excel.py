# ============================================================
# INSTALAR LIBRERIAS (copia y pega esta linea en la terminal):
#   pip install pandas openpyxl
# ============================================================

# leer_excel.py
# Semana 1 - Lectura de un archivo de Excel y mostrarlo como tabla
# Usamos la libreria pandas (lee Excel) y openpyxl (motor que abre .xlsx)
# Para ejecutar:  python leer_excel.py

import pandas as pd


# 1) Leer el Excel y devolver la tabla (un DataFrame)
def leer_excel(nombre_archivo):
    df = pd.read_excel(nombre_archivo)
    return df


# 2) Mostrar la tabla y algunos datos basicos
def mostrar_tabla(df):
    print("\n--- Tabla completa ---")
    print(df.to_string(index=False))  # to_string deja la tabla alineada

    print("\n--- Informacion ---")
    print("Cantidad de filas:", len(df))
    print("Columnas:", list(df.columns))

    # Si existe la columna Valor, sumamos como ejemplo
    if "Valor" in df.columns:
        print("Valor total:", df["Valor"].sum())


# 3) Funcion principal
def ejecutar():
    archivo = "ventas.xlsx"
    tabla = leer_excel(archivo)
    mostrar_tabla(tabla)


# Iniciar el programa
ejecutar()
