# transaccion_poo_v1.py
# Actividad 2 - Refactorizacion a Programacion Orientada a Objetos (POO)
# Tomamos las funciones de PE de procesador_ventas.py y las convertimos en una Clase.
#
# NOTA: en Canvas la clase se llama Transaccion (atributos ID, Tipo, Monto).
#       Aqui, por continuidad con la Semana 1, la modelamos como Venta:
#           ID  -> producto_id    Tipo -> categoria    Monto -> valor
#       El concepto es exactamente el mismo.
#
# Para ejecutar:  python transaccion_poo_v1.py


# 1) La CLASE: una plantilla que une los DATOS y la LOGICA de una sola venta
class Venta:
    """Representa UNA venta: encapsula sus datos y su comportamiento."""

    # El CONSTRUCTOR se ejecuta al crear el objeto y guarda sus datos.
    # 'self' es el propio objeto que se esta construyendo.
    def __init__(self, producto_id, categoria, valor):
        self.producto_id = producto_id     # atributo (antes: clave del diccionario)
        self.categoria = categoria         # atributo
        self.valor = int(valor)           # atributo (lo convertimos a numero aqui)

    # 2) METODO: cada objeto sabe mostrar su propia informacion
    def obtener_informacion(self):
        """Devuelve los datos de la venta como un texto legible."""
        return f"{self.producto_id} | {self.categoria} | ${self.valor}"



# 3) Leer el archivo y crear una LISTA DE OBJETOS (ya no de diccionarios)
def leer_y_almacenar_datos(nombre_archivo):
    """Lee cada linea del archivo y crea un objeto Venta por cada una."""
    ventas = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            producto_id, categoria, valor = linea.strip().split(",")
            venta = Venta(producto_id, categoria, valor)  # se crea un OBJETO
            ventas.append(venta)                          # se almacena el OBJETO
    return ventas


# 4) Funciones de gestion sobre la lista de objetos
def calcular_valor_total(ventas):
    """Suma el valor de todos los objetos Venta."""
    total = 0
    for venta in ventas:
        total = total + venta.valor   # accedemos al atributo del objeto
    return total


def filtrar_por_categoria(ventas, categoria):
    """Devuelve solo los objetos cuya categoria coincide."""
    return [venta for venta in ventas if venta.categoria == categoria]


# 5) Funcion principal
def ejecutar_sistema():
    ventas = leer_y_almacenar_datos("ventas.txt")

    print("--- Todas las ventas ---")
    for venta in ventas:
        print(venta.obtener_informacion())   # el objeto se muestra a si mismo

    print("\nValor total de las ventas:", calcular_valor_total(ventas))

    print("\n--- Solo ELECTRONICA ---")
    for venta in filtrar_por_categoria(ventas, "ELECTRONICA"):
        print(venta.obtener_informacion())


# Iniciar el programa
ejecutar_sistema()
