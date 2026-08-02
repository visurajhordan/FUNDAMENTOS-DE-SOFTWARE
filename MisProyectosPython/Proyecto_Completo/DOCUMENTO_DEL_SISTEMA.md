# Documento del Sistema — Quantum Core

**Asignatura:** Fundamentos de Software
**Autores:** Jhordan Garcia · Emmanuel Ospina
**Repositorio:** <https://github.com/visurajhordan/FUNDAMENTOS-DE-SOFTWARE>
**Módulo:** `MisProyectosPython/Proyecto_Completo/`

---

## 1. Descripción del sistema

**Quantum Core** es una aplicación web full-stack para la gestión de transacciones financieras.
Permite registrar, consultar, modificar y eliminar transacciones desde el navegador, con
persistencia real en una base de datos relacional.

El sistema resuelve un problema concreto: en las primeras semanas del curso las transacciones se
leían desde un archivo de texto plano (`transacciones.txt`) y vivían únicamente en memoria — al
cerrar el programa, todo se perdía. Quantum Core convierte ese ejercicio en un sistema real, con
una interfaz de usuario, una API documentada y una base de datos que conserva la información.

### Funcionalidades

| Operación | Descripción |
|---|---|
| **Crear** | Registra una transacción con código, tipo, monto e impacto |
| **Consultar** | Lista todas las transacciones o consulta una por su identificador |
| **Actualizar** | Modifica los datos de una transacción existente |
| **Eliminar** | Borra una transacción del sistema |
| **Validar** | Rechaza montos negativos y códigos duplicados con un mensaje claro |

---

## 2. Arquitectura

El sistema está construido sobre una **arquitectura de tres capas en procesos independientes**.
No es un monolito: cada capa se ejecuta por separado, en su propio puerto, y puede reiniciarse
sin afectar a las demás.

```
┌──────────────────────┐   HTTP/JSON   ┌──────────────────────┐   Prisma   ┌──────────────────┐
│  CAPA DE PRESENTACIÓN │ ────────────► │  CAPA DE APLICACIÓN   │ ─────────► │  CAPA DE DATOS    │
│                       │               │                       │            │                   │
│  React + Vite         │ ◄──────────── │  Flask (Python)       │ ◄───────── │  MySQL 8          │
│  Tailwind CSS         │    fetch()    │  routes → controllers │            │  contenedor       │
│  puerto 5173          │               │        → models       │            │  Docker "empresa" │
│                       │               │  puerto 5000          │            │  puerto 3306      │
└──────────────────────┘               └──────────────────────┘            └──────────────────┘
```

### 2.1 Capa de presentación (FRONTEND)

Aplicación React que se ejecuta en el navegador. **Nunca se comunica con la base de datos**: su
única entrada al sistema es la API REST, a través de `fetch()`.

| Archivo | Responsabilidad |
|---|---|
| `src/pages/Transacciones.jsx` | Interfaz completa: tabla, formulario, edición y borrado |
| `src/api/transacciones.js` | Encapsula las cuatro llamadas HTTP al backend |
| `src/App.jsx`, `src/main.jsx` | Montaje de la aplicación |

### 2.2 Capa de aplicación (BACKEND)

Servidor Flask organizado en tres subcapas, cada una con **una sola responsabilidad** (principio
SRP de SOLID). Una petición atraviesa las tres en orden:

| Subcapa | Archivo | Responsabilidad única |
|---|---|---|
| **Rutas** | `routes/transaccion_routes.py` | Definir las URL y el método HTTP. No contiene lógica de negocio. |
| **Controladores** | `controllers/transaccion_controller.py` | Validar los datos, atrapar errores y decidir el código de respuesta HTTP. |
| **Modelos** | `models/transaccion_model.py` | Única capa que habla con la base de datos, a través de Prisma. |

`app.py` es el punto de arranque: crea la aplicación Flask, habilita **CORS** (necesario porque el
frontend corre en otro puerto), conecta la base de datos y registra las rutas bajo el prefijo
`/api/transacciones`.

