
UPDATE_RESPONSES = {
    200: {
        "description": "Usuario actualizado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 1,
                    "message": "Usuario actualizado exitosamente",
                    "errors": None,
                    "meta": None
                }
            }
        }
    },
    422: {
        "description": "Error de validación en parámetros o datos",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error de validación",
                    "errors": [
                        {
                            "code": "VALIDATION_ERROR",
                            "message": "id debe ser mayor a 0",
                            "field": "id",
                            "details": None
                        }
                    ],
                    "meta": None
                }
            }
        }
    },
    404: {
        "description": "Usuario no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Usuario no encontrado",
                    "errors": [
                        {
                            "code": "RECORD_NOT_FOUND",
                            "message": "Usuario no encontrado",
                            "field": None,
                            "details": None
                        }
                    ],
                    "meta": None
                }
            }
        }
    },
    500: {
        "description": "Error interno del servidor",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error interno del servidor",
                    "errors": [
                        {
                            "code": "DATABASE_ERROR",
                            "message": "Error en la base de datos",
                            "field": None,
                            "details": None
                        }
                    ],
                    "meta": None
                }
            }
        }
    }
}

UPDATE_SUMMARY = "Actualiza un registro en la tabla usuario"

UPDATE_DESCRIPTION = """
## Resumen
Actualiza un Usuario existente identificado por su clave primaria.

Solo se actualizan los campos incluidos en el body. Los campos omitidos **no se modifican**.

## Campos actualizables
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | `str` | Nombre del usuario |
| `pwd` | `str` | Campo pwd de la tabla usuario |
| `email` | `str` | Campo email de la tabla usuario |
| `last_post_date` | `datetime` | Campo last_post_date de la tabla usuario |

## Escrituras anidadas (Nested Writes)
El campo `values` admite operaciones en cascada sobre relaciones one-to-many.
Cada relación soporta tres operaciones simultáneas: `create`, `update` y `delete`.

### `posts`
Relación hacia **Post** (one-to-many).

```json
{
"name": "nuevo_valor",
    "posts": {
        "create": [
            { /* PostCreate — crea nuevos Posts asociados */ }
        ],
        "update": [
            {
                "author_id": 1,
                "values": { /* PostUpdateValues — campos a modificar */ }
            }
        ],
        "delete": [1, 2, 3]  // Lista de PKs de Post a eliminar
    }
}
```

> **Nota:** Las tres operaciones son opcionales e independientes. Puedes enviar solo `create`, solo `delete`, o cualquier combinación.

## Ejemplo básico
```json
{
"name": "valor_actualizado",
"pwd": "valor_actualizado",
"email": "valor_actualizado"
}
```
"""

UPDATE_MANY_RESPONSES = {
    200: {
        "description": "Usuarios actualizados exitosamente",
        "content": {
            "application/json": {
                "examples": {
                    "records_updated": {
                        "summary": "Registros actualizados",
                        "value": {
                            "status": "success",
                            "data": 5,
                            "message": "5 Usuarios actualizados exitosamente",
                            "errors": None,
                            "meta": None
                        }
                    },
                    "no_records_found": {
                        "summary": "No se encontraron registros",
                        "value": {
                            "status": "success",
                            "data": 0,
                            "message": "No se encontraron registros que coincidan con los criterios",
                            "errors": None,
                            "meta": None
                        }
                    }
                }
            }
        }
    },
    422: {
        "description": "Error de validación en los datos",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error de validación",
                    "errors": [
                        {
                            "code": "VALIDATION_ERROR",
                            "message": "Los criterios de búsqueda son requeridos",
                            "field": "filters",
                            "details": None
                        }
                    ],
                    "meta": None
                }
            }
        }
    },
    500: {
        "description": "Error interno del servidor",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error interno del servidor",
                    "errors": [
                        {
                            "code": "DATABASE_ERROR",
                            "message": "Error en la base de datos",
                            "field": None,
                            "details": None
                        }
                    ],
                    "meta": None
                }
            }
        }
    }
}

UPDATE_MANY_SUMMARY = "Actualiza múltiples registros en la tabla usuario"