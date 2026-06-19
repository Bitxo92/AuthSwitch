from typing import Optional, List, Union

FIND_MANY_RESPONSES = {
    200: {
        "description": "Lista de registros de usuario obtenido exitosamente",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/APIResponse_List_UsuarioRead__"
                }
            }
        },
        "links": {
            "self": {
                "operationId": "usuario_find_many",
                "description": "Enlace a la consulta actual con los mismos filtros",
                "parameters": {
        "name": "$request.query.name",
        "email": "$request.query.email",
        "last_post_date": "$request.query.last_post_date",
                    "limit": "$request.query.limit",
                    "offset": "$request.query.offset",
                    "order_by": "$request.query.order_by",
                    "order": "$request.query.order",
                    "includes": "$request.query.includes"
                }
            },
            "item": {
                "operationId": "usuario_find",
                "description": "Enlace para acceder a un elemento específico",
                "parameters": {
                    "id": "$response.body#/data/**/id",
                    "includes": "$request.query.includes"
                }
            },
            "create": {
                "operationId": "usuario_create",
                "description": "Enlace para crear un nuevo Usuario"
            },
            "count": {
                "operationId": "usuario_count",
                "description": "Enlace para obtener el conteo total con los mismos filtros",
                "parameters": {
        "name": "$request.query.name",
        "email": "$request.query.email",
        "last_post_date": "$request.query.last_post_date",
                }
            },
        "posts": {
        "operationId": "post_find_many",
                "description": "Enlace a los Posts relacionados",
                "parameters": {
                    "id": "$response.body#/data/**/author_id",
                    "includes": "$request.query.includes"
                }
        }
        }
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

FIND_MANY_SUMMARY = "Busca varios registros en la tabla usuario"
FIND_MANY_DESCRIPTION = """
## Resumen
Obtiene una lista de `usuarios` con filtros opcionales y soporte para paginación.

Este endpoint permite realizar búsquedas flexibles aplicando filtros opcionales
por cualquiera de los campos disponibles, con soporte completo para paginación
mediante los parámetros limit y offset.

## Resultado
En `APIResponse.data`, retorna un listado de objetos donde cada uno representa un registro de la tabla `usuario` que incluye todos sus atributos

## Datos
Para cada registro en `data` se incluye:
- **id** (int): Campo id de la tabla usuario
- **name** (str): Nombre del usuario
- **pwd** (str): Campo pwd de la tabla usuario
- **email** (str, opcional): Campo email de la tabla usuario
- **last_post_date** (datetime, opcional): Campo last_post_date de la tabla usuario

## Parámetros de Filtrado

Todos los parámetros de filtrado son opcionales y se pueden combinar:
- **name**: Filtrar por name
    - **in_name**: Filtrar por múltiples valores de name (OR lógico)
    - **email**: Filtrar por email
    - **in_email**: Filtrar por múltiples valores de email (OR lógico)
    - **min_last_post_date**: Filtrar por valor mínimo de last_post_date (incluído)
    - **max_last_post_date**: Filtrar por valor máximo de last_post_date (incluído)


## Parámetros de Paginación

- **limit**: Número máximo de registros a retornar. Solo admite valores positivos. Si no se especifica, retorna todos los registros que coincidan con los filtros.
- **order_by**: Lista de nombres de columnas para ordenar los resultados.⚠️ **IMPORTANTE**: los nombres de columnas deben existir, si no serán omitidas.
- **order**: Dirección de ordenamiento: 'ASC' para ascendente (por defecto), 'DESC' para descendente. Solo aplica si order_by está definido.
- **offset**: Número de registros a omitir desde el inicio. Solo admite valores positivos. Si no se especifica, inicia desde el primer registro.

## Consulta combinada (recomendado para pocos registros)
⚠️ **IMPORTANTE**: Usa siempre el parámetro `includes` para cargar relaciones en una sola consulta y evitar múltiples llamadas al API.

⚠️ **WARNING**: Si la relación incluida tiene muchos registros relacionados, la respuesta puede ser muy grande y lenta. Mejor consultar su endpoint directamente con filtros.

El parametro `includes` permite cargar relaciones asociadas a los registros.

### Relaciones disponibles
- **posts**: lista de Post relacionados (one-to-many)

    - **descripción**: Tabla que almacena los posts de los usuarios

### Ejemplos básicos:
#### Solo datos básicos
`usuario = GET /usuario`

#### Incluir posts
`usuario = GET /usuario?includes=posts`

#### Relaciones anidadas
Puedes incluir los datos de posts y además incluir sus propias relaciones  
`usuario = GET /usuario?includes=posts.{nested_relation}`  
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

COUNT_SUMMARY = "Cuenta registros en la tabla usuario"

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

EXISTS_SUMMARY = "Verifica existencia en la tabla usuario"

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

SUM_SUMMARY = "Suma un campo numérico específico en la tabla usuario"

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

MEAN_SUMMARY = "Calcula la media de un campo numérico específico en la tabla usuario"

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

MAX_SUMMARY = "Encuentra el valor máximo de un campo específico en la tabla usuario"

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

MIN_SUMMARY = "Encuentra el valor mínimo de un campo específico en la tabla usuario"

FIND_RESPONSES = {
    200: {
        "description": "Registro único de usuario obtenido exitosamente",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/APIResponse_UsuarioRead_"
                }
            }
        },
        "links": {
            "self": {
                "operationId": "usuario_find",
                "description": "Enlace al recurso actual",
                "parameters": {
                    "id": "$response.body#/data/id",
                    "includes": "$request.query.includes"
                }
            },
            "collection": {
                "operationId": "usuario_find_many",
                "description": "Enlace a la colección de Usuarios"
            },
            "edit": {
                "operationId": "usuario_update",
                "description": "Enlace para actualizar este Usuario",
                "parameters": {
                    "id": "$response.body#/data/id",
                }
            },
            "delete": {
                "operationId": "usuario_delete",
                "description": "Enlace para eliminar este Usuario",
                "parameters": {
                    "id": "$response.body#/data/id",
                }
            },
        "posts": {
        "operationId": "post_find_many",
                "description": "Enlace a los Posts relacionados",
                "parameters": {
                    "id": "$response.body#/data/author_id",
                    "includes": "$request.query.includes"
                }
        }
        }
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

FIND_SUMMARY = "Busca un registro en la tabla usuario"

FIND_DESCRIPTION = """
## Resumen
Obtiene un Usuario específico por su clave primaria.

