# verificar_insercion.py
# Semana 7 - Paso 8 de la actividad 7-1: realizar una insercion para verificar
# que la base de datos funcione y que la restriccion UNIQUE del email se respete.
# Requiere haber ejecutado antes:  python configurar_db.py
# Ejecutar:  python verificar_insercion.py
#
# NOTA: ejecutalo DOS VECES.
#   1ra vez -> "Usuario insertado correctamente."
#   2da vez -> "El usuario ya existe (el email es UNICO)."
#              porque el email ya esta registrado y SQLite lanza IntegrityError.

import sqlite3

# Prueba rapida de insercion
conexion = sqlite3.connect("quantum_wallet.db")
cursor = conexion.cursor()

try:
    cursor.execute(
        "INSERT INTO usuarios (nombre, email) VALUES (?, ?);",
        ("Juan Perez", "juan@mail.com"),
    )
    conexion.commit()
    print("Usuario insertado correctamente.")
except sqlite3.IntegrityError:
    print("El usuario ya existe (el email es UNICO).")

conexion.close()
