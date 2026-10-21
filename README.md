# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de la materia Metodología de Sistemas II.

El proyecto implementa un módulo sencillo para registrar y gestionar solicitudes académicas realizadas por estudiantes. Su propósito es permitir el análisis de una versión inicial funcional, detectar problemas de calidad interna y aplicar posteriormente un proceso de refactoring seguro.

## Integrantes

- Emilia Gómez Juárez
- Giselle Chaumont

## Estado del proyecto

En principio, el repositorio contiene la versión inicial del sistema.

Esta versión conserva intencionalmente una estructura simple y algunos problemas de diseño que serán identificados y corregidos durante las siguientes etapas del trabajo.

El estado inicial se encuentra identificado mediante el tag:

`estado-inicial`

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

La versión inicial no requiere instalar dependencias externas.

## Estructura inicial

```text
.
├── initial/
│   ├── __init__.py
│   └── app.py
├── .gitignore
└── README.md