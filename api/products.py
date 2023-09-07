from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

from calculations import calculate_local_deviation, calculate_sales_increase
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

    products_df = pd.DataFrame({
        'name': p.name,
        'description': p.description,
        'global_price': p.global_price,
        'local_price': p.local_price,
        'sold_quantity': p.sold_quantity,
        'previous_sold_quantity': p.previous_sold_quantity,
        'cluster': p.cluster,
        'division': p.division,
        'country': p.country,
    } for p in products)

    products_df['net_sales'] = products_df['sold_quantity'] * products_df['local_price']
    products_df['local_deviation'] = products_df.apply(
        lambda row: calculate_local_deviation(row), axis=1
    )
    products_df['sales_increase'] = products_df.apply(
        lambda row: calculate_sales_increase(row), axis=1
    )
    return [Product.model_validate(p) for p in products_df.to_dict('records')]
