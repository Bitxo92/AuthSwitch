DELETE_RESPONSES = {
    200: {
        "description": "Post eliminado exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 1,
                    "message": "Post eliminado exitosamente",
                    "errors": None,
                    "meta": None
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

DELETE_SUMMARY = "Elimina un registro en la tabla post"

DELETE_MANY_RESPONSES = {
    200: {
        "description": "Posts eliminados exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": 5,
                    "message": "5 Posts eliminados exitosamente",
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

DELETE_MANY_SUMMARY = "Elimina múltiples registros en la tabla post según filtros"