
CREATE_RESPONSES = {
    422: {
        "description": "Error de validación en los datos de entrada",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error de validación",
                    "errors": [
                        {
                            "code": "VALIDATION_ERROR",
                            "message": "El campo es requerido",
                            "field": "content",
                            "details": None
                        }
                    ],
                    "meta": None
                }
            }
        }
    },
    409: {
        "description": "Registro duplicado",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "El registro ya existe",
                    "errors": [
                        {
                            "code": "DUPLICATE_RECORD",
                            "message": "El registro ya existe",
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

CREATE_SUMMARY = "Crea un registro en la tabla comment"

AGG_RESPONSES = {
    200: {
        "description": "Agregaciones calculadas exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": {
                        "sum_edad": 450,
                        "sum_salario": 150000.50,
                        "mean_edad": 30.5,
                        "max_fecha_nacimiento": "2000-01-15T00:00:00",
                        "min_fecha_nacimiento": "1970-05-20T00:00:00"
                    },
                    "message": "Agregaciones calculadas exitosamente",
                    "meta": {
                        "total_operations": 4,
                        "valid_operations": 4,
                        "total_expressions": 5,
                        "warnings": []
                    }
                }
            }
        }
    },
    422: {
        "description": "Error de validación en operaciones o filtros",
        "content": {
            "application/json": {
                "example": {
                    "status": "error",
                    "data": None,
                    "message": "Error de validación",
                    "errors": [
                        {
                            "code": "VALIDATION_ERROR",
                            "message": "Operación 'median' no soportada. Operaciones válidas: ['sum', 'mean', 'max', 'min']",
                            "field": "operations",
                            "details": None
                        }
                    ]
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
                            "code": "INTERNAL_SERVER_ERROR",
                            "message": "Ha ocurrido un error inesperado",
                            "field": None,
                            "details": None
                        }
                    ]
                }
            }
        }
    }
}

AGG_SUMMARY = "Realiza múltiples agregaciones en la tabla comment"

AGG_DESCRIPTION = """
## Resumen
Realiza múltiples operaciones de agregación en una sola consulta sobre la tabla comment.

Este endpoint permite combinar diferentes operaciones de agregación (sum, mean, max, min, count) 
sobre múltiples campos en una única petición.

## Cuerpo de la Petición

### operations (requerido)
Diccionario donde cada clave es una operación y el valor es una lista de campos o expresiones.

#### Operaciones disponibles:
- **sum**: Suma de valores numéricos
- **mean**: Promedio de valores numéricos
- **max**: Valor máximo (numérico o fechas)
- **min**: Valor mínimo (numérico o fechas)
- **count**: Conteo de registros

### filters (opcional)
Diccionario con filtros a aplicar:
- **content**: Filtrar por content
    - **in_content**: Filtrar por múltiples valores de content (OR lógico)
    - **post_id**: Filtrar por post_id
    - **in_post_id**: Filtrar por múltiples valores de post_id (OR lógico)

"""