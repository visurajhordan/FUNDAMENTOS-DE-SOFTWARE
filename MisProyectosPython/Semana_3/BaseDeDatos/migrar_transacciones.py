# migrar_transacciones.py
# Lleva las transacciones de ../transacciones.txt hacia la base de datos SQLite usando Prisma.
#
# La idea clave (pasar al siguiente nivel):
#   Reutilizamos EXACTAMENTE las mismas clases POO de diseno_pilares_poo.py
#   (Encapsulamiento, Herencia, Polimorfismo). La unica diferencia es que ahora,
#   en vez de IMPRIMIR el impacto en pantalla, lo GUARDAMOS en la base de datos.
#
# Ejecutar (parado dentro de la carpeta BaseDeDatos):  python migrar_transacciones.py

import os
import sys

# --- Permitir importar el archivo de la Semana 3 (esta una carpeta mas arriba) ---
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CARPETA_SEMANA3 = os.path.join(CARPETA_ACTUAL, "..")
sys.path.append(CARPETA_SEMANA3)

from diseno_pilares_poo import leer_transacciones   # <- MISMAS clases POO
from prisma import Prisma


def tipo_legible(transaccion):
    """TransaccionCredito -> 'CREDITO'   |   TransaccionDebito -> 'DEBITO'."""
    return type(transaccion).__name__.replace("Transaccion", "").upper()


def migrar():
    # 1) Leemos el .txt usando la MISMA funcion de la Semana 3.
    #    Los registros invalidos (como T005 con monto negativo) se ignoran solos.
    ruta_txt = os.path.join(CARPETA_SEMANA3, "transacciones.txt")
    transacciones = leer_transacciones(ruta_txt)

    # 2) Nos conectamos a la base de datos.
    db = Prisma()
    db.connect()

    # 3) Empezamos limpio para poder correr este script las veces que queramos.
    db.transaccion.delete_many()

    print("\n--- Guardando transacciones en la base de datos ---")
    for t in transacciones:
        registro = db.transaccion.create(
            data={
                "codigo": t.id_transaccion,
                "tipo": tipo_legible(t),
                "monto": t.monto,              # encapsulado y validado en la clase
                "impacto": t.calcular_impacto(),  # POLIMORFISMO: cada tipo calcula distinto
            }
        )
        print(f"  Guardado {registro.codigo} | {registro.tipo} | ${registro.monto} -> impacto: {registro.impacto}")

    total = db.transaccion.count()
    print(f"\nListo. La base de datos ahora tiene {total} transacciones.")
    db.disconnect()


if __name__ == "__main__":
    migrar()
