# taskmaster - Gestor de proyectos y tareas

> Aplicación web para **gestionar proyectos y tareas** con un CRUD completo y una API REST.

Backend en **Flask (Python)** con base de datos **SQLite** y frontend en **HTML, CSS y
JavaScript** sin frameworks. Permite crear, listar, editar y eliminar proyectos, y asignarles
tareas con un estado (`Pendiente`, `En progreso` o `Completada`).

![Python](https://img.shields.io/badge/Python-3.x-3776AB)
![Flask](https://img.shields.io/badge/Flask-3-000000)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57)
![JavaScript](https://img.shields.io/badge/JavaScript-vanilla-F7DF1E)

---

## Tabla de contenido

- [Características](#características)
- [Stack tecnológico](#stack-tecnológico)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Uso](#uso)
- [API REST](#api-rest)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Autor](#autor)

---

## Características

- **CRUD de proyectos:** crear, listar, editar y eliminar proyectos (título y descripción).
- **CRUD de tareas:** crear, listar y eliminar tareas, y cambiar su estado.
- **Relación proyecto → tareas:** cada tarea se asigna a un proyecto (`1:N` con llave
  foránea).
- **Estados de tarea:** `Pendiente`, `En progreso` y `Completada`.
- **Integridad referencial:** no se puede eliminar un proyecto que tenga tareas asociadas.
- **API REST** en JSON consumida desde el frontend con `fetch`.

## Stack tecnológico

| Capa          | Tecnología                                  |
|---------------|---------------------------------------------|
| Backend       | Python + Flask (API REST)                   |
| Base de datos | SQLite (módulo estándar `sqlite3`)          |
| Frontend      | HTML, CSS y JavaScript (vanilla)            |
| Servidor      | Servidor de desarrollo de Flask (puerto 5000) |

## Requisitos

- **Python 3.x**.
- **Flask** (`pip install flask`).

## Instalación y ejecución

1. Instala la única dependencia:

   ```bash
   pip install flask
   ```

2. Ejecuta la aplicación:

   ```bash
   python app.py
   ```

   La base de datos (`proyectos.db`) y sus tablas se crean automáticamente en el primer
   arranque.

3. Abre en el navegador: `http://localhost:5000`

## Uso

1. En la sección **Proyectos**, escribe un título (y opcionalmente una descripción) y
   presiona **Crear Proyecto**.
2. En la sección **Tareas**, escribe el nombre, elige el proyecto al que pertenece y
   presiona **Crear Tarea**.
3. Usa **Estado** para cambiar una tarea entre `Pendiente`, `En progreso` y `Completada`.
4. Usa **Editar** y **Borrar** en cada tabla para modificar o eliminar registros.

## API REST

### Proyectos

| Método | Ruta              | Descripción                    |
|--------|-------------------|--------------------------------|
| GET    | `/proyectos`      | Lista todos los proyectos      |
| GET    | `/proyectos/<id>` | Obtiene un proyecto por ID     |
| POST   | `/proyectos`      | Crea un proyecto               |
| PUT    | `/proyectos/<id>` | Actualiza un proyecto          |
| DELETE | `/proyectos/<id>` | Elimina un proyecto            |

### Tareas

| Método | Ruta            | Descripción                 |
|--------|-----------------|-----------------------------|
| GET    | `/tareas`       | Lista todas las tareas      |
| GET    | `/tareas/<id>`  | Obtiene una tarea por ID    |
| POST   | `/tareas`       | Crea una tarea              |
| PUT    | `/tareas/<id>`  | Actualiza una tarea         |
| DELETE | `/tareas/<id>`  | Elimina una tarea           |


## Autor

- **Josué Martínez** - [@Lalocarrito](https://github.com/Lalocarrito)

