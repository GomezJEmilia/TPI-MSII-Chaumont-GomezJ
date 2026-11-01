# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de la materia Metodología de Sistemas II.

El proyecto implementa un módulo sencillo para registrar y gestionar solicitudes académicas realizadas por estudiantes. Su propósito es permitir el análisis de una versión inicial funcional, detectar problemas de calidad interna y aplicar posteriormente un proceso de refactoring seguro.

## Integrantes

- Emilia Gómez Juárez
- Giselle Chaumont

## Estado del proyecto

El repositorio contiene la versión inicial y la versión refactorizada del sistema, además de una demostración y pruebas automatizadas. 

La versión inicial se conserva como referencia y puede consultarse mediante el tag estado-inicial. 

La versión refactorizada organiza el código en modelos, repositorio y servicio y puede consultarse mediante el tag estado-refactorizado.

## Alcance

El sistema permite gestionar solicitudes académicas realizadas por estudiantes y derivarlas al área responsable correspondiente.

Los datos se almacenan temporalmente en memoria y se reinician al finalizar la ejecución. Se utilizan exclusivamente datos ficticios.

## Actores principales

- Estudiante: realiza una solicitud académica.
- Área responsable: recibe y gestiona las solicitudes asignadas.
- Personal administrativo: registra, consulta y actualiza las solicitudes.

## Funcionalidades de la versión inicial

- Registrar una solicitud académica.
- Asignar una solicitud a un área responsable.
- Cambiar el estado de una solicitud.
- Buscar y filtrar solicitudes.
- Generar un reporte básico por estado y prioridad.

## Estados disponibles

Las solicitudes pueden atravesar los siguientes estados:

1. `pending`: solicitud pendiente.
2. `in_progress`: solicitud en tratamiento.
3. `resolved`: solicitud resuelta.

Las transiciones permitidas son:

`pending` → `in_progress` → `resolved`

## Tecnologías utilizadas

- Python 3.9 o superior.
- Datos almacenados en memoria.
- Biblioteca estándar de Python.

El proyecto no requiere instalar dependencias externas.


## Estructura inicial

```text

├── docs/
│   ├── code_review.md
│   └── diagnostico.md
├── initial/
│   ├── __init__.py
│   └── app.py
├── refactored/
│   ├── __init__.py
│   ├── models.py
│   ├── repository.py
│   └── service.py
├── tests/
│   └── test_requests.py
├── demo.py
├── .gitignore
└── README.md
```


## Ejecución y pruebas

Ejecutar la demostración con la versión inicial:

```bash
python3 demo.py --version initial
```

Ejecutarla con la versión refactorizada:

```bash
python3 demo.py --version refactored
```

Ejecutar las pruebas:

```bash
python3 -m unittest discover -s tests -v
```
