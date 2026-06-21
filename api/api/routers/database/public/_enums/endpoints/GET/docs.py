PERMISSION_TYPE_RESPONSES = {
    200: {
        "description": "Valores de la enumeración permission_type obtenidos exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": ["api", "app"],
                    "message": "Enumeración permission_type obtenida exitosamente",
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
PERMISSION_TYPE_RESPONSES = {
    200: {
        "description": "Valores de la enumeración permission_type obtenidos exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": ["api", "app"],
                    "message": "Enumeración permission_type obtenida exitosamente",
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
CONTENT_TYPE_RESPONSES = {
    200: {
        "description": "Valores de la enumeración content_type obtenidos exitosamente",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": ["text", "image", "video"],
                    "message": "Enumeración content_type obtenida exitosamente",
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
