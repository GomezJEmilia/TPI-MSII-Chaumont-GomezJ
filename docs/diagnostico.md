# Diagnóstico de deuda técnica y code smells

## Propósito

Este documento registra el diagnóstico técnico realizado sobre la versión inicial
del Sistema de Gestión de Solicitudes Académicas.

El análisis se concentra en el archivo
[`initial/app.py`](../initial/app.py), correspondiente a la versión preservada
mediante el tag `estado-inicial`.

La aplicación cumple las operaciones funcionales requeridas, pero presenta
debilidades en su estructura interna. Estos problemas no impiden su funcionamiento
actual, aunque incrementan el esfuerzo necesario para comprender, probar,
modificar y extender el sistema.

Un code smell no representa necesariamente un error funcional. Se trata de una
señal que puede indicar una decisión de diseño mejorable o un riesgo futuro de
mantenimiento.

## Criterio de priorización

| Prioridad | Criterio |
|---|---|
| **P1 — Alta** | Puede introducir errores en cambios frecuentes, afecta responsabilidades centrales o condiciona gran parte de la refactorización. |
| **P2 — Media** | Dificulta el mantenimiento y debería corregirse durante el refactoring, pero no representa un riesgo inmediato para el funcionamiento. |
| **P3 — Baja** | Su impacto actual es reducido por el tamaño del prototipo, aunque podría adquirir importancia si el sistema crece. |

## Matriz de deuda técnica y code smells

Las líneas mencionadas corresponden a `initial/app.py` en el tag
`estado-inicial`.

| N.º | Code smell o debilidad | Evidencia y ubicación | Impacto actual | Riesgo de mantenimiento | Prioridad |
|---:|---|---|---|---|:---:|
| 1 | Clase con demasiadas responsabilidades | `AcademicRequestApp` administra estudiantes, áreas y solicitudes; valida entradas; aplica reglas de negocio; realiza búsquedas y genera reportes. Líneas 8 a 126. | La lógica de todo el sistema está concentrada en una única clase. | Un cambio en la persistencia, las validaciones o los reportes puede afectar operaciones que no deberían estar relacionadas. La clase seguirá creciendo al incorporar funcionalidades. | **P1** |
| 2 | Representación de entidades mediante diccionarios | Estudiantes, áreas y solicitudes se representan con diccionarios. Líneas 10 a 19 y 33 a 41. | Las entidades no poseen tipos, atributos ni comportamientos propios. | Una clave incorrecta, como `studentId` en lugar de `student_id`, solo se detectaría durante la ejecución. También resulta difícil garantizar que todos los diccionarios mantengan la misma estructura. | **P1** |
| 3 | Cadenas mágicas | Los estados, prioridades y categorías aparecen como textos literales: `"pending"`, `"resolved"`, `"high"` y `"certificate"`, entre otros. Líneas 25 a 28, 39, 56, 69 a 76, 81 a 84 y 106 a 117. | Los mismos valores se encuentran distribuidos en varios métodos. | Un error de escritura o la incorporación de un nuevo estado obliga a localizar y modificar múltiples fragmentos. Pueden producirse valores inconsistentes sin detección previa. | **P1** |
| 4 | Código duplicado para buscar solicitudes | `assign_area()` y `change_status()` recorren `self.requests`, comparan el identificador y verifican si el resultado es `None`. Líneas 49 a 55 y 62 a 68. | La misma operación se implementa dos veces. | Si cambia la forma de localizar una solicitud, deben modificarse ambos métodos. Una copia podría actualizarse y la otra conservar un comportamiento diferente. | **P1** |
| 5 | Validaciones duplicadas | La prioridad se valida en `register()` y nuevamente en `list_requests()`. Los estados también se enumeran en diferentes métodos. Líneas 27 a 28, 69 a 70 y 81 a 84. | Las reglas de validación se encuentran dispersas. | Al incorporar una prioridad o un estado, alguna validación podría quedar sin actualizar y producir comportamientos contradictorios. | **P2** |
| 6 | Lógica de conteo repetitiva y rígida | `report()` declara seis contadores y utiliza seis condiciones independientes para construir el resultado. Líneas 98 a 126. | La lógica está vinculada a una cantidad fija de estados y prioridades. | Agregar o eliminar un valor requiere modificar las variables, las condiciones y el diccionario de retorno. Esto aumenta la posibilidad de omisiones. | **P2** |
| 7 | Parámetros primitivos relacionados | `register()` recibe `student_id`, `category`, `priority` y `description` como parámetros independientes. Línea 22. | La llamada depende del orden correcto de diferentes valores primitivos relacionados con una misma solicitud. | Los argumentos podrían intercambiarse accidentalmente. Agregar nuevos datos obligaría a ampliar la firma del método y todas sus llamadas. | **P2** |
| 8 | Datos y almacenamiento acoplados al constructor | Los estudiantes, las áreas, la lista de solicitudes y el contador se crean directamente en `__init__()`. Líneas 9 a 20. | La clase depende de datos fijos y de una implementación concreta en memoria. | Reemplazar la memoria por una base de datos, un archivo o un repositorio requeriría modificar la lógica de negocio. También dificulta preparar datos diferentes para las pruebas. | **P1** |
| 9 | Excepciones demasiado genéricas | Todas las condiciones inválidas generan `ValueError`, por ejemplo en las líneas 23 a 32, 47 a 57 y 67 a 76. | Distintas fallas de dominio se comunican mediante el mismo tipo de excepción. | El código cliente deberá interpretar los mensajes para distinguir entre una entidad inexistente, un dato inválido o una transición prohibida. | **P2** |
| 10 | Búsqueda lineal de solicitudes | Para encontrar una solicitud se recorre completamente `self.requests`. Líneas 50 a 53 y 63 a 66. | Con pocos registros, el impacto sobre el rendimiento es insignificante. | Si aumenta la cantidad de solicitudes, cada búsqueda puede recorrer toda la lista. La solución no escala tan bien como una estructura indexada por identificador. | **P3** |
| 11 | Ausencia de anotaciones de tipo | Los métodos no especifican los tipos esperados de sus parámetros ni de sus valores de retorno. Líneas 9, 22, 46, 61, 80 y 98. | El contrato de cada método debe deducirse mediante la lectura de su implementación. | Reduce la asistencia del IDE y dificulta detectar anticipadamente argumentos o retornos incompatibles durante futuras modificaciones. | **P2** |
| 12 | Mensajes de error poco contextualizados | Se utiliza el mensaje `"Invalid status transition"` para diferentes situaciones. Líneas 71 a 76. | El mensaje no indica cuál fue la transición solicitada ni desde qué estado se intentó realizar. | Diagnosticar fallas será más difícil y una interfaz futura no podrá presentar información específica sin interpretar o reemplazar estos mensajes. | **P3** |

