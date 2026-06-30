# Semana 3 — De un `.txt` a una Base de Datos real (Prisma + SQLite)

Hasta ahora nuestras transacciones vivían en un archivo de texto (`transacciones.txt`).
**Subimos de nivel:** las vamos a guardar en una **base de datos SQLite** usando **Prisma**,
reutilizando **las mismas clases POO** de [`diseno_pilares_poo.py`](../diseno_pilares_poo.py).
Al final veremos los datos en un visor gráfico.

---

## ⚠️ Concepto clave

**SQLite NO es un servidor** como MySQL o PostgreSQL. Es una base de datos que vive en
**un solo archivo** (`transacciones.db`). No hay que "prender" ningún motor ni usar Docker:
el archivo *es* la base de datos, y Prisma se conecta **directamente a ese archivo**.

---

## Programa para ver la base de datos

👉 **DB Browser for SQLite** — gratis y en español: <https://sqlitebrowser.org/dl/>

Para usarlo: ábrelo → **Abrir base de datos** → elige `transacciones.db` → pestaña
**Examinar datos** (*Browse Data*) → tabla `Transaccion`.

---

## Requisitos

1. **Python 3** — <https://www.python.org/downloads/>
2. **Instalar Prisma** (parado dentro de la carpeta `BaseDeDatos`):

   ```powershell
   cd "MisProyectosPython\Semana_3\BaseDeDatos"
   pip install -r requirements.txt
   ```

   > No necesitas instalar Node.js: `pip install prisma` ya trae el comando `prisma`.
   >
   > 🛟 ¿Te salió un error de **permisos** (`Failed to write executable`) o luego `prisma` **no se reconoce**?
   > Es un detalle de cómo está instalado tu Python. Lee la sección **Problemas comunes** al final.

> 💡 Ejecuta TODOS los comandos parado **dentro de la carpeta `BaseDeDatos`**.

---

## Paso 1 — Mira el plano de la base de datos (`schema.prisma`)

[`schema.prisma`](./schema.prisma) define **a qué** base te conectas y **qué forma** tiene la tabla:

```prisma
datasource db {
  provider = "sqlite"
  url      = "file:./transacciones.db"   // la base = un archivo
}

model Transaccion {
  id      Int    @id @default(autoincrement())
  codigo  String @unique   // T001, T002...
  tipo    String           // CREDITO / DEBITO
  monto   Int
  impacto Float            // resultado de calcular_impacto()
}
```

---

## Paso 2 — Crea la base de datos

Este comando lee el `schema.prisma`, **crea el archivo `transacciones.db`** con la tabla y
prepara el cliente de Prisma para Python:

```powershell
prisma db push
```

Al terminar verás: *"Your database is now in sync with your schema"*. ✅

---

## Paso 3 — Migra el `.txt` a la base de datos

[`migrar_transacciones.py`](./migrar_transacciones.py) reutiliza **las mismas clases POO**
de la Semana 3 y, en vez de imprimir el impacto, lo **guarda** en la base:

```powershell
python migrar_transacciones.py
```

Salida esperada:

```
  [Aviso] Se ignoro T005: El monto no puede ser negativo.

--- Guardando transacciones en la base de datos ---
  Guardado T001 | CREDITO | $500000 -> impacto: 10000.0
  Guardado T002 | DEBITO | $80000 -> impacto: 1500.0
  Guardado T003 | CREDITO | $1200000 -> impacto: 24000.0
  Guardado T004 | DEBITO | $45000 -> impacto: 1500.0

Listo. La base de datos ahora tiene 4 transacciones.
```

> 🔎 ¿Por qué solo 4 y no 5? Porque `T005` tiene monto negativo: el **encapsulamiento**
> (el *setter* que valida) lo rechaza, igual que en la Semana 3. Un dato malo no entra. 💪

---

## Paso 4 — Lee la base de datos desde Python

[`conectar_db.py`](./conectar_db.py) es la conexión **más simple posible**: se conecta, lee y muestra.

```powershell
python conectar_db.py
```

---

## Paso 5 — Velo en el visor gráfico

Abre **DB Browser for SQLite** → **Abrir base de datos** → `transacciones.db` →
pestaña **Examinar datos** → tabla `Transaccion`. 🎉 Ahí están tus 4 registros.

---

## Resumen rápido (copiar y pegar)

```powershell
cd "MisProyectosPython\Semana_3\BaseDeDatos"
pip install -r requirements.txt
prisma db push                  # crea transacciones.db
python migrar_transacciones.py  # txt -> base de datos (usando las clases POO)
python conectar_db.py           # leer y mostrar
```

> ✅ Flujo **probado de principio a fin** en Windows con Python 3.12.

---

## Archivos de esta carpeta

| Archivo | Para qué sirve |
|---------|----------------|
| [`schema.prisma`](./schema.prisma) | Define la conexión y la forma de la tabla `Transaccion`. |
| [`migrar_transacciones.py`](./migrar_transacciones.py) | Lee `../transacciones.txt` con las **clases POO** y lo guarda en la base. |
| [`conectar_db.py`](./conectar_db.py) | Conexión más simple posible: lee y muestra lo guardado. |
| [`requirements.txt`](./requirements.txt) | Única dependencia: `prisma`. |

---

## Problemas comunes

- **`No such table: Transaccion`:** te saltaste el **Paso 2** (`prisma db push`).

- **`pip install` falla con `Failed to write executable` (permisos):** tu Python está instalado
  "para todo el sistema" y `pip` no puede escribir ahí sin administrador. Instala **a tu usuario**:

  ```powershell
  pip install --user -r requirements.txt
  ```

- **Después de instalar, `prisma` no se reconoce / `spawn prisma-client-py ENOENT`:** el comando
  `prisma` quedó en una carpeta que no está en el **PATH**. Encuéntrala con:

  ```powershell
  python -c "import site, os; print(os.path.join(os.path.dirname(site.getusersitepackages()), 'Scripts'))"
  ```

  Copia esa ruta y agrégala al PATH de tu usuario (busca en Windows *"Editar las variables de
  entorno de tu cuenta"* → variable **Path** → **Nuevo** → pega la ruta → Aceptar). **Cierra y
  vuelve a abrir** la terminal y listo.

- **Quiero empezar desde cero:** borra la base con `Remove-Item transacciones.db` y repite desde el Paso 2.

---

## El hilo pedagógico (el "siguiente nivel")

`transacciones.txt` → **mismas clases POO** (Encapsulamiento / Herencia / Polimorfismo) →
**Prisma** las guarda en una **base de datos** → la ves en **DB Browser for SQLite**.
El dato malo (`T005`) sigue siendo rechazado: el blindaje de POO ahora protege también lo que
entra a la base de datos.
