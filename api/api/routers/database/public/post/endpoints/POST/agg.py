from fastapi import Body, Depends
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel
from ......auth import requires_permissions, AccessToken
from ...._shared import username_context, get_model_by_name

from ...database import PostAsyncDAO, PostFilter, AggRow, AggRequest
from api.resources import APIResponse, APIError, ErrorCode
from .docs import AGG_RESPONSES, AGG_SUMMARY, AGG_DESCRIPTION
from ... import post_router

class AggregationPayload(BaseModel):
    operations: AggRequest
    filters: Optional[PostFilter] = None

@post_router.post("/agg",
    response_model=APIResponse[List[AggRow]],
    operation_id="public_post_aggregate",
    summary=AGG_SUMMARY,
    description=AGG_DESCRIPTION,
    responses=AGG_RESPONSES
)
async def post_aggregate(
    payload: AggregationPayload = Body(...,
        example={
            "operations": {
                "sum": ["precio", "precio*cantidad", {"expr": "ingreso-coste", "as": "ganancia"}],
                "mean": ["cantidad"],
                "max": ["fecha_creacion"],
                "min": ["fecha_creacion"]
            },
            "filters": {
                "activo": True,
                "email": "%@gmail.com"
            }
        }
    ),
    token: AccessToken = Depends(requires_permissions("read", "post")),
) -> APIResponse[List[AggRow]]:
    """
    Realiza múltiples operaciones de agregación en una sola consulta sobre la tabla post.
    """
    with username_context(token.preferred_username):
        result = await PostAsyncDAO.agg(
            request=payload.operations,
            **payload.filters.to_dict()
        )

        if not result.success:
            return APIResponse.error(
                errors=[
                    APIError(
                        code=ErrorCode.VALIDATION_ERROR,
                        message=error,
                        field=field
                    ) for error, field in result.errors
                ],
                message="No se pudieron procesar las agregaciones"
            )

        return APIResponse.success(
            data=result.rows,
            message="Agregaciones calculadas exitosamente",
            meta=result.metadata
        )