**Ventaja de esta separación:** si mañana se cambia MySQL por PostgreSQL, solo se modifica
`models/`. Si se cambia React por una aplicación móvil, el backend no se entera.

### 2.3 Capa de datos

Servidor **MySQL 8** ejecutándose dentro de un contenedor Docker llamado `empresa`. Los datos se
guardan en un volumen (`mysql_datos`), por lo que **sobreviven aunque el contenedor se elimine**.

El acceso se hace mediante **Prisma ORM**, que traduce las operaciones de Python a SQL.

---

## 3. Modelo de datos

Definido en `BACKEND/schema.prisma`:

```prisma
model Transaccion {
  id      Int    @id @default(autoincrement())
  codigo  String @unique
  tipo    String
  monto   Int
  impacto Float
}
```

| Campo | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | Int | **PK**, autoincremental | Identificador único |
| `codigo` | String | **UNIQUE** | Código de la transacción (T001, T002…) |
| `tipo` | String | — | CREDITO, DEBITO o TRANSFERENCIA |
| `monto` | Int | Validado ≥ 0 | Valor de la transacción |
| `impacto` | Float | — | Impacto financiero calculado |

La restricción `@unique` sobre `codigo` es la que impide registrar dos transacciones con el mismo
código: la base de datos misma rechaza el duplicado.

---

## 4. Contrato de la API (endpoints)

Base: `http://localhost:5000/api/transacciones`

| Método | Ruta | Acción | Respuesta exitosa |
|---|---|---|---|
| `GET` | `/` | Lista todas las transacciones | `200` + arreglo JSON |
| `GET` | `/<id>` | Obtiene una transacción | `200` + objeto JSON |
| `POST` | `/` | Crea una transacción | `201` + objeto creado |
| `PUT` | `/<id>` | Actualiza una transacción | `200` + objeto actualizado |
| `DELETE` | `/<id>` | Elimina una transacción | `200` + mensaje |

### Manejo de errores

Toda función del controlador está envuelta en `try/except`: ante un dato inválido el servidor
responde con un código de error y un mensaje, **sin caerse**.

| Situación | Código | Respuesta |
|---|---|---|
| Monto negativo | `400` | `{"error": "El monto no puede ser negativo"}` |
| Código duplicado | `400` | `{"error": "..."}` (restricción UNIQUE) |
| Transacción inexistente | `404` | `{"error": "Transaccion no encontrada"}` |

---

## 5. Tecnologías utilizadas

| Capa | Tecnología | Versión verificada |
|---|---|---|
| Frontend | React | 19.2 |
| Frontend | Vite | 8.1 |
| Frontend | Tailwind CSS | 4.3 |
| Backend | Python | 3.13 |
| Backend | Flask | 3.1 |
| Backend | Flask-CORS | 6.0 |
| Backend | Prisma Client Python | 0.15 |
| Base de datos | MySQL | 8 |
| Infraestructura | Docker | 29.6 |
| Control de versiones | Git / GitHub | — |

---

## 6. Cómo ejecutar el sistema

### 6.1 Requisitos previos

- **Docker Desktop** — <https://www.docker.com/products/docker-desktop/> (requiere WSL2 en Windows)
- **Python 3** — <https://www.python.org/downloads/>
- **Node.js LTS** — <https://nodejs.org/>

### 6.2 Primera vez: crear el contenedor de la base de datos

```powershell
docker run --name empresa -e MYSQL_ROOT_PASSWORD=12345 -p 3306:3306 -v mysql_datos:/var/lib/mysql -d mysql:8
```

Este comando se ejecuta **una sola vez**. Las siguientes veces basta con `docker start empresa`.

### 6.3 Arranque (tres terminales, en este orden)

**Terminal 1 — Base de datos**

```powershell
docker start empresa
```

Esperar entre 10 y 20 segundos: MySQL tarda en quedar disponible.

**Terminal 2 — Backend**

```powershell
cd "MisProyectosPython\Proyecto_Completo\BACKEND"
pip install -r requirements.txt
prisma db push
python app.py
```

Debe mostrar `Running on http://127.0.0.1:5000`. Verificación:

