# conectar_db.py
# La conexion MAS SIMPLE posible a la base de datos con Prisma.
# Solo se conecta, lee las transacciones guardadas y las muestra.
#
# Ejecutar (parado dentro de la carpeta BaseDeDatos):  python conectar_db.py

from prisma import Prisma

# 1) Creamos el cliente y nos conectamos al archivo transacciones.db
db = Prisma()
db.connect()

# 2) Pedimos TODAS las transacciones de la tabla
transacciones = db.transaccion.find_many()

# 3) Las mostramos en pantalla
print(f"\nHay {len(transacciones)} transacciones en la base de datos:\n")
for t in transacciones:
    print(f"  {t.codigo} | {t.tipo} | ${t.monto} -> impacto: {t.impacto}")

# 4) Cerramos la conexion (buena practica)
db.disconnect()
