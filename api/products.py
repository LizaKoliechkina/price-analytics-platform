from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

from api import response_404, response_500
from calculations import calculate_local_deviation, calculate_sales_increase
from database.queries import read_products, get_cluster_division
from schemas.product import Product

router = APIRouter()


@router.get(
    '/{country}/{cluster}',
    response_model=list[Product],
    responses={500: response_500, 404: response_404},
)
def get_products(
        country: str,
        cluster: str,
        request: Request,
) -> list[Product] | HTTPException:
    logger.info(
        f'Received request to get products for '
        f'following parameters: {country}, {cluster}.'
    )
    try:
        products = read_products(request.state.db, cluster, country)
    except SQLAlchemyError as e:
        error_msg = (
            f'Failed to retrieve products from the database '
            f'for {country}, {cluster}: {e}'
        )
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

    if not products:
        error_msg = f'No products were found for given parameters: {country}, {cluster}'
        logger.error(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)

    division = get_cluster_division(request.state.db, cluster)

    products_df = pd.DataFrame({
        'name': p.name,
        'description': p.description,
        'global_price': p.global_price,
        'local_price': p.local_price,
        'sold_quantity': p.sold_quantity,
        'previous_sold_quantity': p.previous_sold_quantity,
        'cluster': p.cluster,
        'division': division,
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