```powershell
curl http://localhost:5000/api/transacciones/
```

**Terminal 3 — Frontend**

```powershell
cd "MisProyectosPython\Proyecto_Completo\FRONTEND"
npm install
npm run dev
```

Abrir <http://localhost:5173> en el navegador.

### 6.4 Cargar los datos iniciales (opcional)

Si la base está vacía, el script de la Semana 3 la puebla con las transacciones de origen:

```powershell
cd "MisProyectosPython\Semana_3\Mysql_Prisma"
python migrar_transacciones.py
```

---

## 7. Evidencia de funcionamiento

Sistema verificado end-to-end con las tres capas activas:

**Respuesta del backend** — `GET /api/transacciones/` devuelve `200` con las cuatro transacciones
persistidas en MySQL:

```json
[
  { "id": 4, "codigo": "T004", "tipo": "DEBITO",  "monto": 45000,   "impacto": 1500.0 },
  { "id": 3, "codigo": "T003", "tipo": "CREDITO", "monto": 1200000, "impacto": 24000.0 },
  { "id": 2, "codigo": "T002", "tipo": "DEBITO",  "monto": 80000,   "impacto": 1500.0 },
  { "id": 1, "codigo": "T001", "tipo": "CREDITO", "monto": 500000,  "impacto": 10000.0 }
]
```

**Frontend** — la tabla renderiza las cuatro transacciones consumidas por `fetch()` desde la API,
con los formularios de creación y edición operativos.

**Pruebas de validación ejecutadas:**

| Caso de prueba | Resultado esperado | Resultado obtenido |
|---|---|---|
| `POST` con `monto: -5000` | Rechazo `400` | ✅ `400` |
| `POST` con código `T001` (duplicado) | Rechazo `400` | ✅ `400` |
| `GET /999` (no existe) | `404` | ✅ `404` |

En los tres casos el servidor respondió con el código correcto y **siguió funcionando**, que es
justamente el propósito del manejo de excepciones.

> Se recomienda adjuntar capturas de pantalla de: la tabla en el navegador, la respuesta JSON del
> backend, el mensaje de error al intentar un monto negativo, y el contenedor activo en Docker
> Desktop.

---

## 8. Trazabilidad con el curso

| Semana | Concepto | Dónde se aplica en el sistema |
|---|---|---|
| 1–2 | Lectura de archivos, POO | Origen de los datos (`transacciones.txt`) y modelado de la entidad |
| 3 | Encapsulamiento, SOLID (SRP) | Validación de `monto` en el controlador; separación `routes`/`controllers`/`models` |
| 3 | Persistencia con Prisma y MySQL en Docker | `schema.prisma` y `models/transaccion_model.py` |
| 4 | `try/except`, robustez | Cada función del controlador responde `400`/`404` en vez de caerse |
| 4 | Serialización JSON | Todas las respuestas de la API; el frontend las consume con `fetch()` |
| 5 | Git y GitHub | Historial de commits, ramas y sincronización con el repositorio *upstream* |
| 6 | UML y patrones de diseño | Diagrama de clases que documenta la entidad `Transaccion` |
| 7 | Bases de datos relacionales | Llaves primarias, restricción `UNIQUE` y consultas parametrizadas |

---

## 9. Conclusiones

1. **La separación en capas tiene un costo inicial y un beneficio permanente.** Escribir tres
   archivos donde cabría uno parece innecesario hasta que hay que cambiar algo: cada modificación
   queda confinada a una sola capa.

2. **La validación debe vivir en el servidor.** El navegador puede ser manipulado; el control del
   monto negativo está en el controlador, no en el formulario, de modo que ninguna petición
   directa a la API puede saltárselo.

3. **La persistencia cambia la naturaleza del programa.** Con la base de datos en un volumen de
   Docker, la información sobrevive al reinicio del contenedor y del equipo — la diferencia entre
   un ejercicio y un sistema.

4. **El contrato de la API es lo único que une las capas.** Mientras los endpoints no cambien,
   frontend y backend pueden evolucionar de forma completamente independiente.
