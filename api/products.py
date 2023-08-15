from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from database.queries import read_products
from schemas.product import Product

router = APIRouter()


@router.get(
    '/{country}/{division}/{cluster}',
    response_model=list[Product],
    responses={
        500: {'description': 'Failed to retrieve products from the database', 'model': str},
        404: {'description': 'No products were found for given parameters', 'model': str},
    },
)
def get_products(
        country: str,
        division: str,
        cluster: str,
        request: Request,
) -> list[Product] | JSONResponse:
    logger.info(
        f'Received request to get products for '
        f'following parameters: {country}, {division}, {cluster}.'
    )
    try:
        products = read_products(request.state.db, country, division, cluster)
    except SQLAlchemyError as e:
        error_msg = (
            f'Failed to retrieve products from the database '
            f'for {country}, {division}, {cluster}: {e}'
        )
        logger.error(error_msg)
        return JSONResponse(status_code=500, content=error_msg)

    if not products:
        error_msg = (
            f'No products were found for given '
            f'parameters: {country}, {division}, {cluster}',
        )
        logger.error(error_msg)
        return JSONResponse(status_code=404, content=error_msg)

    return [Product.model_validate(p) for p in products]  # Pydantic v1: Product.from_orm(p)
