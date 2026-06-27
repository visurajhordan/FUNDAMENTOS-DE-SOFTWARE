# ============================================================
# Quiz 1 — Fundamentos de Programación
# FUNSO - Institución Universitaria CEIPA
# Autor: Jhordan García | 2026
# Descripción: Programa para analizar información de empresas
#              usando Programación Estructurada y POO.
# ============================================================

import os  # Para encontrar el archivo sin importar desde dónde se ejecute


# ============================================================
# CLASE Empresa
# ============================================================

class Empresa:
    """
    Representa una empresa con sus datos básicos:
    nombre, sector, número de empleados e ingresos anuales.
    """

    def __init__(self, nombre, sector, num_empleados, ingresos_anuales):
        """
        Constructor de la clase Empresa.

        Args:
            nombre (str): Nombre de la empresa.
            sector (str): Sector económico al que pertenece.
            num_empleados (str/int): Cantidad de empleados (se convierte a int).
            ingresos_anuales (str/int): Ingresos anuales en pesos (se convierte a int).
        """
        self.nombre = nombre
        self.sector = sector
        self.num_empleados = int(num_empleados)       # Convertir a entero
        self.ingresos_anuales = int(ingresos_anuales) # Convertir a entero

    def obtener_informacion(self):
        """
        Devuelve una cadena con la información legible de la empresa.

        Returns:
            str: Texto con nombre, sector, empleados e ingresos.
        """
        return f"{self.nombre} | {self.sector} | {self.num_empleados} empleados | ${self.ingresos_anuales}"


# ============================================================
# FUNCIONES
# ============================================================

def leer_empresas(nombre_archivo):
    """
    Lee el archivo de texto y construye una lista de objetos Empresa.
    Ignora los registros con num_empleados menor o igual a 0.

    Args:
        nombre_archivo (str): Ruta/nombre del archivo .txt a leer.

    Returns:
        list[Empresa]: Lista de objetos Empresa válidos.
    """
    empresas = []

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()  # Quitar saltos de línea y espacios

                # Ignorar líneas vacías
                if not linea:
                    continue

                # Separar los campos por coma
                partes = linea.split(",")

                # Verificar que la línea tenga exactamente 4 campos
                if len(partes) != 4:
                    continue

                nombre, sector, num_empleados, ingresos_anuales = partes

                # Validar que num_empleados sea un número entero válido
                try:
                    num_empleados_int = int(num_empleados)
                except ValueError:
                    continue  # Si no es un número, ignorar el registro

                # Ignorar empresas con num_empleados <= 0 (registro trampa)
                if num_empleados_int <= 0:
                    continue

                # Crear el objeto Empresa y agregarlo a la lista
                empresa = Empresa(nombre, sector, num_empleados, ingresos_anuales)
                empresas.append(empresa)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")

    return empresas


def calcular_total_ingresos(empresas):
    """
    Suma los ingresos anuales de todas las empresas de la lista.

    Args:
        empresas (list[Empresa]): Lista de objetos Empresa.

    Returns:
        int: Total de ingresos acumulados.
    """
    total = 0
    for empresa in empresas:
        total += empresa.ingresos_anuales
    return total


def filtrar_por_sector(empresas, sector):
    """
    Filtra y devuelve únicamente las empresas que pertenecen al sector indicado.

    Args:
        empresas (list[Empresa]): Lista de objetos Empresa.
        sector (str): Nombre del sector a filtrar (ej: "TECNOLOGIA").

    Returns:
        list[Empresa]: Lista de empresas del sector especificado.
    """
    resultado = []
    for empresa in empresas:
        if empresa.sector == sector:
            resultado.append(empresa)
    return resultado


def empresa_con_mas_empleados(empresas):
    """
    Encuentra y devuelve la empresa con el mayor número de empleados.

    Args:
        empresas (list[Empresa]): Lista de objetos Empresa.

    Returns:
        Empresa | None: Objeto Empresa con más empleados, o None si la lista está vacía.
    """
    if not empresas:
        return None

    mayor = empresas[0]  # Asumir que la primera es la mayor inicialmente
    for empresa in empresas[1:]:
        if empresa.num_empleados > mayor.num_empleados:
            mayor = empresa

    return mayor


def promedio_empleados(empresas):
    """
    Calcula el promedio de empleados entre todas las empresas.
    Evita la división entre cero si la lista está vacía.

    Args:
        empresas (list[Empresa]): Lista de objetos Empresa.

    Returns:
        float: Promedio de empleados, o 0 si la lista está vacía.
    """
    if not empresas:
        return 0

    total_empleados = 0
    for empresa in empresas:
        total_empleados += empresa.num_empleados

    return total_empleados / len(empresas)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    # Buscar empresas.txt en la misma carpeta del .py sin importar desde dónde se corra
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "empresas.txt")

    # Leer las empresas desde el archivo
    empresas = leer_empresas(ruta)

    # --- Mostrar todas las empresas registradas ---
    print("--- Empresas registradas ---")
    for empresa in empresas:
        print(empresa.obtener_informacion())

    # --- Total de ingresos ---
    total = calcular_total_ingresos(empresas)
    print(f"\nTotal de ingresos: {total}")

    # --- Filtrar por sector TECNOLOGIA ---
    print("\n--- Empresas del sector TECNOLOGIA ---")
    tecnologia = filtrar_por_sector(empresas, "TECNOLOGIA")
    for empresa in tecnologia:
        print(empresa.obtener_informacion())

    # --- Empresa con más empleados ---
    mayor = empresa_con_mas_empleados(empresas)
    if mayor:
        print(f"\nEmpresa con mas empleados: {mayor.obtener_informacion()}")

    # --- Promedio de empleados ---
    promedio = promedio_empleados(empresas)
    print(f"\nPromedio de empleados: {promedio:.2f}")