## Evidencias representativas

### Concentración de responsabilidades

La clase principal crea y almacena los datos que utiliza el sistema:

```python
class AcademicRequestApp:
    def __init__(self):
        self.students = {
            1: {"id": 1, "name": "Ana Pérez"},
            2: {"id": 2, "name": "Martín López"},
            3: {"id": 3, "name": "Lucía Gómez"},
        }
        self.areas = {
            1: {"id": 1, "name": "Secretaría Académica"},
            2: {"id": 2, "name": "Coordinación de Carrera"},
        }
        self.requests = []
        self.next_id = 1
```

Además de almacenar los datos, `AcademicRequestApp` realiza validaciones, aplica
reglas de negocio, localiza solicitudes, modifica estados y genera reportes.
Esto concentra responsabilidades que podrían separarse en componentes con
propósitos específicos.

### Entidades representadas mediante diccionarios

Las solicitudes se construyen como diccionarios:

```python
request = {
    "id": self.next_id,
    "student_id": student_id,
    "category": category,
    "priority": priority,
    "description": description.strip(),
    "status": "pending",
    "area_id": None,
}
```

Esta representación es funcional, pero no define explícitamente una entidad de
dominio. La estructura depende de que todas las claves estén correctamente
escritas y sean utilizadas de la misma manera en todos los métodos.

### Búsqueda duplicada

En `assign_area()` se busca una solicitud de la siguiente manera:

```python
found = None
for request in self.requests:
    if request["id"] == request_id:
        found = request
        break

if found is None:
    raise ValueError("Request not found")
```

La misma secuencia aparece nuevamente en `change_status()`:

```python
found = None
for request in self.requests:
    if request["id"] == request_id:
        found = request
        break

if found is None:
    raise ValueError("Request not found")
```

La repetición genera dos puntos de mantenimiento para una misma operación. Una
posible mejora consiste en extraer la búsqueda a un método o componente
especializado.

### Uso de cadenas mágicas

Los estados se escriben directamente como cadenas de texto:

```python
if new_status not in ("pending", "in_progress", "resolved"):
    raise ValueError("Invalid status")

if found["status"] == "pending" and new_status != "in_progress":
    raise ValueError("Invalid status transition")

if found["status"] == "in_progress" and new_status != "resolved":
    raise ValueError("Invalid status transition")
```

La misma lista de estados aparece también en otros métodos. Esto dispersa la
definición de los valores permitidos y obliga a modificar varios puntos cuando
cambia una regla.

### Lógica rígida del reporte

El método `report()` declara un contador para cada estado y prioridad:

```python
pending = 0
in_progress = 0
resolved = 0
low = 0
medium = 0
high = 0
```

Después utiliza condiciones independientes:

```python
if request["status"] == "pending":
    pending += 1

if request["status"] == "in_progress":
    in_progress += 1

if request["status"] == "resolved":
    resolved += 1
```

Esta lógica funciona con los valores actuales, pero requiere modificar diferentes
secciones del método al incorporar un nuevo estado o una nueva prioridad.

### Almacenamiento acoplado

El almacenamiento en memoria se crea directamente dentro de
`AcademicRequestApp`:

```python
self.students = {...}
self.areas = {...}
self.requests = []
```

La lógica del sistema depende de estas estructuras concretas. Por lo tanto,
cambiar el mecanismo de persistencia implicaría modificar la misma clase que
contiene las reglas de negocio.

## Relación entre los hallazgos

Los problemas identificados no aparecen de manera aislada. La concentración de
responsabilidades provoca que el almacenamiento, las validaciones y las reglas
de negocio dependan de una única clase. Al mismo tiempo, el uso de diccionarios
y cadenas mágicas debilita la representación del dominio.

La duplicación de búsquedas y validaciones aumenta la cantidad de lugares que
deben modificarse cuando cambia una regla. Esto incrementa el riesgo de que dos
partes del sistema evolucionen de manera diferente.

## Conclusión

El diagnóstico demuestra que la versión inicial posee calidad externa suficiente
para cumplir los casos de uso solicitados, pero presenta debilidades de calidad
interna.

Las prioridades principales son separar responsabilidades, representar
explícitamente las entidades del dominio, centralizar estados y prioridades,
eliminar búsquedas duplicadas y desacoplar el almacenamiento de la lógica del
sistema.

Estas observaciones servirán como fundamento para aplicar principios SOLID,
técnicas de Clean Code y refactorings controlados. La versión inicial permanece
preservada mediante el tag `estado-inicial`, lo que permitirá comparar ambas
implementaciones y verificar que las mejoras estructurales no alteren
negativamente el comportamiento externo.