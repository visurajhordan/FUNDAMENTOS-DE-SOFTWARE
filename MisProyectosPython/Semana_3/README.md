# Semana 3 — Pilares y Diseño de POO

Esta semana hacemos el código **robusto y profesional**: blindamos los datos
(Encapsulamiento), lo hacemos reutilizable (Herencia), flexible (Polimorfismo) y lo
alineamos con los principios de diseño **SOLID** (SRP y OCP).

## Archivos

| Archivo | Para qué sirve |
|---------|----------------|
| [`diseno_pilares_poo.py`](./diseno_pilares_poo.py) | **Actividad 1.** Refactor de la clase de la Semana 2 aplicando Encapsulamiento, Herencia y Polimorfismo. |
| [`transacciones.txt`](./transacciones.txt) | Registros de ejemplo (`ID,TIPO,MONTO`). Incluye uno inválido para probar el manejo de errores. |
| [`codigo_fragil_srp.py`](./codigo_fragil_srp.py) | **Actividad 2.** Código de ejemplo para **analizar** (no se corrige en código, solo en el informe). |

## Actividad 1 — Encapsulamiento, Herencia y Polimorfismo

- **Encapsulamiento:** el atributo `monto` es privado (`self._monto`) y se accede mediante un
  *getter* (`@property`) y un *setter* (`@monto.setter`) que **valida** que nunca sea negativo.
- **Herencia:** `TransaccionBase` (padre) reúne la lógica común; `TransaccionCredito` y
  `TransaccionDebito` (hijas) la heredan.
- **Polimorfismo:** `calcular_impacto()` se sobreescribe en cada hija (interés vs. comisión).
- **Robustez:** `leer_transacciones()` usa `try/except` para que un registro inválido (el monto
  negativo de `T005`) **no detenga** el programa.

> **Nota de continuidad:** en la Semana 2 nuestro ejemplo fue la clase `Venta`; aquí seguimos
> el enunciado modelando `Transaccion` (con `monto` y `tipo`) porque se presta naturalmente a la
> jerarquía Crédito/Débito. El concepto es el mismo.

## Actividad 2 — Análisis SOLID

Abre `codigo_fragil_srp.py` y analiza el método `procesar_y_validar_y_reportar()`:

- **Paso A (SRP):** identifica las **tres responsabilidades** mezcladas (validación, lógica de
  negocio y reporte) y propón tres clases para separarlas (p. ej. `ValidadorDatos`,
  `MotorLogica`, `GeneradorReporte`). *Solo nombrarlas y justificar, sin programarlas.*
- **Paso B (OCP):** explica por qué cambiar el formato del reporte (a XML/JSON) modificando esta
  clase viola el OCP, y cómo una jerarquía `ReporteBase → ReporteXML, ReporteJSON` (Herencia +
  Polimorfismo) lo resuelve. *Solo explicar el diseño, sin programarlo.*

## Cómo ejecutar

```bash
python diseno_pilares_poo.py     # Actividad 1 (refactor con los pilares)
python codigo_fragil_srp.py      # Actividad 2 (código a analizar)
```
