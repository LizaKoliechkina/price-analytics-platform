import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from api import response_404, response_500
from calculations import percentage_increase
from database.queries import read_cluster_data, read_products
from schemas.cluster import Cluster

router = APIRouter()


@router.get(
    '/{name}',
    response_model=Cluster,
    responses={500: response_500, 404: response_404},
)
def get_cluster_data(
        name: str,
        request: Request,
) -> Cluster | JSONResponse:
    logger.info(f'Received request to get cluster data for {name}.')
    try:
        cluster_data = read_cluster_data(request.state.db, name)
        products = read_products(request.state.db, name)
    except SQLAlchemyError:
        error_msg = f'Failed to retrieve cluster data from the database for: {name}'
        logger.error(error_msg)
        return JSONResponse(status_code=500, content=error_msg)

    if not products or not cluster_data:
        error_msg = f'No data were found for cluster: {name}'
        logger.error(error_msg)
        return JSONResponse(status_code=404, content=error_msg)

    products_df = pd.DataFrame({
        'name': p.name,
        'local_price': p.local_price,
        'sold_quantity': p.sold_quantity,
    } for p in products)
    products_df['net_sales'] = products_df['sold_quantity'] * products_df['local_price']
    total_sold_quantity = products_df['sold_quantity'].sum()
    cluster_sales_increase = percentage_increase(
        total_sold_quantity, cluster_data.previous_sold_quantity
    )

    return Cluster(
        name=cluster_data.name,
        description=cluster_data.description,
        division=cluster_data.division,
        nof_products=len(products_df['name'].unique()),
        sold_quantity=total_sold_quantity,
        net_sales=round(products_df['net_sales'].sum(), 2),
        sales_increase=cluster_sales_increase,
    )
