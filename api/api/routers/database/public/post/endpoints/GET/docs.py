from typing import Optional, List, Union

FIND_MANY_RESPONSES = {
    200: {
        "description": "Lista de registros de post obtenido exitosamente",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/APIResponse_List_PostRead__"
                }
            }
        },
        "links": {
            "self": {
                "operationId": "post_find_many",
                "description": "Enlace a la consulta actual con los mismos filtros",
                "parameters": {
        "title": "$request.query.title",
        "content": "$request.query.content",
        "content_type": "$request.query.content_type",
        "timestamp": "$request.query.timestamp",
        "author_id": "$request.query.author_id",
                    "limit": "$request.query.limit",
                    "offset": "$request.query.offset",
                    "order_by": "$request.query.order_by",
                    "order": "$request.query.order",
                    "includes": "$request.query.includes"
                }
            },
            "item": {
                "operationId": "post_find",
                "description": "Enlace para acceder a un elemento específico",
                "parameters": {
                    "id": "$response.body#/data/**/id",
                    "includes": "$request.query.includes"
                }
            },
            "create": {
                "operationId": "post_create",
                "description": "Enlace para crear un nuevo Post"
            },
            "count": {
                "operationId": "post_count",
                "description": "Enlace para obtener el conteo total con los mismos filtros",
                "parameters": {
        "title": "$request.query.title",
        "content": "$request.query.content",
        "content_type": "$request.query.content_type",
        "timestamp": "$request.query.timestamp",
        "author_id": "$request.query.author_id",
                }
            },
        "comments": {
        "operationId": "comment_find_many",
                "description": "Enlace a los Comments relacionados",
                "parameters": {
                    "id": "$response.body#/data/**/post_id",
                    "includes": "$request.query.includes"
                }
        },
        "author": {
        "operationId": "usuario_find",
                "description": "Enlace al Usuario relacionado",
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

FIND_MANY_SUMMARY = "Busca varios registros en la tabla post"
FIND_MANY_DESCRIPTION = """
## Resumen
Obtiene una lista de `posts` con filtros opcionales y soporte para paginación.

Este endpoint permite realizar búsquedas flexibles aplicando filtros opcionales
por cualquiera de los campos disponibles, con soporte completo para paginación
mediante los parámetros limit y offset.

## Resultado
En `APIResponse.data`, retorna un listado de objetos donde cada uno representa un registro de la tabla `post` que incluye todos sus atributos

## Datos
Para cada registro en `data` se incluye:
- **id** (bigint): Campo id de la tabla post
- **title** (str): Campo title de la tabla post
- **content** (str): Contenido del post
- **content_type** (str): Campo content_type de la tabla post
- **timestamp** (datetime): Fecha y hora del post
- **author_id** (int): Campo author_id de la tabla post

## Parámetros de Filtrado

Todos los parámetros de filtrado son opcionales y se pueden combinar:
- **title**: Filtrar por title
    - **in_title**: Filtrar por múltiples valores de title (OR lógico)
    - **content**: Filtrar por content
    - **in_content**: Filtrar por múltiples valores de content (OR lógico)
    - **content_type**: Filtrar por content_type
    - **in_content_type**: Filtrar por múltiples valores de content_type (OR lógico)
    - **min_timestamp**: Filtrar por valor mínimo de timestamp (incluído)
    - **max_timestamp**: Filtrar por valor máximo de timestamp (incluído)
    - **author_id**: Filtrar por author_id
    - **in_author_id**: Filtrar por múltiples valores de author_id (OR lógico)


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
- **comments**: lista de Comment relacionados (one-to-many)

    - **descripción**: Tabla que almacena los comentarios de los posts
- **author**: Usuario relacionado (many-to-one)

    - **descripción**: Tabla que almacena información de los usuarios del sistema

### Ejemplos básicos:
#### Solo datos básicos
`post = GET /post`

#### Incluir comments
`post = GET /post?includes=comments`

#### Incluir author
`post = GET /post?includes=author`

#### Múltiples relaciones en una sola consulta
`post = GET /post?includes=comments&includes=author`

#### Relaciones anidadas
Puedes incluir los datos de comments y además incluir sus propias relaciones  
`post = GET /post?includes=comments.{nested_relation}`  
Puedes incluir los datos de author y además incluir sus propias relaciones  
`post = GET /post?includes=author.{nested_relation}`  
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

COUNT_SUMMARY = "Cuenta registros en la tabla post"

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

EXISTS_SUMMARY = "Verifica existencia en la tabla post"

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

SUM_SUMMARY = "Suma un campo numérico específico en la tabla post"

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

MEAN_SUMMARY = "Calcula la media de un campo numérico específico en la tabla post"

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

MAX_SUMMARY = "Encuentra el valor máximo de un campo específico en la tabla post"

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

MIN_SUMMARY = "Encuentra el valor mínimo de un campo específico en la tabla post"

FIND_RESPONSES = {
    200: {
        "description": "Registro único de post obtenido exitosamente",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/APIResponse_PostRead_"
                }
            }
        },
        "links": {
            "self": {
                "operationId": "post_find",
                "description": "Enlace al recurso actual",
                "parameters": {
                    "id": "$response.body#/data/id",
                    "includes": "$request.query.includes"
                }
            },
            "collection": {
                "operationId": "post_find_many",
                "description": "Enlace a la colección de Posts"
            },
            "edit": {
                "operationId": "post_update",
                "description": "Enlace para actualizar este Post",
                "parameters": {
                    "id": "$response.body#/data/id",
                }
            },
            "delete": {
                "operationId": "post_delete",
                "description": "Enlace para eliminar este Post",
                "parameters": {
                    "id": "$response.body#/data/id",
                }
            },
        "comments": {
        "operationId": "comment_find_many",
                "description": "Enlace a los Comments relacionados",
                "parameters": {
                    "id": "$response.body#/data/post_id",
                    "includes": "$request.query.includes"
                }
        },
        "author": {
        "operationId": "usuario_find",
                "description": "Enlace al Usuario relacionado",
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

FIND_SUMMARY = "Busca un registro en la tabla post"

FIND_DESCRIPTION = """
## Resumen
Obtiene un Post específico por su clave primaria.

Este endpoint permite recuperar un registro individual de Post
utilizando su identificador único (clave primaria). Opcionalmente puede
incluir datos de relaciones asociadas.

## Resultado
Si la consulta es exitosa, en `APIResponse.data`, retorna un objeto que representa un registro de la tabla `post` que incluye todos sus atributos

Si no se encuentra el registro, devuelve un error 404 `RECORD_NOT_FOUND`.

## Datos
Para cada registro en `data` se incluye:
- **id** (bigint): Campo id de la tabla post
- **title** (str): Campo title de la tabla post
- **content** (str): Contenido del post
- **content_type** (str): Campo content_type de la tabla post
- **timestamp** (datetime): Fecha y hora del post
- **author_id** (int): Campo author_id de la tabla post

## Parámetros de Identificación

- **id**: id del Post a buscar (tipo: bigint)

## Consulta combinada (RECOMENDADO)
⚠️ **IMPORTANTE**: Usa siempre el parámetro `includes` para cargar relaciones en una sola consulta y evitar múltiples llamadas al API.

El parametro `includes` permite cargar relaciones asociadas a los registros.

### Relaciones disponibles (usar con parámetro 'includes'):
- comments: Lista de Comment relacionados (one-to-many)
    Tabla que almacena los comentarios de los posts
- author: Usuario relacionado (many-to-one)
    Tabla que almacena información de los usuarios del sistema

### Uso del parámetro 'includes':
Para cargar relaciones específicas, usa el parámetro 'includes' en la consulta:

### Ejemplos básicos:
#### Solo datos básicos
`post = GET /post/{id:int}`

#### Incluir comments
`post = GET /post/{id:int}?includes=comments`

#### Incluir author
`post = GET /post/{id:int}?includes=author`

#### Múltiples relaciones en una sola consulta
`post = GET /post/{id:int}?includes=comments&includes=author`

#### Relaciones anidadas
Puedes incluir los datos de comments y además incluir sus propias relaciones  
`post = GET /post/{id:int}?includes=comments.{nested_relation}`
Puedes incluir los datos de author y además incluir sus propias relaciones  
`post = GET /post/{id:int}?includes=author.{nested_relation}`
"""
