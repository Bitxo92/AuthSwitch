
UPDATE_RESPONSES = {
    200: {
        "description": "Post actualizado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 1,
                    "message": "Post actualizado exitosamente",
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
        "description": "Post no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Post no encontrado",
                    "errors": [
                        {
                            "code": "RECORD_NOT_FOUND",
                            "message": "Post no encontrado",
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

UPDATE_SUMMARY = "Actualiza un registro en la tabla post"

UPDATE_DESCRIPTION = """
## Resumen
Actualiza un Post existente identificado por su clave primaria.

Solo se actualizan los campos incluidos en el body. Los campos omitidos **no se modifican**.

## Campos actualizables
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `title` | `str` | Campo title de la tabla post |
| `content` | `str` | Contenido del post |
| `content_type` | `str` | Campo content_type de la tabla post |
| `timestamp` | `datetime` | Fecha y hora del post |
| `author_id` | `int` | Campo author_id de la tabla post |

## Escrituras anidadas (Nested Writes)
El campo `values` admite operaciones en cascada sobre relaciones one-to-many.
Cada relación soporta tres operaciones simultáneas: `create`, `update` y `delete`.

### `comments`
Relación hacia **Comment** (one-to-many).

```json
{
"title": "nuevo_valor",
    "comments": {
        "create": [
            { /* CommentCreate — crea nuevos Comments asociados */ }
        ],
        "update": [
            {
                "post_id": 1,
                "values": { /* CommentUpdateValues — campos a modificar */ }
            }
        ],
        "delete": [1, 2, 3]  // Lista de PKs de Comment a eliminar
    }
}
```

> **Nota:** Las tres operaciones son opcionales e independientes. Puedes enviar solo `create`, solo `delete`, o cualquier combinación.

## Ejemplo básico
```json
{
"title": "valor_actualizado",
"content": "valor_actualizado",
"content_type": "valor_actualizado"
}
```
"""

UPDATE_MANY_RESPONSES = {
    200: {
        "description": "Posts actualizados exitosamente",
        "content": {
            "application/json": {
                "examples": {
                    "records_updated": {
                        "summary": "Registros actualizados",
                        "value": {
                            "status": "success",
                            "data": 5,
                            "message": "5 Posts actualizados exitosamente",
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

UPDATE_MANY_SUMMARY = "Actualiza múltiples registros en la tabla post"