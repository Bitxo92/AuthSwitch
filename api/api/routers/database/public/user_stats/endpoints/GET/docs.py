from typing import Optional, List, Union

FIND_MANY_RESPONSES = {
    200: {
        "description": "Lista de registros de user_stats obtenido exitosamente",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/APIResponse_List_UserStatsRead__"
                }
            }
        },
        "links": {
            "self": {
                "operationId": "user_stats_find_many",
                "description": "Enlace a la consulta actual con los mismos filtros",
                "parameters": {
        "user_id": "$request.query.user_id",
        "user_name": "$request.query.user_name",
        "post_count": "$request.query.post_count",
                    "limit": "$request.query.limit",
                    "offset": "$request.query.offset",
                    "order_by": "$request.query.order_by",
                    "order": "$request.query.order",
                    "includes": "$request.query.includes"
                }
            },
            "item": {
                "operationId": "user_stats_find",
                "description": "Enlace para acceder a un elemento específico",
                "parameters": {
                    "includes": "$request.query.includes"
                }
            },
            "create": {
                "operationId": "user_stats_create",
                "description": "Enlace para crear un nuevo UserStats"
            },
            "count": {
                "operationId": "user_stats_count",
                "description": "Enlace para obtener el conteo total con los mismos filtros",
                "parameters": {
        "user_id": "$request.query.user_id",
        "user_name": "$request.query.user_name",
        "post_count": "$request.query.post_count",
                }
            }}
    },
    422: {
        "description": "Error de validación en parámetros",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error de validación",
                    "errors": [
                        {
                            "code": "VALIDATION_ERROR",
                            "message": "El límite no puede ser negativo",
                            "field": "limit",
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

FIND_MANY_SUMMARY = "Busca varios registros en la tabla user_stats"
FIND_MANY_DESCRIPTION = """
## Resumen
Obtiene una lista de `user_statss` con filtros opcionales y soporte para paginación.

Este endpoint permite realizar búsquedas flexibles aplicando filtros opcionales
por cualquiera de los campos disponibles, con soporte completo para paginación
mediante los parámetros limit y offset.

## Resultado
En `APIResponse.data`, retorna un listado de objetos donde cada uno representa un registro de la tabla `user_stats` que incluye todos sus atributos

## Datos
Para cada registro en `data` se incluye:
- **user_id** (int): Campo user_id de la tabla user_stats
- **user_name** (str): Campo user_name de la tabla user_stats
- **post_count** (int): Campo post_count de la tabla user_stats

## Parámetros de Filtrado

Todos los parámetros de filtrado son opcionales y se pueden combinar:
- **user_id**: Filtrar por user_id
    - **in_user_id**: Filtrar por múltiples valores de user_id (OR lógico)
    - **min_user_id**: Filtrar por valor mínimo de user_id (incluído)
    - **max_user_id**: Filtrar por valor máximo de user_id (incluído)
    - **user_name**: Filtrar por user_name
    - **in_user_name**: Filtrar por múltiples valores de user_name (OR lógico)
    - **post_count**: Filtrar por post_count
    - **in_post_count**: Filtrar por múltiples valores de post_count (OR lógico)
    - **min_post_count**: Filtrar por valor mínimo de post_count (incluído)
    - **max_post_count**: Filtrar por valor máximo de post_count (incluído)


## Parámetros de Paginación

- **limit**: Número máximo de registros a retornar. Solo admite valores positivos. Si no se especifica, retorna todos los registros que coincidan con los filtros.
- **order_by**: Lista de nombres de columnas para ordenar los resultados.⚠️ **IMPORTANTE**: los nombres de columnas deben existir, si no serán omitidas.
- **order**: Dirección de ordenamiento: 'ASC' para ascendente (por defecto), 'DESC' para descendente. Solo aplica si order_by está definido.
- **offset**: Número de registros a omitir desde el inicio. Solo admite valores positivos. Si no se especifica, inicia desde el primer registro.

## Consulta combinada (recomendado para pocos registros)
⚠️ **IMPORTANTE**: Usa siempre el parámetro `includes` para cargar relaciones en una sola consulta y evitar múltiples llamadas al API.

⚠️ **WARNING**: Si la relación incluida tiene muchos registros relacionados, la respuesta puede ser muy grande y lenta. Mejor consultar su endpoint directamente con filtros.

El parametro `includes` permite cargar relaciones asociadas a los registros.
"""

COUNT_RESPONSES = {
    200: {
        "description": "Conteo realizado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 42,
                    "message": "Conteo realizado exitosamente",
                    "errors": None,
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

COUNT_SUMMARY = "Cuenta registros en la tabla user_stats"

EXISTS_RESPONSES = {
    200: {
        "description": "Verificación realizada exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": True,
                    "message": "Verificación realizada exitosamente",
                    "errors": None,
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

EXISTS_SUMMARY = "Verifica existencia en la tabla user_stats"

AGG_FIELD_422 = {
    "description": "Campo inválido o no válido para la operación",
    "content": {
        "application/json": {
            "example": {
                "status": "error",
                "data": None,
                "message": "Error de validación",
                "errors": [
                    {
                        "code": "VALIDATION_ERROR",
                        "message": "El campo especificado no es válido para la operación",
                        "field": "field",
                        "details": None
                    }
                ],
                "meta": None
            }
        }
    }
}

AGG_FIELD_500 = {
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

SUM_RESPONSES = {
    200: {
        "description": "Suma calculada exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 12500.75,
                    "message": "Suma de 'campo' calculada exitosamente",
                    "errors": None,
                    "meta": None
                }
            }
        }
    },
    422: AGG_FIELD_422,
    500: AGG_FIELD_500
}

SUM_SUMMARY = "Suma un campo numérico específico en la tabla user_stats"

MEAN_RESPONSES = {
    200: {
        "description": "Media calculada exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 32.45,
                    "message": "Media de 'campo' calculada exitosamente",
                    "errors": None,
                    "meta": None
                }
            }
        }
    },
    422: AGG_FIELD_422,
    500: AGG_FIELD_500
}

MEAN_SUMMARY = "Calcula la media de un campo numérico específico en la tabla user_stats"

MAX_RESPONSES = {
    200: {
        "description": "Valor máximo encontrado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 99999.99,
                    "message": "Máximo de 'campo' encontrado exitosamente",
                    "errors": None,
                    "meta": None
                }
            }
        }
    },
    422: AGG_FIELD_422,
    500: AGG_FIELD_500
}

MAX_SUMMARY = "Encuentra el valor máximo de un campo específico en la tabla user_stats"

MIN_RESPONSES = {
    200: {
        "description": "Valor mínimo encontrado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 100.00,
                    "message": "Mínimo de 'campo' encontrado exitosamente",
                    "errors": None,
                    "meta": None
                }
            }
        }
    },
    422: AGG_FIELD_422,
    500: AGG_FIELD_500
}

MIN_SUMMARY = "Encuentra el valor mínimo de un campo específico en la tabla user_stats"