Este endpoint permite recuperar un registro individual de Usuario
utilizando su identificador único (clave primaria). Opcionalmente puede
incluir datos de relaciones asociadas.

## Resultado
Si la consulta es exitosa, en `APIResponse.data`, retorna un objeto que representa un registro de la tabla `usuario` que incluye todos sus atributos

Si no se encuentra el registro, devuelve un error 404 `RECORD_NOT_FOUND`.

## Datos
Para cada registro en `data` se incluye:
- **id** (int): Campo id de la tabla usuario
- **name** (str): Nombre del usuario
- **pwd** (str): Campo pwd de la tabla usuario
- **email** (str, opcional): Campo email de la tabla usuario
- **last_post_date** (datetime, opcional): Campo last_post_date de la tabla usuario

## Parámetros de Identificación

- **id**: id del Usuario a buscar (tipo: int)

## Consulta combinada (RECOMENDADO)
⚠️ **IMPORTANTE**: Usa siempre el parámetro `includes` para cargar relaciones en una sola consulta y evitar múltiples llamadas al API.

El parametro `includes` permite cargar relaciones asociadas a los registros.

### Relaciones disponibles (usar con parámetro 'includes'):
- posts: Lista de Post relacionados (one-to-many)
    Tabla que almacena los posts de los usuarios

### Uso del parámetro 'includes':
Para cargar relaciones específicas, usa el parámetro 'includes' en la consulta:

### Ejemplos básicos:
#### Solo datos básicos
`usuario = GET /usuario/{id:int}`

#### Incluir posts
`usuario = GET /usuario/{id:int}?includes=posts`

#### Relaciones anidadas
Puedes incluir los datos de posts y además incluir sus propias relaciones  
`usuario = GET /usuario/{id:int}?includes=posts.{nested_relation}`
"""
